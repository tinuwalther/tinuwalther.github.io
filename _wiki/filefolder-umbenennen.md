---
title: File/Folder umbenennen
date: '2016-02-10T13:25:57+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Scripting
wordpress_id: 1432
layout: post
permalink: /wiki/filefolder-umbenennen/
render_with_liquid: false
---

## Mehrere Files/Folder umbenennen

```
Get-ChildItem | %{Rename-Item -Path $_.FullName -NewName "Prefix_$($_.Name)"}
```

```
$searchstr  = 'old'
$replacestr = 'new'
$entrydir   = 'Z:\06_Puppet\sciiswebadministration'
gci $entrydir -Recurse | Where Name -Like -Value $searchstr | % {
    $newname = $_.name.replace($searchstr, $replacestr)
    Rename-Item $_.fullname $newname
}
```

## Ausdruck in mehrerern Files ersetzten

```
$searchstr  = 'old'
$replacestr = 'new'
$entrydir   = 'Z:\Temp'

gci $entrydir -Recurse | % {
    if(!($_.PsIsContainer))
    {
        if(gc -Path $_.FullName | Select-String -Pattern $searchstr)        
        {
            "$($searchstr) -> $($_.FullName)"
            (gc $_.FullName) -replace $searchstr, $replacestr | sc $_.FullName
        }
    }
}
```