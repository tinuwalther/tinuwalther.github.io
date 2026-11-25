---
title: Reboot timestamp
date: '2015-02-16T15:19:58+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Reboot
wordpress_id: 655
layout: post
permalink: /wiki/reboot-timestamp/
render_with_liquid: false
---

Mit PowerShell und WMI den Zeitpunkt des letzten Reboots herauslesen:

## Mit PowerShell 2.0

 **Get-WmiObject** liefert kein DateTime-Object sondern einen LongDateString zurück, dieser muss noch in ein DateTime-Object umgewandelt werden. 

```csharp
[Management.ManagementDateTimeConverter]::ToDateTime((Get-WmiObject -Class `
Win32_OperatingSystem | Select-Object -Property LastBootupTime).LastBootupTime)
```

 Remoteabfrage 

```csharp
[Management.ManagementDateTimeConverter]::ToDateTime((Get-WmiObject -Class `
Win32_OperatingSystem -ComputerName $(read-host ("Enter Server name"))| `
Select-Object -Property LastBootupTime).LastBootupTime)

```

 Mit dem **WMI Accelerator \[wmi\]** kann direkt die Methode ConvertToDateTime aufgerufen werden. 

```csharp
([wmi]'').ConvertToDateTime((gwmi win32_operatingsystem).LastBootUpTime)
```

 Remoteabfrage 

```csharp
([wmi]'').ConvertToDateTime((gwmi win32_operatingsystem -ComputerName `
 $(read-host $("Enter Server name"))).LastBootUpTime)

```

## Ab PowerShell 3.0

 Lokal mit Get-CimInstance 

```csharp
(Get-CimInstance Win32_OperatingSystem).LastBootupTime

```

 Remoteabfrage 

```csharp
(Get-CimInstance Win32_OperatingSystem -ComputerName $(read-host `
("Enter Server name"))).LastBootupTime

```