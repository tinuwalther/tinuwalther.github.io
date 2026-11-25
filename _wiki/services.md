---
title: Services
date: '2014-11-26T20:41:24+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Remote Commands
- Services
wordpress_id: 142
layout: post
permalink: /wiki/services/
render_with_liquid: false
---

## Local Services

### Alle Services auflisten

```csharp
Get-Service
```

### Alle Services mit McAfee im DisplayName auflisten

```csharp
Get-CimInstance -Class win32_service -Filter "DisplayName LIKE '%McAfee%'"
```

### Alle Services mit StartMode Automatic auflisten

```csharp
Get-WmiObject Win32_Service | Where-Object {$_.StartMode -eq 'Automatic'}
```

### Alle gestoppten Services mit StartMode Automatic auflisten

```csharp
Get-WmiObject Win32_Service | Select Name, State, StartMode, Started | `
 where StartMode -eq 'Auto' | where State -eq 'Stopped' | ft -auto
```

### Service starten

```csharp
Start-Service netlogon
```

### Service stoppen

```csharp
Stop-Service netlogon
```

### Service Restarten

```csharp
Restart-Service netlogon
```

### Service Startup Type ändern

```
Set-Service w32time -startuptype "Manual" | "Automatic" | "Disabled"
```

## Remote Services

### Einen bestimmten Service auflisten

```csharp
$svc = 'winrm'
$srv = @('Server01', 'Server02')
Get-Service -name $svc -computername $serv | Select Name, State, StartMode, Started
```

### Alle gestoppten Services mit StartMode Automatic auflisten

```csharp
$computer = (read-host ("Enter Server name"))
Get-WmiObject -Computer $computer win32_service -filter "startmode='auto' AND `
state<>'Running'" | Select SystemName, Name, DisplayName, State, StartMode, Started,`
StartName, PathName | ft -auto

```

### Service remote restarten

```
$computer = (read-host ("Enter Server name"))
$service = (read-host ("Enter Service name")) invoke-command {restart-service $service} -computer $computer
```

### Service remote stoppen

```
$computer = (read-host ("Enter Server name"))
$service = (read-host ("Enter Service name")) invoke-command {stop-service $service} -computer $computer
```

### Service remote starten

```
$computer = (read-host ("Enter Server name"))
$service = (read-host ("Enter Service name")) invoke-command {start-service $service} -computer $computer
```