---
title: Lingering Objects
date: '2015-03-24T12:04:26+01:00'
author: Tinu
excerpt: ''
categories:
- Active Directory
tags:
- Active Directory
wordpress_id: 1044
layout: post
permalink: /wiki/lingering-objects/
render_with_liquid: false
---

Wie kann man Lingering Objects (veraltete Objekte) entdecken und entfernen?

## Dsquery

### Konflikt-Objekte anzeigen lassen

```
dsquery * forestroot -gc -attr distinguishedname -scope subtree `
-filter "(name=*\0ACNF:*)" -limit 500
```

## Repadmin

### GUID eines DCs herausfinden

 Um die GUID eines DCs herauszufinden, kann man z.B. den Befehl REPADMIN /Showrepl &lt;DC-Name&gt; eingeben. 

### Veraltete Objekte entfernen

```
REPADMIN /removelingeringobjects <DNS-Name des "veralteten" DCs> `
<GUID eines "aktuellen" DCs> <Verzeichnispartition der veralteten Objekte> `
/Advisory_Mode
```

 Der Parameter /Advisory\_Mode protokolliert dabei im Verzeichnisdienstprotokoll die Ereignis-ID 1946 für jedes existierende veraltete Objekt. 

## Verzeichnisdienstprotokoll

 Event ID 2108 and Event ID 1084 occur during inbound replication of Active Directory ... Event ID 1388 or 1988: A lingering object is detected ... [Yusuf weiss immer eine Lösung](http://blog.dikmenoglu.de/2007/04/lingering-objects-veraltete-objekte/ "LDAP://Yusufs.Directory.Blog")