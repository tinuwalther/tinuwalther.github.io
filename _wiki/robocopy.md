---
title: Robocopy
date: '2015-07-06T13:31:20+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
wordpress_id: 1278
layout: post
permalink: /wiki/robocopy/
render_with_liquid: false
---

## Standard Robocopy

 Anzahl Files, Directories, Bytes anzeigen 

```
$srcdir = ""
$dstdir = ""
robocopy $($srcdir) $($dstdir) /E /R:0 /W:0 /NJH /NP /NFL /NDL /L
```

### Standard Ausgabe

```
 Total Copied Skipped Mismatch FAILED Extras
 Dirs : 2 1 1 0 0 50
 Files : 26 26 0 0 0 28
 Bytes : 173.11 m 173.11 m 0 0 0 124.70 m
 Times : 0:00:00 0:00:00 0:00:00 0:00:00

 Ended : Fri Jul 10 15:05:25 2015
```

## Robocopy Ausgabe formatieren

```
function Copy-Data
{
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][String] $source,
        [Parameter(Mandatory=$true)][String] $target
    )
    $obj = $null
    $result = robocopy $source $target /S /R:1 /W:1 /NDL /NS
    if(-not([string]::IsNullOrEmpty($result )))
    {
        $summary = (($result -match 'Files:' -replace '\s+','@').TrimStart('@Files:@') -split '@')
        $obj = New-Object PSObject
        $obj | Add-Member NoteProperty Total    $summary[0]
        $obj | Add-Member NoteProperty Copied   $summary[1]
        $obj | Add-Member NoteProperty Skipped  $summary[2]
        $obj | Add-Member NoteProperty Mismatch $summary[3]
        $obj | Add-Member NoteProperty FAILED   $summary[4]
        $obj | Add-Member NoteProperty Extras   $summary[5]
    }
    return $obj 
}
```

### Formatierte Ausgabe

```
Total Copied Skipped Mismatch FAILED Extras
----- ------ ------- -------- ------ ------
14308 0      14308   0        0      8
```

## Options

```
/S   = excl. empty
/E   = incl. empty
/R   = Retry count
/W   = Wait count for Retry
/NP  = no percent
/NS  = no size
/NJH = no job header
/NDL = no directory list
/NFL = no file list
/L   = List only - do not copy anything
```

 Zum Kopieren einfach /L weglassen. Mehr Optionen siehe [Command line reference](https://ss64.com/nt/robocopy.html).