---
title: Software auflisten
date: '2015-10-02T16:46:52+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- PSObject
- Software
wordpress_id: 1376
layout: post
permalink: /wiki/software-auflisten/
render_with_liquid: false
---

## Alle installierte Software auflisten

 Ab PowerShell Version 2.0 

```
function Get-InstaledSoftware{
    [CmdletBinding()]
    param($param1)
    $function = $($MyInvocation.MyCommand.Name)
    $ret = @()
    Get-WmiObject -Class Win32_Product -ErrorAction SilentlyContinue | Where-Object {-not([string]::IsNullOrEmpty($_.Name))} | %{
        $obj = New-Object PSObject
        $obj | Add-Member NoteProperty Name            $_.Name
        $obj | Add-Member NoteProperty Description     $_.Description
        $obj | Add-Member NoteProperty InstallDate     $([DateTime]::ParseExact($_.InstallDate,'yyyyMMdd',$null))
        $obj | Add-Member NoteProperty Version         $_.Version
        $obj | Add-Member NoteProperty Language        $_.Language
        $obj | Add-Member NoteProperty PackageName     $_.PackageName
        $obj | Add-Member NoteProperty LocalPackage    $_.LocalPackage
        $obj | Add-Member NoteProperty InstallSource   $_.InstallSource
        $obj | Add-Member NoteProperty InstallLocation $_.InstallLocation
        $obj | Add-Member NoteProperty Vendor          $_.Vendor
        $obj | Add-Member NoteProperty HelpLink        $_.HelpLink
        $obj | Add-Member NoteProperty URLInfoAbout    $_.URLInfoAbout
        $obj | Add-Member NoteProperty  URLUpdateInfo  $_.URLUpdateInfo
        $ret += $obj
    }
    return $ret
}
Get-InstaledSoftware | Out-GridView
```

## Software mit bestimmtem Namen auflisten

```
Get-WmiObject -Class Win32_Product -Filter "Name LIKE '%Windows%'"
```

## Software über den Uninstall Key auflisten

```
$Application = 'End Point Operations Manager'
Get-ChildItem 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall' `
| Get-ItemProperty | Where-Object {$_.DisplayName -match $Application } `
| Select DisplayName,DisplayVersion,UninstallString
```