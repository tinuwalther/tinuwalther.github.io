---
title: Firewallport prüfen
date: '2015-01-13T12:30:24+01:00'
author: Tinu
excerpt: Eine Verbindung zwischen zwei Computern zu prüfen, kann zu einem long-time
  Task führen. In diesem Beitrag wird dies zu einem short-time Task.
categories:
- PowerShell
tags:
- Firewall
- Netstat
- Netzwerk
image: /assets/wiki/firewall-e1620744165429.png
wordpress_id: 540
layout: post
permalink: /wiki/tcp-connection/
render_with_liquid: false
---

## Connection über Port prüfen

Als erster Task prüfen wir vom Source Computer aus die Connectivity zum Target Computer über den gewünschten TCP Port.

```
Test-NetConnection www.sbb.ch -Port 80

ComputerName     : www.sbb.ch
RemoteAddress    : w.x.y.z
RemotePort       : 80
InterfaceAlias   : WLAN
SourceAddress    : w.x.y.z
TcpTestSucceeded : True
```

## Listener prüfen

Wenn TcpTestSucceeded False zurückgibt, dann ist häufig einfach kein Listener auf dem Taget Computer gestartet. Dies kann entweder wie vor urzeiten mit netstat oder wie es jeder PS Enthusiast macht, mit Get-NetTCPConnection geprüft werden.

### Netstat

```
netstat -ano | findstr /I "5985"

  Proto  Local Address          Foreign Address        State           PID
  TCP    0.0.0.0:5985           0.0.0.0:0              LISTENING       4
  TCP    [::]:5985              [::]:0                 LISTENING       4
```

### PowerShell

```
$port = (read-host ("Enter TCP-Port (*)"))
Get-NetTCPConnection | Where LocalPort -like $port | ft –auto

LocalAddress LocalPort RemoteAddress RemotePort State       AppliedSetting
------------ --------- ------------- ---------- -----       --------------
127.0.0.1    49273     127.0.0.1     808        Established Datacenter
0.0.0.0      49216     0.0.0.0       0          Listen
0.0.0.0      49215     0.0.0.0       0          Listen
```

## Local Firewall prüfen

Wenn ein Listener auf dem Target Computer gestartet ist und funktioniert, dann kann es noch an der lokalen Firewall liegen. Mit diesem Command kann geprüft werden, ob eine Firewall Rule den Port in der gewünschten Richtung auch zulässt.

```
$Port = @(443, 5985, 3389)
$fw = foreach($item in $Port){ 
    Get-NetFirewallPortFilter | Where LocalPort -eq $item | Get-NetFirewallRule 
}
$fw | Select Name,DisplayName,Description,Enabled,Profile,Direction,Action,PrimaryStatus
```

