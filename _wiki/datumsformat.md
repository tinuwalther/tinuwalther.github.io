---
title: Datum/Zeit formatieren
date: '2014-12-19T16:22:47+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- DateTime
- Format
wordpress_id: 494
layout: post
permalink: /wiki/datumsformat/
render_with_liquid: false
---

## Datumsobjekt

```
get-date
```

Ergibt Freitag, 19. Dezember 2014 15:15:30 als Object

### 24-Stundenformat

```
get-date -f 'yyyy-MM-dd HH:mm:ss'
```

Ergibt 2014-12-19 15:15:30 als String

### 12-Stundenformat

```
get-date -f 'yyyy-MM-dd hh:mm:ss'
```

Ergibt 2014-12-19 03:15:30 als String

### DisplayHint

```
Get-Date -DisplayHint DateTime
```

```
Mittwoch, 20. September 2017 21:14:44
```

```
Get-Date -DisplayHint Date
```

```
Mittwoch, 20. September 2017
```

```
Get-Date -DisplayHint Time
```

```
21:20:19
```

### Differenz zwischen zwei Zeitangaben berechnen

Die Differenz zwischen zwei Zeitangaben kann ganz einfach mit PowerShell berechnet werden.

Am Beispiel einer Stempeluhr: einstempeln, ausstempeln und die Differenz einmal einmal in Stunden und Minuten und einmal in dezimal Stunden ausgeben:

```
$StartTime = Get-Date #'2024-03-21 07:30'
$EndTime   = Get-Date #'2024-03-21 09:45'
$(New-TimeSpan -Start $StartTime -End $EndTime | % { "Arbeitszeit: {1:0}h {2:0}m ({0}h)" -f $_.TotalHours, $_.Hours, $_.Minutes })
```

Output:

```
Arbeitszeit: 2h 15m (2.25h)
```