---
title: FRS zu DFRS migrieren
date: '2015-03-18T14:40:21+01:00'
author: Tinu
excerpt: ''
categories:
- Active Directory
tags:
- Domain Controller
wordpress_id: 997
layout: post
permalink: /wiki/frs-zu-dfrs-migrieren/
render_with_liquid: false
---

## Voraussetzungen

 Domain Functional Level muss mindestens Windows Server 2008 sein. 

### Global States

 0 Start (Nur FRS) 1 Prepared (FRS und DFSR) 2 Redirected (DFRS und FRS) 3 Eliminated (nur DFRS) Aktuellen Status überprüfen: dfsrmig /getglobalstate 

### Vorgehen

1. Auf allen DCs net share eingeben und prüfen, ob der NETLOGON sowie der SYSVOL auf SYSVOL freigegeben sind.
2. Auf dem PDC Emulator dfsrmig /getglobalstate eingeben
3. dfsrmig /setglobalstate 1
4. dfsrmig /getmigrationstate **ACHTUNG:** Erst weiterfahren, wenn „Migration has reached a consistent state on all Domain Controllers.“ auf dfsrmig /getmigrationstate zurückgegeben wird!
5. dfsrmig /setglobalstate 2
6. dfsrmig /getmigrationstate
7. Auf allen DCs net share eingeben und prüfen, ob der NETLOGON sowie der SYSVOL auf SYSVOL\_DFSR freigegeben sind.
8. Auf allen DCs DFS Replication Eventlog prüfen **ACHTUNG:** An dieser Stelle kann man noch ein Rollback auf FRS machen, später ist es nicht mehr möglich!
9. dfsrmig /setglobalstate 3
10. dfsrmig /getmigrationstate
11. DFS Replication Eventlog auf allen DCs prüfen.
12. Auf allen DCs net share eingeben und prüfen, ob der NETLOGON sowie der SYSVOL auf SYSVOL\_DFSR freigegeben sind.
13. Auf dem PDC Emulator im GPMC in der Default Domain Controller Policy den File Replication Service disablen.
 
 Weitere Informationen siehe Technet[ SYSVOL Replication Migration Guide](https://technet.microsoft.com/en-us/library/dd640019%28v=ws.10%29.aspx "Technet: SYSVOL Replication Migration Guide")