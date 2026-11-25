---
title: DHCP Server abfragen
date: '2015-03-18T10:10:35+01:00'
author: Tinu
excerpt: ''
categories:
- Windows Server
tags:
- DHCP Server
wordpress_id: 989
layout: post
permalink: /wiki/dhcp-server-abfragen/
render_with_liquid: false
---

### DHCP Server Version

```csharp
$dhcpserver = (read-host 'Enter Server name')
Get-DhcpServerVersion -ComputerName $dhcpserver

```

### DHCP Server Audit Log

```csharp
$dhcpserver = (read-host 'Enter Server name')
Get-DhcpServerAuditLog -ComputerName $dhcpserver | ft -auto

```

### DHCP Server Failoverkonfiguration

```csharp
$dhcpserver = (read-host 'Enter Server name')
Get-DhcpServerv4Failover -ComputerName $dhcpserver | ft -auto

```

### DHCP Server Scopes

```csharp
$dhcpserver = (read-host 'Enter Server name')
Get-DhcpServerv4Scope -ComputerName $dhcpserver | ft -auto
```

### DHCP Server Options

```csharp
$dhcpserver = (read-host 'Enter Server name')
Get-DhcpServerv4OptionValue -ComputerName dhcpserver -OptionId 6,42,66 `
-ea SilentlyContinue | select OptionId,Name,Type,Value | ft -auto
```

### DHCP Server Scope Options

```csharp
$dhcpserver = (read-host 'Enter Server name')
Get-DhcpServerv4OptionValue -ComputerName dhcpserver -ScopeId 10.10.10.0 `
-OptionId 6,42,66 -ea SilentlyContinue | select OptionId,Name,Type,Value | ft -auto
```