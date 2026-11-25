---
title: ASP .NET
date: '2015-06-01T16:37:56+02:00'
author: Tinu
excerpt: ''
categories:
- Webserver
wordpress_id: 1209
layout: post
permalink: /wiki/asp-net/
render_with_liquid: false
---

AspNet funktioniert nur wenn .NET Environment 3.5 (WAS-NET-Environment) installiert ist.

## WAS-NET-Environment installieren

```
Dism /online /enable-feature /featurename:WAS-NetFxEnvironment /All /Source:D:\sources\sxs /LimitAccess
```