---
title: Clear Download
date: '2016-08-30T06:50:31+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Folder
wordpress_id: 1554
layout: post
permalink: /wiki/clear-download/
render_with_liquid: false
---

## Temporäre Dateien aus dem Download löschen

```
<# Remove all PDF-Files older than 4 days #>
function Remove-PdfFiles{
    param($path)
    $function = $($MyInvocation.MyCommand.Name)
    $days = (Get-Date).AddDays(-4)
    Get-ChildItem -Include *.pdf -Path $path -Recurse | Where-Object LastWriteTime -lt $days | % {
        Write-Verbose "$(get-date -f 'yyyy-MM-dd HH:mm:ss') $($function)" -Verbose
        "$(get-date -f 'yyyy-MM-dd HH:mm:ss') Remove-Item $($_.FullName)" | Out-File -FilePath $Logfullname -Encoding default -Append
        Remove-Item -Path $_.FullName -Force 
    }
}

$Scriptpath  = Split-Path -Parent $MyInvocation.MyCommand.Path
$Logfilename = $(($MyInvocation.MyCommand.Name).Replace('ps1','log'))
$Logfullname = "$($Scriptpath)\$($Logfilename)"

Remove-PdfFiles 'C:\Users\<UserName>\Downloads'
```