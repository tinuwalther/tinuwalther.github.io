---
title: IIS Maintenance
date: '2015-03-03T10:03:16+01:00'
author: Tinu
excerpt: ''
categories:
- Webserver
tags:
- IIS
wordpress_id: 864
layout: post
permalink: /wiki/iis-maintenance/
render_with_liquid: false
---

## IIS Logfiles

 Die Logfiles sind unter dem im IIS Manager eingestelleten Pfad als **u\_ex150710.log** gespeichert. 

## Application Pool recyclen

```
appcmd recycle apppool /apppool.name:<Applicationpool name>
```