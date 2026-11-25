---
title: OS Version
date: '2015-02-18T14:25:22+01:00'
author: Tinu
excerpt: ''
categories:
- Windows Server
tags:
- Windows Server
wordpress_id: 723
layout: post
permalink: /wiki/os-version/
render_with_liquid: false
---

## Win32\_OperatingSystem

### OS Version

 OS Version auf einem Computer auslesen: 

```
$computer = (read-host ("Enter Server name"))
(Get-WmiObject -Computer $computer -Class Win32_OperatingSystem).caption
```

 oder mit 

```
Get-WmiObject -Computer $computer -Class Win32_OperatingSystem | select -Property Version
```

### Service Pack

 Service Pack auf einem Computer auslesen: 

```
(Get-WmiObject -Computer $computer -Class Win32_OperatingSystem).CSDVersion
```

 oder mit 

```
Get-WmiObject -Computer $computer -Class Win32_OperatingSystem | select -Property ServicePack*
```

### Weitere interessante Properties

- InstallDate
- LastBootUpTime
- LocalDateTime
- FreePhysicalMemory
- FreeSpaceInPagingFiles
- FreeVirtualMemory