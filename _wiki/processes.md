---
title: Memory Usage eines Prozesses
date: '2016-02-09T11:00:10+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Memory
- Processes
wordpress_id: 1428
layout: post
permalink: /wiki/processes/
render_with_liquid: false
---

## Memory Usage eines Prozesses auflisten

Mit folgenem Code kann z.B. abgefragt werden wie viel RAM die eigenen Tools benötigen, dazu werden die einzelnen Prozesse in ein Array geschrieben und in einer ForEach-Schleife abgearbeitet. 

```
$process = Read-Host 'Enter the Process name to search' # $process = @('sqlserver')
Get-Process | Where-Object -Property ProcessName -Like -Value $process | ForEach-Object -Process {
    [PSCustomObject]@{
        'Process Name'   = $_.ProcessName
        'Process Id'     = $_.id
        'StartTime'      = $_.StartTime
        'Commit (KB)'    = [math]::Round(($_.PrivateMemorySize)/1kb)
        'Working Set (KB)' = [math]::Round(($_.WorkingSet)/1kb)
    }
} |
Sort-Object -Property  'Commit (KB)' | Format-Table -AutoSize

Get-Process | Select ProcessName,id,PrivateMemorySize,WorkingSet | out-gridview
```