---
title: Registry
date: '2014-11-26T20:29:58+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Hashtable
- Registry
wordpress_id: 138
layout: post
permalink: /wiki/registry/
render_with_liquid: false
---

## List Subkeys Name, Property and Value

Ab einem Hive alle Subkeys mit Name, Property und Value auflisten. 

```
function Get-RegistryProperties{

    param(
        [Parameter(Mandatory=$true)][String] $hive
    )

    $ret = @()
    if(Test-path -Path $hive){
        $root = Get-Item $hive
        foreach($subkey in $root.GetSubKeyNames()){

            $items = Get-Item "$hive\$subkey"
            if($items.subkeycount -eq 0){

                foreach($prop in $items.Property){

                    $obj = [PSCustomObject]@{
                        Hive     = $hive
                        Name     = $items.PSChildName
                        Property = $prop
                        Value    = Get-ItemPropertyValue -Path ("$hive\$subkey") -Name ($prop)
                    }
                    $ret += $obj

                }

            }
            else{
                Get-RegistryProperties -hive "$hive\$subkey"
            }

        }
    }
    return $ret

}

Get-RegistryProperties -hive 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion' | Sort-Object Hive, Name | Format-Table
```

## Remote Registry

Hives: LocalMachine, Users oder CurrentUser 

```csharp
$hive = 'LocalMachine' #Users, CurrentUser
$computer = Read-Host "Computer eingeben"
$Reg = [Microsoft.Win32.RegistryKey]::OpenRemoteBaseKey($hive, $computer)
$RegKeys = $Reg.OpenSubKey("SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
$RegKeys.GetValueNames() | % {"$($_)  $($RegKeys.GetValue($_))"}
```

## Local Registry

HKEY\_LOCAL\_MACHINE kann direkt mit HKLM:\\ angesprochen werden 

```csharp
gi "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run"
```

HKEY\_USERS neues Object auf Basis PSDrive erstellen 

```csharp
New-PSDrive HKU Registry HKEY_USERS
```

danach kann auf Subkeys zugegriffen werden, hier z.B. auf das Trennzeichen in den Regional Settings 

```csharp
gci "HKU:\" | % {
    if (Test-Path "HKU:\$($_.Name)\Control Panel\International"){
        $Delimiter = (gp "HKU:\$($_.Name)\Control Panel\International" `
         -Name "sDecimal").sDecimal
        "$($_.Name) $($Delimiter)"
    }
}
```

## Registry key mit Value erstellen

```
function Set-RegistryValue {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$false)][Object]$Props
    )
    $function = $($MyInvocation.MyCommand.Name)
    Write-verbose $function
    $ret = $null
    if(Test-Path $Properties.RootKey){
        Try{
            $Item = (Set-ItemProperty -Path $Props.RootKey -Name $Props.Name -Value $Props.Value -PassThru -ErrorAction Stop)
            $ret = @{ItemProperty=$Item}
        }
        catch{
            $ret = $null
        }
    }
    return $ret
}
```

```
# -- Arrange
$pr         = @{}
$pr.RootKey = 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon'
$pr.Name    = 'AutoAdminLogon'
$pr.Value   = 1

# -- Act
$Actual = Set-RegistryValue -Props $p
$Actual.Values
```

## Registry Value prüfen

```
function Test-RegistryValue {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$false)][Object]$Props
    )
    $ret = $false
    if(Test-Path $Properties.RootKey){
        Try{
            $ItemValue = (Get-ItemProperty -Path $Props.RootKey -Name $Props.Name -ErrorAction Stop)."$($Props.Name)" 
            if ($ItemValue -eq $Props.Value){
                $ret = $true
            }
        }
        catch{
            $ret = $true
        }
    }
    return $ret
}
```

```
# -- Arrange
$pr         = @{}
$pr.RootKey = 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon'
$pr.Name    = 'AutoAdminLogon'
$pr.Value   = 0

# -- Act
$Actual = Test-RegistryValue -Props $pr
```

## Registrypfade rekursive auslesen

Registrypfade rekurive auslesen und Pfade in Hashtable aufnehmen. 

```
function Get-RegistryPathRecurse{
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][String]$path
    )
    $function = $($MyInvocation.MyCommand.Name)
    $ret = $null
    try{
        if($path -match '^HKLM:\\.+\\'){
            $collection = $path.Split('\')
            if($collection -is [array]){
                $regpath    = $collection[0]
                $returnhash = @{}
                for($i = 1; $i -le $collection.GetUpperBound(0); $i++){
                    $regpath = "$($regpath)\$($collection[$i])"
                    if(Test-Path $regpath -ErrorAction SilentlyContinue){
                        $returnhash.Add($regpath, $true)
                    }
                    else{
                        $returnhash.Add($regpath, $false)
                    }
                }
                $ret = $returnhash
            }
        }
    }
    catch{
        Write-Host "$($function): $($_.Exception)" -Foregroundcolor Red
        $Error.Clear()
    }
    return $ret
}

$reghash = Get-RegistryPathRecurse -path 'HKLM:\SOFTWARE\Company\ImageInfo'
if($reghash -is [hashtable]){
    foreach($item in $reghash.keys){
        if($($reghash[$item])){
            # path exists
            Write-Output "$($item), $($reghash[$item])"
        }
        else{
            # path not exists
            Write-Output "$($item), $($reghash[$item])"
        }
    }
}
```

## Registrypfade rekursive erstellen

Registrypfade rekurive erstellen. 

```csharp
function Set-RegistryPathRecurse
{
 param(
 [string]$path = ''
 )
 $collection = $path.Split('\')
 $regpath = $collection[0]
 $returnhash = @{}
 for($i = 1; $i -le $collection.GetUpperBound(0); $i++)
 {
 $regpath = "$($regpath)\$($collection[$i])"
 if(-not(Test-Path $regpath -ErrorAction SilentlyContinue))
 {
 $returnhash.Add($regpath, 'created')
 New-Item -Path $regpath
 }
 }
 return $returnhash
}
$reghash = Get-RegistryPathRecurse -path "HKLM:\SOFTWARE\Company\ImageInfo"
```

## Mehrere Registryvalues erstellen

Mehrere Registryvalues aus einer Hashtable erstellen. 

```csharp
$regpath  = "HKLM:\SOFTWARE\Company\ImageInfo"
$datahash = @{
 PatchLevel          = "October 2016"
 TemplateDescription = "VMware Template"
 TemplateVersion     = "1.0.0.00001"
}
foreach($item in $datahash.keys)
{
 "Name: $($item), Data: $($datahash[$item])"
 if(-not((Get-ItemProperty -Path $regpath -Name $($item) -ErrorAction SilentlyContinue).$item))
 {
 Set-ItemProperty -Path $regpath -Name $($item) -Value $($datahash[$item]) -PassThru
 }
}
```