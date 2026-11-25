---
title: Local Groups
date: '2017-06-21T16:28:16+02:00'
author: Tinu
excerpt: ''
categories:
- Active Directory
- PowerShell
tags:
- Accounts
- Hashtable
- PSObject
wordpress_id: 2204
layout: post
permalink: /wiki/local-admins/
render_with_liquid: false
---

Alle lokalen Gruppen mit den Mitgliedern auflisten und als Object mit einer Hashtable zurückgeben.

## WinNT-Provider

 Ohne das Windows Management Framework 5.1 musste mühsam über den WinNT-Provider oder mit dem [Local Account Management Module](https://gallery.technet.microsoft.com/scriptcenter/Local-Account-Management-a777191b) aus der Technet Gallery auf die lokalen User und Gruppen zugegriffen werden. 

```
function CheckLocalAdmins{
    <# Check the Membership in local Groups#>
    [cmdletbinding()]
    Param()
    $ErrorActionPreference = "SilentlyContinue "
    $function = $($MyInvocation.MyCommand.Name)
    write-verbose "Running $($function) ..."
    $Computer = [ADSI]"WinNT://$env:ComputerName,Computer"
    $Groups   = $Computer.psbase.Children | Where {$_.psbase.schemaClassName -eq "group"}
    $Hash     = [ordered]@{}
    $Hash.ComputerName = $($env:COMPUTERNAME)
    ForEach ($Group In $Groups){
        $Hash.LocalGroups += @{$Group.Name=$Group.Description}
        $Members           = @($Group.psbase.Invoke("Members"))
        ForEach ($Member In $Members){
            try{
                $UserName    = $Member.GetType().InvokeMember("Name", 'GetProperty', $Null, $Member, $Null)
                $Description = $Member.GetType().InvokeMember("Description", 'GetProperty', $Null, $Member, $Null)
            }
            catch [Exception]{
                $UserName = $Group.Name
                $Description = "ERROR: $($_.Exception.Message)"
                $error.clear()
            }
            finally{
                $Hash.$($Group.Name) += @{$UserName=$Description}
            }
        }
    }
    $Obj = New-Object psobject -Property $Hash
    return $Obj
}
```

## WMI

 Variante mit dem Get-WMiObject Cmdlet. 

```
function Get-LocalGroups
{
    [cmdletbinding()]
    param($ComputerName)
    $function = $($MyInvocation.MyCommand.Name)
    write-verbose "Running $($function) ..."
    $wmiobject    = Get-WmiObject -ComputerName $ComputerName -Query "SELECT * FROM Win32_GroupUser" 
    $Groups       = @()
    if ($wmiobject -ne $null) 
    { 
        foreach ($item in $wmiobject) 
        { 
            $Group = ($item.GroupComponent.Substring($item.GroupComponent.IndexOf(',') + 1).Replace('Name=', '').Replace("`"", '')) 
            if(-not($Groups.Contains($Group)))
            {
                $Groups += $Group
            }
        } 
    }
    else
    {
        Write-Verbose "there is something wrong in paradise"
    }
    return $Groups
}

$ComputerName = $env:computername
$Groups = Get-LocalGroups -ComputerName $ComputerName
$Hash = [ordered]@{}
$Hash.ComputerName = $($ComputerName)

foreach($GroupName in $Groups){
    Write-Verbose $GroupName -Verbose
    $wmiobject = Get-WmiObject -ComputerName $ComputerName -Query `
    "SELECT * FROM Win32_GroupUser WHERE GroupComponent=`"Win32_Group.Domain='$ComputerName',Name='$GroupName'`"" 
    $Users = @()
    # Parse out the username from each result and append it to the array. 
    if ($wmiobject -ne $null) 
    { 
        foreach ($item in $wmiobject) 
        { 
            $User = ($item.PartComponent.Substring($item.PartComponent.IndexOf(',') + 1).Replace('Name=', '').Replace("`"", '')) 
            if($Users.Contains($User))
            {
                Write-Verbose "$User already in array"
            }
            else
            {
                $Users += $User
            }
        } 
        $Hash.Groups += @{$GroupName=$Users}
    } 
}
return $Hash
```

## WMF 5.1

 Mit dem Modul Microsoft.Power­Shell.Local­Accounts aus dem Windows Management Framework 5.1 kann einfach auf die lokalen User und Gruppen zugegriffen werden. 

```
function CheckLocalAdmins{
    <# Check the Membership in local Groups #>
    [cmdletbinding()]
    Param()
    $ErrorActionPreference = "SilentlyContinue "
    $function = $($MyInvocation.MyCommand.Name)
    write-verbose "Running $($function) ..."
    $Groups   = Get-LocalGroup
    $Hash     = [ordered]@{}
    $Hash.ComputerName = $($env:COMPUTERNAME)
    ForEach ($Group In $Groups){
        $Hash.LocalGroups += @{$Group.Name=$Group.Description}
        $Members           = @(Get-LocalGroupMember -Group $Group)
        ForEach ($Member In $Members){
            try{
                $UserName    = $Member.SID
                $Description = $Member.Name
            }
            catch [Exception]{
                $UserName    = $Group.Name
                $Description = "ERROR: $($_.Exception.Message)"
                $error.clear()
            }
            finally{
                $Hash.$($Group.Name) += @{$UserName=$Description}
            }
        }
    }
    $Obj = New-Object psobject -Property $Hash
    return $Obj
}
```