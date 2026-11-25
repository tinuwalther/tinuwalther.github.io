---
title: Object abfüllen
date: '2014-12-23T10:38:44+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- PSObject
wordpress_id: 505
layout: post
permalink: /wiki/object-abfuellen/
render_with_liquid: false
---

# PSObject in einer Schleife abfüllen

```csharp
$ret = @()
$list | % {
    $obj = New-Object PSObject
    Add-Member -InputObject $obj -MemberType NoteProperty -Name Computer -Value $($_)
    Add-Member -InputObject $obj -MemberType NoteProperty -Name Path -Value $path
    $ret += $obj
}
$ret | ft -auto -wrap | Out-String
```