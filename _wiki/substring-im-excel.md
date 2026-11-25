---
title: Substring im Excel
date: '2016-10-19T11:14:21+02:00'
author: Tinu
excerpt: ''
categories:
- Office
tags:
- Excel
wordpress_id: 1663
layout: post
permalink: /wiki/substring-im-excel/
render_with_liquid: false
---

Ich suche immer wieder nach der Formel im Excel, um den Hostname vom FQDN zu extrahieren. Hier ist die Lösung für das deutsche Excel:

| **FQDN** | **Hostname** |
|---|---|
| server.domain.name | =LINKS(A2;SUCHEN(".";A2)-1) |

 Eine gute Seite mit Formeln habe ich [hier](http://www.netschulung.com/stringfunktionen-in-excel-teil-2/) gefunden.