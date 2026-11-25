---
title: Transcript
date: '2015-06-25T08:49:20+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Logging
- Scripting
wordpress_id: 1264
layout: post
permalink: /wiki/transcript/
render_with_liquid: false
---

Ausgabe mit Transcript in ein Logfile abspeichern.

## Transcript starten

```
Try {Stop-Transcript}catch{}
Start-Transcript -Path "C:\Scripts\Transcript.log"
```

## Transcript stoppen

Nicht vergessen die Aufzeichnung nach Gebrauch zu stoppen. 

```
Stop-Transcript
```

## Fazit

Die Formatierung lässt noch zu wünschen übrig. Ansonsten finde ich diese Funktion sehr hilfreich.