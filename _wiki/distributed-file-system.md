---
title: Distributed File System
date: '2014-11-30T11:14:21+01:00'
author: Tinu
excerpt: ''
categories:
- Windows Server
tags:
- DFS
wordpress_id: 289
layout: post
permalink: /wiki/distributed-file-system/
render_with_liquid: false
---

# DFS

## DFS-Replication

 Replikation von Dateien auf zwei oder mehrere Fileserver über LAN oder WAN 

- Windows Feature DFS-Replication muss auf allen beteiligten Servern installiert werden
- Identische Folderstruktur muss auf allen beteiligten Servern erstellt werden
- Replikation erfolgt über Active Directory File Replication Service (DFSR bzw. DFSRs.exe)
 

## DFS-Namespace

 Gemeinsamer Namensraum für den Share 

- Service: DFS oder dfssvc.exe
 

### DFS-Namespace auf DFS-Server

 C:\\DFSRoot\\&lt;DFS-Name&gt; 

- Links auf Shares (\\\\server\\share)
- Shares können auf vielen verschiedenen Servern liegen
- Berechtigungen werden auf NTFS vergeben
 

### Stand-allone DFS-N

- Windows Feature DFS-Namespace muss dem DFS-Servern installiert werden
- Konfiguration wird auf einem Server abgelegt
- Namensraum ist der Servername (\\\\vm1345\\data)
 

### Active Directory Integrated DFS-N

- Windows Feature DFS-Namespace muss dem DFS-Servern installiert werden
- Konfiguration wird im AD gespeichert und somit auf alle DCs synchronisiert
- Namensraum ist der Domain Name (\\\\&lt;domain.local&gt;\\data)