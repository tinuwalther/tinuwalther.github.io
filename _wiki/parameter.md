---
title: Parameter
date: '2014-11-26T19:24:15+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Scripttemplate
wordpress_id: 105
layout: post
permalink: /wiki/parameter/
render_with_liquid: false
---

# Übergabeparameter

 Nach dem Header im Script folgen die Übergabeparameter, welche im Header ja angegeben/beschrieben werden. 

```
#region param
[CmdletBinding()]
param (
   [Parameter(Mandatory=$true)][String] $XmlFile,
   [Parameter(Mandatory=$true)][int] $ScriptCount = 0,
   [Parameter(Mandatory=$false)][switch]$psdebug = $false
)
#endregion
```

 Nach jedem (ausser dem letzten) Parameter wird die Zeile mit einem Komma abgetrennt. Die Parameter können bereits hier bei der Deklaration mit Default Values abgefüllt werden ($ScriptCount = 0, $psdebug = $false). 

## Hilfe Text zu Parameter

 Ein kleine Hilfetext für den Nutzer ist oft hilfreich: 

```
#region param
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, HelpMessage = 'Enter json or csv as output format.')]
    [String]$format = '',
    [Parameter(Mandatory = $false, HelpMessage = 'Write debug information to the console.')]
    [switch]$psdebug = $false
)
#endregion
```

## ValidateSet

 Oder gleich die Möglichkeiten der Werte definieren, welche eingegeben werden können: 

```
#region param
[CmdletBinding()]
param(
    [ValidateSet('Bern','Zürich','Chur','Lugano')]
    [Parameter(Mandatory = $true)][String] $City = '', 
)
#endregion
```

## CmdletBinding

 Wozu eigentlich dient \[CmdletBinding()\] eigentlich? Damit können die [Common Parameters](https://technet.microsoft.com/de-DE/library/dd315352.aspx) benutzt werden, diese werden von Windows PowerShell implementiert, und sind für jedes Cmdlet automatisch verfügbar. Die gängigsten Parameter sind folgende: -Verbose -Debug -WarningAction -WarningVariable -ErrorAction -ErrorVariable -OutVariable -OutBuffer -WhatIf -Confirm