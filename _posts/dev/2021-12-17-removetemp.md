---
layout: post
title:  "Remove content from Temp"
author: Tinu
categories: "PowerShell-Basic"
tags:   PowerShell News
permalink: /posts/:title:output_ext
---

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Temp-folders](#temp-folders)
  - [List content from temp-folders](#list-content-from-temp-folders)
  - [Remove content from temp-folders](#remove-content-from-temp-folders)
- [See also](#see-also)

# Temp-folders

We known a Windows Server has (too) many temp-folders and did not clean-up this folders.

## List content from temp-folders

List content of temp-folders if it's older than 3 month.

````powershell
$UsersRoot = $($home) -split '\\'
$AllUsers  = Join-Path -Path "$($splitted[0])" -ChildPath "$($splitted[1])"
$AllUsersTemp = $AllUsers | Get-ChildItem | ForEach { 
    Join-Path -Path $_.FullName -ChildPath 'AppData\Local\Temp' 
}

$folders = @(
    "$($env:systemroot)\Temp"
    $AllUsersTemp 
)
Get-ChildItem $folders -ErrorAction SilentlyContinue | Sort LastWriteTime | 
 Where LastWriteTime -lt (Get-Date).AddMonths(-3)
````

## Remove content from temp-folders

Remove content of temp-folders if it's older than 3 month.

````powershell
$folders = @(
    "$($env:systemroot)\Temp"
    $AllUsersTemp
)
Get-ChildItem $folders -ErrorAction SilentlyContinue | Sort LastWriteTime | 
 Where LastWriteTime -lt (Get-Date).AddMonths(-3) | Remove-Item -Recurse
````

# See also

[Weekend Scripter: Use PowerShell to Clean Out Temp Folders](https://devblogs.microsoft.com/scripting/weekend-scripter-use-powershell-to-clean-out-temp-folders/) on devblogs.microsoft.com

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]