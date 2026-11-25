---
title: Memory Usage
date: '2016-03-23T16:44:38+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Memory
wordpress_id: 1445
layout: post
permalink: /wiki/memory/
render_with_liquid: false
---

## Installiertes physical Memory ausgeben

```
(Get-WmiObject -Class Win32_PhysicalMemory | `
Measure-Object -Property Capacity -Sum).Sum/1mb
```

## Aktuell benutztes Memory Ausgeben

```
Get-Process | Select ProcessName,id,PrivateMemorySize64,WorkingSet64,PriorityClass,TotalProcessorTime,Product,Path | out-gridview
```

oder gleich berechnen lassen

```
$ret = Get-Process | Select ProcessName,id,PrivateMemorySize64,WorkingSet64 $ret | Sort-object PrivateMemorySize64 | Format-Table -AutoSize
$ret = $ret | Measure-Object -Property PrivateMemorySize64 -Sum $procarray = "$([math]::Round(($ret).Sum/1mb,2))","$($ret.Count)" "-" * 80
"Total processes running {1}, Total PrivateMemory in use {0} MB" -f $procarray; "-" * 80
```

## Top Memory Killers

```

function Get-TopMemoryKillers{
[CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [Int] $count
    )
    $function = $($MyInvocation.MyCommand.Name)
    Write-Verbose "Running $function"
    #cls

    "-" * 80
    Write-Host "THE TOP $count MEMORY KILLER ON COMPUTER $($env:COMPUTERNAME) (ASCENDING ORDER):" -ForegroundColor Yellow
    "-" * 80

    $ram = (Get-WmiObject -Class Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum).Sum/1mb

    $ret = Get-Process | Select ProcessName,id,PrivateMemorySize64,WorkingSet64,Product
    $ret | Sort-object PrivateMemorySize64 | select -Last $count | Format-Table -AutoSize
    #$ret | Sort-object WorkingSet64 | select -Last $count | Format-Table -AutoSize

    $ret = $ret | Measure-Object -Property PrivateMemorySize64 -Sum
    #$ret = $ret | Measure-Object -Property WorkingSet64 -Sum

    $usage = ([math]::Round(($ret).Sum/1mb,2))

    "-" * 80
    Write-Host "Total memory installed $($ram) MB, Total PrivateMemory in use $($usage) MB"
    "-" * 80

    if($ram -le ([math]::Round(($ret).Sum/1mb,2))){
        Write-Host "Please increase the Memory on the VM, this VM use more Memory than installed!" -ForegroundColor White -BackgroundColor Red
        "-" * 80
   }

}

function Get-CpuLoad{
[CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [Int] $count
    )
    $function = $($MyInvocation.MyCommand.Name)
    Write-Verbose "Running $function"

    "-" * 80
    Write-Host "THE TOP $count CPU KILLER ON COMPUTER $($env:COMPUTERNAME) (ASCENDING ORDER):" -ForegroundColor Yellow
    "-" * 80

    Get-WmiObject win32_processor | ForEach {
        [PSCustomObject]@{
            Name           = $($_.Name)
            Socket         = $($_.SocketDesignation)
            LoadPercentage = $($_.LoadPercentage)
        }
    }

    Get-Counter -ComputerName localhost '\Process(*)\% Processor Time' `
        | Select-Object -ExpandProperty countersamples `
        | Select-Object -Property instancename, cookedvalue `
        | Sort-Object -Property cookedvalue -Descending | Select-Object -First $count `
        | ft InstanceName,@{L='CPU usage';E={($_.Cookedvalue/100).toString('P')}} -ErrorAction SilentlyContinue

}

Get-TopMemoryKillers -count 10
"`n"
Get-CpuLoad -count 5

```

