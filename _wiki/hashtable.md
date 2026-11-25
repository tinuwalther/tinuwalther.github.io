---
title: Hashtable
date: '2016-10-11T17:18:11+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Hashtable
wordpress_id: 1601
layout: post
permalink: /wiki/hashtable/
render_with_liquid: false
---

## Hashtable

 Ein einfaches Beispiel einer Hashtable anhand einer Folderabfrage auf einem Mac: 

```
Get-ChildItem -Path $home | %{
    @{$_.Name=(Split-Path -Parent $_.Fullname)}
}
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
```

 Die Syntax ist @{Name=Value} 

```
@{$_.Name=(Split-Path -Parent $_.Fullname)}
```

## Hashtable mit Source- und Targetfolder

 Eine Hashtable mit Source- und Targetfolder abfüllen, danach kann ein Backup mit einer Schleife abgearbeitet werden: 

```
$targetroot = 'Z:'
$datahash   = [ordered]@{
    'S:\Scripting'    = "$($targetroot)\Backup\Scripting"
    'D:\Dokumente'    = "$($targetroot)\Backup\Dokumente"
    'W:\WebSites'     = "$($targetroot)\Backup\WebSites"
    'C:\Daten\Tools'  = "$($targetroot)\Backup\Tools"
    'F:\Fotografie'   = "$($targetroot)\Fotografie\Kataloge"
    'H:\HyperV'       = "$($targetroot)\Virtualisierung\HyperV"
}
foreach($item in $datahash.keys){
    if(Test-Path $targetroot){
        Write-Output "Source $($item), Target $($datahash[$item])"
    }
}
```