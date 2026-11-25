---
title: Script Logging
date: '2014-11-26T19:40:02+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Logging
- Scripttemplate
wordpress_id: 120
layout: post
permalink: /wiki/logging/
render_with_liquid: false
---

# Jedes Script schreibt ein Log

 Entweder in ein Logfile oder in das Eventlog. Mit nachfolgender Möglichkeit wird in ein Logfile auf dem Computer geschrieben. 

```
<#
 [INFORMATION]
 [ WARNING ]
 [ ERROR ] 
#>

$script:Scriptpath = Split-Path -Parent $MyInvocation.MyCommand.Path
$script:Scriptname = $MyInvocation.MyCommand.ToString()
$script:Basename = $script:Scriptname.Remove($script:Scriptname.Length -4)
$script:Logpath = "C:\Admin\Logs\$($script:Basename)"
$script:Logfile = "$($script:Logpath)\$($script:Basename).log"

"$(Get-Date -DisplayHint DateTime) [INFORMATION] Start $($script:Scriptname)" | Out-File -FilePath $script:Logfile -Append -Encoding default
"$(Get-Date -DisplayHint DateTime) [  WARNING  ] Start $($script:Scriptname)" | Out-File -FilePath $script:Logfile -Append -Encoding default
"$(Get-Date -DisplayHint DateTime) [   ERROR   ] Start $($script:Scriptname)" | Out-File -FilePath $script:Logfile -Append -Encoding default

```