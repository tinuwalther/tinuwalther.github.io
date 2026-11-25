---
title: PowerShell starten
date: '2016-06-14T18:18:27+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Scripting
wordpress_id: 1463
layout: post
permalink: /wiki/powershell-starten/
render_with_liquid: false
---

## PowerShell von ausserhalb starten

```
PowerShell.exe -NoExit -File C:\Scripts\Get-MemoryUsage.ps1
```

### Script

```
<#
     .SYNOPSIS
         Calculates the total memory usage
     .SYNTAX
         Get-MemoryUsage.ps1 -property 'PrivateMemorySize64'
     .PARAMETERS property
         One of the following propertes:
             NonpagedSystemMemorySize64
             PagedMemorySize64
             PagedSystemMemorySize64
             PeakPagedMemorySize64
             PeakWorkingSet64
             PeakVirtualMemorySize64
             PrivateMemorySize64
             VirtualMemorySize64
             WorkingSet64
      .DESCRIPTION
         Calculates the total memory usage
     .REMARKS
         Do enything
     .NOTES
         Author: Martin Walther
#>
function Get-TotalMemoryUsage{
    param(
        [Parameter(Mandatory=$true)][String]$property=''
    )
    $function = $($MyInvocation.MyCommand.Name)
    try
    {
        $proc = Get-Process | Select $property
        $sum  = $proc | Measure-Object -Property $property -Sum 
        [PSCustomObject]@{
            "Total$($property)GB" = $([math]::Round(($sum).Sum/1gb,3))
            TotalRunningProcesses = $($sum.Count)
        }
    }
    catch [Exception]
    {
        write-host "$($function): $($_.Exception.Message)" -ForegroundColor Red
        $error.clear()
    }
    return
}
return Get-TotalMemoryUsage -property 'PrivateMemorySize64'
```