---
title: Split and Join
date: '2018-03-23T19:00:17+01:00'
author: Tinu
excerpt: Unregelmässige Texte mit vielen Leerzeichen zerlegen und in strukturierte
  Texte zusammensetzen.
categories:
- PowerShell
tags:
- String
image: /assets/wiki/powershell-1.png
wordpress_id: 2472
layout: post
permalink: /wiki/split-and-join/
render_with_liquid: false
---

Unregelmässige Texte mit vielen Leerzeichen zerlegen und in strukturierte Texte zusammensetzen ist ganz einfach.

```
$string1 = "   Account Logon                Success and Failure "
```

## Split

Mit Split einen String zerlegen: 

```
$string2 = $string1.Trim() -split '\s+'

$string2
Account
Logon
Success
and
Failure
```

## Join

Mit Join ein String-Array wieder als String zusammensetzen: 

```
$string2 -join " "

Account Logon Success and Failure
```