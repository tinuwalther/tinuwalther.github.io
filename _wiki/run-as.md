---
title: Run as
date: '2018-12-29T11:38:06+01:00'
author: Tinu
excerpt: Eine PowerShell als Administrator starten.
categories:
- PowerShell
tags:
- RunAs
image: /assets/wiki/powershell-1.png
wordpress_id: 2538
layout: post
permalink: /wiki/run-as/
render_with_liquid: false
---

## Run PowerShell as Administrator

Eine PowerShell als User starten und folgenden Befehl eingeben:

```
Start-Process "$psHome\powershell.exe" -Verb Runas -Wait 
```

Damit wird ein neuer Prozess mit einer PowerShell als Administrator gestartet.

## Run PowerShell as System

Mit dem ersten Befehl eine neue PowerShell als Administrator starten, zum Pfad von PsExec navigieren und den Befehl eingeben:

```
psexec.exe -i -s powershell.exe
```

*PsExec is a tool written by Mark Russinovich (included in the Sysinternals Suite) and can downloaded* [*here*](https://technet.microsoft.com/en-us/sysinternals/bb897553.aspx)*.*