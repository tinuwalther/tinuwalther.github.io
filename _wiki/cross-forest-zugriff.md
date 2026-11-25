---
title: Cross-Forest Zugriff
date: '2014-12-01T23:13:38+01:00'
author: Tinu
excerpt: ''
categories:
- Active Directory
tags:
- Active Directory
wordpress_id: 393
layout: post
permalink: /wiki/cross-forest-zugriff/
render_with_liquid: false
---

# Account- und Resource Domain

![cross-forest](/assets/wiki/cross-forest.jpg)Copyright (c) 2014 Martin Walther 

## Trust verifizieren

```
Get-ADObject -Filter {objectClass -eq "trustedDomain"} -Properties TrustPartner,TrustDirection,trustType | FT Name,TrustPartner,TrustDirection,TrustType
```

## Der Mythos mit den Gruppen und Berechtigungen

Ausgehend von einem Domainfunctional Level Windows 2000 native oder Windows Server 2003 oder höher. 

### Global Group

![Global-Group](/assets/wiki/Global-Group.jpg)Grösse: 8 Bytes **MemberOf:**Accounts und Global Groups aus der eigenen Domain. **Permission to:**auf Ressourcen beliebiger Domains. **Speicherort der Gruppe:**Im Domainkontext der eigenen Domain. 

### Domain Local Group

![Domain-Local-Group](/assets/wiki/Domain-Local-Group.jpg)Grösse: 40 Bytes **MemberOf:**Accounts, Global Groups und Universal Groups aus allen Domains. Domain Local Groups nur aus der eigenen Domain. **Permission to:**auf Ressourcen der eigenen Domain. **Speicherort der Gruppe:**Im Domainkontext der eigenen Domain. 

### Universal Group

![Universal-Group](/assets/wiki/Universal-Group.jpg)Grösse: 8 Bytes **MemberOf:**Accounts, Global Groups und Universal Groups aus allen Domains innerhalb des Forests. **Permission to:**auf Ressourcen aller Domains innerhalb des Forests. **Speicherort der Gruppe:**Im Global Catalog (Forest). Und hier das ganze Bild dazu mit einem Forest und zwei Domains: ![Group-Scope](/assets/wiki/Group-Scope.jpg)

# Active Directory Federation Services

## Identity Provider

Kontenverwaltung: Verwaltung der Benutzer, die Firma in der die Benutzer arbeiten. Zugriff auf Web-Applikation beim Provider kann über Gruppenmitgliedschaft gesteuert werden. 

## Application Provider

Web-Applikation, z.B. SharePoint oder Cloud-Service. Zugriff mit Account aus Identity Provider Active Directory.