---
layout: post
title:  "List installed Software"
author: Tinu
categories: "System-Engineering"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Get Software from WMI](#get-software-from-wmi)
- [Get Software from Uninstallkey](#get-software-from-uninstallkey)

# Get Software from WMI

Loop through the Win32_Product class and get all installed software.

````powershell
$collection = Get-WmiObject -Class Win32_Product -ErrorAction SilentlyContinue | Where-Object {-not([string]::IsNullOrEmpty($_.Name))}

$resultset = @()
foreach($item in $collection){
   $obj = [PSCustomObject]@{
      InstallDate = $item.InstallDate
      Vendor      = $item.Vendor
      Name        = $item.Name
      PackageName = $item.PackageName
      Description = $item.Description
      Version     = $item.Version
   }
   $resultset += $obj
}
$resultset | Sort-Object Name | Format-Table -AutoSize
````

Output:

````text
InstallDate Vendor                     Name                        Version
----------- ------                     ----                        -------
20180822    Adobe Systems Incorporated Adobe Acrobat Reader DC MUI 18.009.20044
20180918    Microsoft Corporation      PowerShell 6-x64            6.1.0.0
````

# Get Software from Uninstallkey

Formats a hashtable to a PSCustomObject.

````powershell
# 64-bit applications that run on a 64-bit version of Windows
$collection = Get-ChildItem 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall' `
| Get-ItemProperty | Where-Object {-not([string]::IsNullOrEmpty($_.DisplayName))} `
| Select-Object DisplayName,DisplayVersion,UninstallString

# 32-bit applications that run on a 64-bit version of Windows
$collection += Get-ChildItem 'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall' `
| Get-ItemProperty | Where-Object {-not([string]::IsNullOrEmpty($_.DisplayName))} `
| Select-Object DisplayName,DisplayVersion,UninstallString

$resultset = @()
foreach($item in $collection){
    $obj = [PSCustomObject] @{
        Name            = $item.DisplayName
        Version         = $item.DisplayVersion
        UninstallString = $item.UninstallString
    }
    $resultset += $obj
}
$resultset | Sort-Object Name | Format-Table -AutoSize
````

Output:

````text
Name                                Version         UninstallString
----                                -------         ---------------
Adobe Acrobat Reader DC - Deutsch   19.010.20091    MsiExec.exe /I{AC76BA86-7AD7-1031-7B44-AC0F074E4100}
PowerShell 6-x64                    6.1.2.0         MsiExec.exe /X{65276649-728D-4AB9-AAEC-6EFF860B11EC}
````

[ [Top](#table-of-contents) ] [ [Blog](../devops.html) ]