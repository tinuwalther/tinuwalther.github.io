---
title: DHCP Server
date: '2015-03-13T12:17:37+01:00'
author: Tinu
excerpt: ''
categories:
- Windows Server
tags:
- DHCP Server
wordpress_id: 944
layout: post
permalink: /wiki/dhcp-server/
render_with_liquid: false
---

## DHCP Server Authorisierung

### Im Active Directory autorisierte DHCP Server auflisten

```csharp
$configurationNC = ([adsi]"LDAP://rootdse").ConfigurationNamingContext
Get-ADObject -SearchBase $($configurationNC) -Filter "objectclass -eq 'dhcpclass' `
 -AND Name -ne 'dhcproot'" | Select Name

```

### Add Server to Authorized servers

```
netsh dhcp add server dhcpsrv1.example.microsoft.com 10.2.2.2
```

#### Windows PowerShell 4.0

 Wird das Cmdlet ohne Parameter ausgeführt, so wird der lokale Server im AD autorisiert. Die IP Adresse wird automatisch mit einem Nslookup ermittelt. 

```csharp
Add-DhcpServerInDC -DnsName dhcpserver.contoso.com -IPAddress 10.10.10.2
```

### Remove Server from Authorization

```
netsh dhcp delete server dhcpsrv1.example.microsoft.com 10.2.2.2
```

#### Windows PowerShell 4.0

 Wird das Cmdlet ohne Parameter ausgeführt, so wird der lokale Server aus der AD-Autorisierung gelöscht. Die IP Adresse wird automatisch mit einem Nslookup ermittelt. 

```csharp
Remove-DhcpServerInDC -DnsName dhcpserver.contoso.com -IPAddress 10.10.10.2
```