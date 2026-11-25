---
title: DHCP Scopes
date: '2015-03-13T12:18:11+01:00'
author: Tinu
excerpt: ''
categories:
- Windows Server
tags:
- DHCP Server
wordpress_id: 946
layout: post
permalink: /wiki/dhcp-scopes/
render_with_liquid: false
---

### Scope erstellen

```csharp
$name = 'Lab 1'
$start = '10.10.10.1'
$end = '10.10.10.254'
$subnet = '255.255.255.0'
Add-DhcpServerv4Scope -Name $name -StartRange $start -EndRange $end -SubnetMask $subnet

```

### Scope Exportbeispiel

```
netsh dhcp server "\\$($dhcpserver)" v4 export "c:\$($dhcpserver)-scopes.txt" all
```

 Wird im nachfolgenden Beispiel kein Scope angegeben, so werden alle Scopes exportiert. 

```csharp
$dhcpserver = (read-host 'Enter Server name')
$scope = @('10.10.10.0','20.20.20.0')
$file = "C:\temp\$($dhcpserver)-dhcpexport.xml"
Export-DhcpServer -ComputerName $dhcpserver -File $file -ScopeId $scope -Leases

```

### Scopes aus Export-XML auslesen

```csharp
$file = "C:\temp\$($dhcpserver)-dhcpexport.xml"
[xml]$a = gc $file
$a.DHCPServer.IPv4.Scopes.scope.Leases.Lease | select ScopeId, IPAddress, HostName, `
AddressState, LeaseExpiryTime, DnsRR, DnsRegistration, NapStatus | ft -auto

```

### Scope Importbeispiele

```
netsh dhcp server "\\$($dhcpserver)" v4 import "c:\$($dhcpserver)-scopes.txt" all
```

 Wird im nachfolgenden Beispiel kein Scope angegeben, so werden alle Scopes importiert. 

```csharp
$dhcpserver = (read-host 'Enter Server name')
$scope = @('10.10.10.0','20.20.20.0')
$file = "C:\temp\$($dhcpserver)-dhcpexport.xml"
$backup = 'C:\temp\dhcpbackup\'
Import-DhcpServer -ComputerName $dhcpserver -File $file -BackupPath $backup `
-ScopeId $scope -Leases -ScopeOverwrite

```

### Scope löschen

 Nach dem erfolgreichen Import muss der migrierte Scope auf dem alten DHCP Server gelöscht werden. 

```
netsh dhcp server delete scope 192.168.1.0 DHCPFULLFORCE
```

### Scopes auslesen

```csharp
$dhcpserver = (read-host 'Enter Server name')
Get-DhcpServerv4Scope -ComputerName $dhcpserver | ft -auto

```