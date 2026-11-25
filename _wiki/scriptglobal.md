---
title: Globale Variablen
date: '2014-11-26T19:35:50+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Scripttemplate
wordpress_id: 116
layout: post
permalink: /wiki/scriptglobal/
render_with_liquid: false
---

# Script-global-gültige Variablen

 Nachdem wir die Parameter deklariert haben, folgt nun die Deklaration und Initialisierung der script-global-gültigen Variablen. 

```
#region scriptglobals
$script:ScriptStart  = (get-date)
$script:Scriptpath   = Split-Path -Parent $MyInvocation.MyCommand.Path
$script:Scriptname   = $MyInvocation.MyCommand.ToString()
$script:Basename     = $script:Scriptname.Remove($script:Scriptname.Length -4)
$script:Logfile      = $($script:Scriptname).Replace('.ps1','.log')
$script:version      = '1.0.0.0000'
$script:Scriptreturn = @()
#endregion
```

 In jedem Script wird der Startzeitpunkt, der Scriptname, ev. ein Configfile, die Scriptversion und der Return vom Script an den Command Prompt benötigt. Die Scriptversion wird in der Notation Major.Minor.Build.Revision angegeben und bei jeder Änderung um 1 inkrementiert. 

```
PS D:\Dev> [version]'1.0.0.0000'

Major  Minor  Build  Revision
-----  -----  -----  --------
1      0      0      0       

```