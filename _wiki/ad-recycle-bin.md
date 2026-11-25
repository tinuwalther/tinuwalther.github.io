---
title: Active Directory Recycle Bin
date: '2015-03-13T19:10:32+01:00'
author: Tinu
excerpt: ''
categories:
- Active Directory
tags:
- Papierkorb
- Recycle Bin
wordpress_id: 966
layout: post
permalink: /wiki/ad-recycle-bin/
render_with_liquid: false
---

Ab Forest Functional Level 2008 R2 kann der AD Recycle Bin aktiviert und genutzt werden. Die Aktivierung sollte auf dem Domain Naming Master als Enterprise Admin durchgeführt werden.

## Status abfragen

```csharp
Get-ADOptionalFeature 'Recycle Bin Feature'
```

## Aktivieren

```csharp
$domaindns = (Get-ADDomain | Select DNSRoot).DNSRoot
$configurationNC = ([adsi]"LDAP://rootdse").ConfigurationNamingContext
$dirServices = "CN=Directory Service,CN=Windows NT,CN=Services,$($configurationNC)"
$recycleBin = "CN=Recycle Bin Feature,CN=Optional Features,$($dirServices)"
Enable-ADOptionalFeature –Identity $recycleBin –Scope ForestOrConfigurationSet `
–Target $domaindns
```

## Gelöschtes Objekt wiederherstellen

### Object Lifecycle

 Live object **→** Deleted object (restorable) **→** Recycled object (tombstone) **→** physically deleted **Deleted object** Das Objekt ist in den Container "Deleted objects" verschoben, all seine Attribute sind gegenüber Windows 2003/2008 noch vorhanden (z.B. Groupmembership). Das Objekt ist nicht mehr aktiv, ein User kann sich z.B. nicht mehr anmelden. Das Objekt kann über den AD Recycle Bin wiederhergestellt werden. Deleted object lifetime = msDS-deletedObjectLifetime, neu seit Windows Server 2008 R2, default value =180 **Recycled object** Die "Deleted object lifetime" des gelöschten Objekts ist abgelaufen und die meisten seiner Attribute sind entfernt. Das Objekt kann nicht mehr aus dem AD Recycle Bin wiederhergestellt werden. Auch andere Verfahren wie "tombstone reanimation" können das Objekt nicht mehr wiederherstellen. Tombestone Lifetime = tombstoneLifetime, existiert seit Windows 2000, default value = 60 Ist das Attribut nicht gesetzt, so wurde der erste DC mit einer älteren Version als Windows 2003 SP1 installiert. Ab Windows 2003 SP1 wird das Attribut mit dem default value von 180 gesetzt. **Physically deleted** Der Active Directory Garbage Collection Prozess hat das Objekt endgültig aus dem Active Directory gelöscht. **Einzelnen User restoren**

```csharp
Get-ADObject -Filter {displayName -eq "Mary"} `
-IncludeDeletedObjects | Restore-ADObject
```

 **OU restoren**

```csharp
Get-ADObject -ldapFilter:"(msDS-LastKnownRDN=Finance_Department)" `
–IncludeDeletedObjects | Restore-ADObject
```