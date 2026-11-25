---
title: Remote Commands
date: '2014-12-23T10:53:39+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- PSObject
- Remote Commands
wordpress_id: 510
layout: post
permalink: /wiki/remote-commands/
render_with_liquid: false
---

Ab PowerShell 3.0

## Remote Commands auf Servern ausführen

 Als ersetes wird ein Array mit den Servernamen (oder deren IPs) abgefüllt. Danach wird das Array in einer Schleife abgearbeitet. Mit invoke-command -ComputerName $($\_) -scriptblock{} wird der der Scriptblock remote auf dem Server abgesetzt und der Rückgabewert in die Variable $retinvoke abgespeichert. 

```csharp
$serverlist = @("Server1","Server2","Server3")
$ret = @()
$serverlist | % {
    $invoke = invoke-command -ComputerName $($_) -scriptblock {
        gci -path "C:\" -filter "BI*" | select fullname |%{$_.fullname}
    }
    $obj = New-Object PSObject
    Add-Member -InputObject $obj -MemberType NoteProperty -Name Computer -Value $($_)
    Add-Member -InputObject $obj -MemberType NoteProperty -Name Path -Value $invoke
    $ret += $obj
}
$ret | ft -auto -wrap | Out-String
```