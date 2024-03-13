---
layout: post
title:  "Hashtable"
author: Tinu
categories: "PowerShell-Basic"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Create a hashtable](#create-a-hashtable)
- [Loop through a hashtable](#loop-through-a-hashtable)

## Create a hashtable

Create a hashtable from an file-system-object.

````powershell
Get-ChildItem -Path $home | ForEach-Object{
    @{$_.Name=(Split-Path -Parent $_.Fullname)}
}
````

Output from my Mac:

````text
Name                           Value
----                           -----
Applications                   /Users/xxx
Desktop                        /Users/xxx
Documents                      /Users/xxx
Downloads                      /Users/xxx
Movies                         /Users/xxx
Music                          /Users/xxx
Pictures                       /Users/xxx
Public                         /Users/xxx
````

## Loop through a hashtable

Loop through a hashtable and get one single entry.

````powershell
$targetroot = 'Z:'
$datahash   = [ordered]@{
    'S:\Scripting'    = "$($targetroot)\Backup\Scripting"
    'D:\Dokumente'    = "$($targetroot)\Backup\Dokumente"
    'W:\WebSites'     = "$($targetroot)\Backup\WebSites"
    'C:\Daten\Tools'  = "$($targetroot)\Backup\Tools"
    'F:\Fotografie'   = "$($targetroot)\Fotografie\Kataloge"
    'H:\HyperV'       = "$($targetroot)\Virtualisierung\HyperV"
}
````

````powershell
foreach($item in $datahash.keys){
    if($item -match 'WebSites'){
        Write-Output "Source $($item), Target $($datahash[$item])"
    }
}
````

Output:

````text
Source W:\WebSites, Target Z:\Backup\WebSites
````

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]
