---
title: Replace content
date: '2018-06-28T13:49:03+02:00'
author: Tinu
excerpt: Mit PowerShell Text in einem File ersetzen
categories:
- PowerShell
tags:
- Scripting
image: /assets/wiki/powershell-1.png
wordpress_id: 2484
layout: post
permalink: /wiki/replace-content-in-file/
render_with_liquid: false
---

Mit PowerShell Text in einem File ändern, kann auch in einer Remote Session durchgeführt werden:

```
$file        = "C:\Temp\file.txt"
$searchfor   = "alpha"
$replacewith = "beta"
(Get-Content $file).Replace($searchfor, $replacewith) | Set-Content $file -Force -PassThru
```