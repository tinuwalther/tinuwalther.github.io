---
title: BGinfo
date: '2016-10-03T20:12:16+02:00'
author: Tinu
excerpt: ''
categories:
- Allgemein
- Windows Server
tags:
- BGinfo
wordpress_id: 1594
layout: post
permalink: /wiki/bginfo/
render_with_liquid: false
---

BGInfo.exe von Sysinternals starten und mit den gewünschten Daten konfigurieren.

## Konfigurationsfile

```
Host Name:       <Host Name>
Logon Domain:    <Logon Domain>

IP Address:      <IP Address>
Subnet Mask:     <Subnet Mask>
Default Gateway: <Default Gateway>
DNS Server:      <DNS Server>

CPU:             <CPU>
Memory:          <Memory>

OS Version:      <OS Version>
Service Pack:    <Service Pack>
```

## Autostart einrichten

 Registry key erstellen 

```
$path  = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
$name  = 'StartBgInfo'
$value = 'C:\Admin\Tools\BGInfo\bginfo.exe C:\Admin\Tools\BGInfo\Screen.bgi /timer:0'
Set-ItemProperty -Path $path -Name $name -Value $value -PassThru
```