---
title: ValidateSet
date: '2016-06-23T21:09:47+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Switch
- ValidateSet
wordpress_id: 1491
layout: post
permalink: /wiki/validateset/
render_with_liquid: false
---

If all you want is limiting choices, you can use a ValidateSet attribute instead.

```
#requires -Version 2
function Select-City
{
  param
  (
    [ValidateSet('Bern','Zürich','Chur','Lugano')]
    [Parameter(Mandatory=$true)][String]$City
  )
    switch ($City)
    {
    'Bern'   {"The Gurten is in $City"}
    'Zürich' {"The Uetliberg is in $City"}
    'Chur'   {"The Brambrüesch is in $City"}
    'Lugano' {"The Monte San Salvatore is in $City"}
    }
}
Select-City
```