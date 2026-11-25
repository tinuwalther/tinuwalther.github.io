---
title: Python Help like PowerShell Help
date: '2021-04-12T19:25:07+02:00'
author: Tinu
excerpt: Gibt es eine Comment-Based Help wie mit PowerShell für Python? Ich habe mir
  eine Function dafür geschrieben.
categories:
- Python
tags:
- Programmieren
- Python
- Scripting
image: /assets/wiki/python3-e1619608143693.png
wordpress_id: 2735
layout: post
permalink: /wiki/python-help-like-powershell-help/
render_with_liquid: false
---

# Comment-Based Help

Scripts sollten vollständig dokumentiert sein, bevor sie ausgeliefert werden. Dazu gehört eine kurze verständliche Hilfestellung die aufgerufen werden kann.

## PowerShell Help

Wird in der PowerShell-Function mit der Synopsis gearbeitet, kann mit `Get-Help <Commandlet> -Detailed` folgende Hilfe aufgerufen werden:

```powershell
Get-Help Test-PsNetPing -Detailed

NAME
    Test-PsNetPing
    
SYNOPSIS
    Test ICMP echo
    
SYNTAX
    Test-PsNetPing [-Destination] <String[]> [[-try] <Int32>] [<CommonParameters>]
    
DESCRIPTION
    Attempts to send an ICMP echo message to a remote computer and receive a corresponding 
    ICMP echo reply message from the remote computer.
    
PARAMETERS
    -Destination <String[]>
        A String or an Array of Strings with Names or IP Addresses to test <string>
        
    -try <Int32>
        Number of attempts to send ICMP echo message
        
    <CommonParameters>
        This cmdlet supports the common parameters: Verbose, Debug,
        ErrorAction, ErrorVariable, WarningAction, WarningVariable,
        OutBuffer, PipelineVariable, and OutVariable. For more information, see
        about_CommonParameters (https://go.microsoft.com/fwlink/?LinkID=113216). 
    
    -------------------------- EXAMPLE 1 --------------------------
    
    PS > Test-PsNetPing -Destination sbb.ch

```

## Python Help

Diese Comment-Based Help gibt es in Python nicht (oder ich habe sie auf jeden Fall nicht gefunden). Aus diesem Grund habe ich eine Python-Function geschrieben, welche ich in jedem Programm verwenden kann und somit eine Comment-Based Help wie in PowerShell zur Verfügung habe. Die Function ist in meinem [GitHub Profile](https://github.com/tinuwalther/learningPython/blob/main/Functions/help.py) abgelegt.

```powershell
NAME
    py-sender.py

SYNOPSIS
    Send a message to the listener

SYNTAX
    python3 /Users/Tinu/git/github.com/docker-example/pyhost/py-sender.py -l address -m message

DESCRIPTION
    Send a message to the listener, the listener run a command based on the message

PARAMETERS
    -l listener name or ip address

PARAMETERS
    -m keyword of the message to send: srf, wetter or covid are active

    -------------------------- EXAMPLE 1 --------------------------

    python3 /Users/Tinu/git/github.com/docker-example/pyhost/py-sender.py -l pyhost1 -m wetter

```

