---
title: PowerShell-Version
date: '2015-06-01T13:13:15+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Scripting
wordpress_id: 1198
layout: post
permalink: /wiki/powershell-version/
render_with_liquid: false
---

## PowerShell-Version

 Es ist immer wieder wichtig, zu wissen welche PowerShell- und .Net Framework Version auf dem Computer installiert ist. Diese kann man einfach mit folgendem Befehl auslesen: 

```
"PowerShell Version:`t$($PSVersionTable.PSVersion)` .Net Framework Version:`t$($PSVersionTable.CLRVersion)"
```

## OS-Versionen ↔ PowerShell Versionen

 Ab PowerShell 3.0 wird Windows Management Instrumentation 3.0 (WMI) benötigt. 

| **Windows Version** | **PowerShell** | **WMF¹** | **.NET²** | **Hinweis** |
|---|---|---|---|---|
| Windows Server 2003 |  - |  - |  - | End of Lifecycle, weg damit! |
| Windows Server 2008 | 1.0 |  | 2.0.50727 | default |
| Windows Server 2008 R2 | 2.0 | 3.0 | 4.0 | durch WMF 3 nachinstallierbar |
| Windows Server 2012 | 3.0 | 3.0 | 4.0 | default |
| Windows Server 2012 R2 | 4.0 | 4.0 | 4.5 | default, mit [DSC](/windows-configuration/) |
| Windows Server 2016 | 5.0 | 5.0 | 4.5 | [Whats new?](https://technet.microsoft.com/library/hh857339.aspx) |

 ¹) Windows Management Framework ²) .NET Framework Wird in der ersten Zeile des Scriptes #requires -version 3 eingesetzt, läuft das Script nur ab dieser PowerShell-Version durch. Hilfreich für jeden Administrator ist, wenn auf möglichst allen Windows Servern die selben PowerShell-, WMF- und .NET Framework-Versionen installiert sind. Bei SharePoint 2010 muss darauf geachtet werden, dass im IIS unter Application Pool Defaults das .NET Framework 3.5 ausgewählt ist. 

## PowerShell 5.1

 [Installationsanleitung WMF 5.1](https://msdn.microsoft.com/en-us/powershell/wmf/5.1/install-configure#)

## .NET Framework Versionen

| **.NET Framework version** | **CLR version** | **Windows Server** |
|---|---|---|
| .NET 4.7 | 4 | Windows Server 2008 R2 SP1, Windows Server 2012, Windows Server 2012 R2, Windows Server 2016 |
| .NET 4.6.2 | 4 | Windows Server 2008 R2 SP1, Windows Server 2012, Windows Server 2012 R2 |
| .NET 4.6.1 | 4 | Windows Server 2008 R2 SP1, Windows Server 2012, Windows Server 2012 R2 |
| .NET 4.5.2 | 4 | Windows Server 2008 R2 SP1, Windows Server 2008 Service Pack 2, Windows Server 2012, Windows Server 2012 R2 |
| .NET 4 | 4 | Windows Server 2003 Service Pack 2, Windows Server 2008, Windows Server 2008 R2, Windows Server 2008 R2 SP1 |
| .NET 3.5 | 2 | Windows Server 2003, Windows Server 2008 |