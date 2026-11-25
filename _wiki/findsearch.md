---
title: Find/Search
date: '2015-01-12T16:22:13+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Find
- Search
wordpress_id: 533
layout: post
permalink: /wiki/findsearch/
render_with_liquid: false
---

# Die PowerShell Suche

File(s) ab dem Folder F:\\webapps abwärts suchen. 

```csharp
$file = "web.config"
$entry = "F:\webapps"
gci -path $entry -filter $file -Recurse | select fullname, LastWriteTime | ft -auto
```