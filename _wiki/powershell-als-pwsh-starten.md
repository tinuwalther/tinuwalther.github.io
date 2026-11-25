---
title: PowerShell als pwsh starten
date: '2024-05-30T11:39:11+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- PowerShell
image: /assets/wiki/powershell-1.png
wordpress_id: 4086
layout: post
permalink: /wiki/powershell-als-pwsh-starten/
render_with_liquid: false
---

Aus einem Terminal kann die PowerShell 7 mit Parameters folgenderweise gestartet werden:

## Code

```powershell
pwsh.exe -command {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true, Position = 0)]
        [String] $MyName,
		
	[Parameter(Mandatory=$true, Position = 1)]
        [String] $Language
    )
    Write-Host ('I am {0} an I love {1} {2}' -f $MyName, $Language, $PSVersionTable.PSVersion.ToString()) -ForegroundColor Green
} -args 'Tinu','PowerShell'

```

## Output

```
I am Tinu an I love PowerShell 7.4.2

```

