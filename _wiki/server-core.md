---
title: Windows Server Core
date: '2015-03-26T12:04:02+01:00'
author: Tinu
excerpt: ''
categories:
- Windows Server
tags:
- Windows Server
wordpress_id: 1065
layout: post
permalink: /wiki/server-core/
render_with_liquid: false
---

## Benutzer abfragen

 Listet den Benutzer auf. 

```
net user <username>
```

## Passwort eines Benutzers ändern

 Password eines Benutzers ändern mit Abfrage nach dem Passwort (\*"). 

```
net user <username> *"
```

## Installierte Software abfragen

 Installierte Software auf Server Core oder auch auf Remote Computern können mit WMI abgefragt und aufgelistet werden. 

```csharp
$computer = read-host ('Enter Computer name')
Get-WmiObject -Class Win32_Product -ComputerName $computer | Select Name, Version, `
Description, InstallDate, PackageName, Vendor | sort Name | ft -auto
```