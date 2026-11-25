---
title: Array
date: '2015-03-03T09:30:24+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Array
wordpress_id: 856
layout: post
permalink: /wiki/array/
render_with_liquid: false
---

Arbeiten mit Arrays in PowerShell.

## Variable initialisieren

```csharp
$array = @()
```

## Werte zuweisen

```csharp
$array = @('Single element')
```

```csharp
foreach($item in $collection) {
    $array += '<new element>'
}
```

```csharp
$array = @('element1','element2','element3')
```

```csharp
$array = @(
    'element1,
    'element2',
    'element3'
)
```

## Überprüfung auf Array

```csharp
if ($array -is [system.array]){...}
if ($array $variable -isnot [system.array]){...}
```

## Erstes Element auslesen

```csharp
$array[0]
```

## Letztes Element auslesen

```csharp
$array[-1]
```

## Anzahl Elemente auslesen

```csharp
$array.length-1
```