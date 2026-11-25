---
title: Yes or No Abfrage
date: '2016-07-01T10:19:56+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Regex
wordpress_id: 1508
layout: post
permalink: /wiki/yes-or-no-abfrage/
render_with_liquid: false
---

Mit einer Regex-Auswertung auf Yes oder No abfragen:

```
$ret = Read-Host 'Would you create a file? [Y] Yes, [N] No'
if($ret -match '^y')
{
    Write-Output "Yes ($($ret))"
}
elseif($ret -match '^n')
{
    Write-Output "No ($($ret))"
}
```