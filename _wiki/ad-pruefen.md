---
title: Active Directory prüfen
date: '2015-03-17T10:02:03+01:00'
author: Tinu
excerpt: ''
categories:
- Active Directory
tags:
- Active Directory
wordpress_id: 981
layout: post
permalink: /wiki/ad-pruefen/
render_with_liquid: false
---

Wenn ein DC promoted wurde, sollte dieser überprüft werden.

## Datenbank und Log

### SYSVOL-Folder anzeigen

 Im SYSVOL werden die Policies und Scripts domain-wide abgelegt. 

```csharp
ls (get-wmiobject -class win32_share -computer . | `
where-object {$_.Name -eq 'SYSVOL'}).Path |  ` 
select Name, FullName, Length, LastWriteTime, CreationTime | ft -auto
```

### Inhalt vom Folder NTDS auflisten

 ntds.dit ist die Active Directory Datenbank 

```csharp
$key = "hklm:\SYSTEM\CurrentControlSet\Services\NTDS\parameters"
ls (Get-ItemProperty $key).'Database log files path' |  `
select Name, FullName, Length, LastWriteTime, CreationTime | ft -auto

```

## Allgemeine DC Checks

```
dcdiag
```

## Replikations Checks

```
repadmin /showrepl
```

```
repadmin /replsummary
```

```
repadmin /syncall
```

## Active Directory Replication

```csharp
$dc = (read-host 'Enter DC name')
Get-ADReplicationFailure $dc
```

### Alle DCs einer Site

```csharp
$dc = (read-host 'Enter DC name')
Get-ADReplicationFailure -scope SITE -target $dc | FT Server, FirstFailureTime, `
FailureClount, LastError, Partner -AUTO
```

### Replication auf Attribute

```csharp
$dc = (read-host 'Enter DC name')
$domainDN = (Get-ADDomain).DistinguishedName
Get-ADReplicationAttributeMetadata -Object "CN=Domain Admins,CN=Users,$($domainDN)" `
-Server $dc -ShowAllLinkedValues | ft
```

### Inbound Replication vom Partner DC

```csharp
$dc = (read-host 'Enter DC name')
Get-ADReplicationPartnerMetadata -target $dc | Select LastChangeUsn, `
LastReplicationResult, LastReplicationSuccess, Partition, Server,  
PartnerType, PartnerAddress | ft -auto
```

### Replication in der Queue

```csharp
$dc = (read-host 'Enter DC name')
Get-ADReplicationQueueOperation -server $dc
```

### Domain Controller prüfen

```csharp
Get-EventLog -list | select Log
$logname = `(read-host 'Enter the Logname')`
Get-EventLog -LogName $logname -Newest 20 | ft -auto
```