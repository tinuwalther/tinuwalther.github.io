---
layout: post
title:  "Read Value from Registry"
author: Tinu
categories: "PowerShell-Registry"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Read Single-Value from Registry](#read-single-value-from-registry)
- [Read Values from all Users](#read-values-from-all-users)
  - [Volatile registry key](#volatile-registry-key)
- [See also](#see-also)

Copy items from a local to a remote computer using a psremote-session.

# Read Single-Value from Registry

````powershell
function Get-RegistryValue {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$false)]
        [Object]$args
    )
    $ret = $null
    if(Test-Path "$($args.Hive):\$($args.Path)"){
        Try{
            $ret = Get-ItemPropertyValue -Path "$($args.Hive):\$($args.Path)" -Name $args.Property
        }
        catch{
            $ret = $null
        }
    }
    return $ret
}

$params = @{
    Hive     = 'HKLM'
    Path     = 'SOFTWARE\Microsoft\Windows NT\CurrentVersion'
    Property = 'ReleaseId'
}

return (Get-RegistryValue -args $params)
````

# Read Values from all Users

````powershell
$ErrorActionPreference = 'SilentlyContinue'

if(-not(Get-PSDrive -Name 'HKU')){
    New-PSDrive HKU Registry HKEY_USERS
}

$path = '\Control Panel\International'

Get-ChildItem "HKU:\" | ForEach {
    if (Test-Path "HKU:\$($_.Name)\$($path)"){
        @{"$($_.Name)" = "$(Get-ItemPropertyValue "HKU:\$($_.Name)\$($path)" -Name "LocaleName")"}
        if($error){
            $error.Clear()
        }
    }
}
````

## Volatile registry key

If you use the New-Item-Cmdlet, the subkey is created as stable key. Sometimes you need a subkey that will be deleted after a reboot, you can create a volatile subkey.

````powershell
$HKLM   =[Microsoft.Win32.RegistryKey]::OpenBaseKey('LocalMachine','default')
$SubKey = $HKLM.OpenSubKey('SOFTWARE\Company\Settings', $true)
$SubKey.CreateSubKey('Volatile', $true , [Microsoft.Win32.RegistryOptions]::Volatile)
$SubKey.CreateSubKey('Non-Volatile', $true , [Microsoft.Win32.RegistryOptions]::None)
````


# See also

[Get-ItemPropertyValue](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-itempropertyvalue?view=powershell-6) on Microsoft Docs.

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]