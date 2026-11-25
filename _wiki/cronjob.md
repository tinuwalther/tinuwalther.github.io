---
title: Cronjob
date: '2018-07-20T20:13:32+02:00'
author: Tinu
excerpt: Was bei Windows der Scheduled Task ist, ist bei Linux der Cronjob.
categories:
- Linux
tags:
- Open Source
image: /assets/wiki/linux-1.png
wordpress_id: 2499
layout: post
permalink: /wiki/cronjob/
render_with_liquid: false
---

Was bei Windows der Scheduled Task ist, ist bei Linux der Cronjob. Alle cronjobs auflisten:

```
crontab -l
```

## Crontab Syntax

Jeder Cronjob hat folgendes Format: 

```
* * * * * auszuführender Befehl
┬ ┬ ┬ ┬ ┬
│ │ │ │ │
│ │ │ │ └──── Wochentag (0-7, Sonntag ist 0 oder 7)
│ │ │ └────── Monat (1-12)
│ │ └──────── Tag (1-31)
│ └────────── Stunde (0-23)
└──────────── Minute (0-59)
```

Ein Stern \* bedeutet Ausführung wird immer erfolgen, also zu jeder Minute, jeder Stunde, jedem Tag, jedem Monat oder jedem Wochentag. Um die einzelnen Stellen auseinander zu halten, hilft folgendes Diagram: 1 2 3 4 5 Befehl 1 = Minute (0-59) 2 = Stunde (0-23) 3 = Tag (0-31) 4 = Monat (1-12) 5 = Wochentag (0-7, Sonntag ist 0 oder 7) Befehl = Der auszuführende Befehl. Für die ersten fünf Stellen, also die Zeiwerte sind folgende Optionen zusätzlich möglich: \* = Ausführung immer (zu jeder…) \*/n = Ausführung aller n n,x,y = Ausführung um/am n, x und y 

## Crontab mit eigenen Zeilen ergänzen

crontab in Datei umleiten 

```
crontab -l > cronfile
```

eigene Zeile in Datei hinzufügen 

```
echo "0 * 15 * * /usr/bin/php -f /var/www/cron.php" >> cronfile
```

Datei in crontab einlesen 

```
crontab cronfile
```