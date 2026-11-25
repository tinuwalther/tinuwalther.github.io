---
title: Remote logoff
date: '2015-02-16T17:56:41+01:00'
author: Tinu
excerpt: ''
categories:
- Windows Server
tags:
- Logoff
wordpress_id: 663
layout: post
permalink: /wiki/remote-logoff/
render_with_liquid: false
---

Mit PowerShell ein remote logoff, funktioniert aber nur auf einen (aktiven) User.

```csharp
(gwmi win32_operatingsystem -ComputerName 'Server').Win32Shutdown(4)
```

 Win32Shutdown Values: 0 – logoff 4 – forced logoff 1 – shutdown 5 – forced shutdown 2 – reboot 6 – forced reboot 8 – power off 12 – forced power off Angemeldete User auflisten und spezifischen User abmelden: 

```
quser /server:Server
logoff /server:Server /v Session-ID
```