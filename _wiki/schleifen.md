---
title: Schleifen
date: '2015-03-06T12:25:31+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Schleifen
wordpress_id: 893
layout: post
permalink: /wiki/schleifen/
render_with_liquid: false
---

## for-Schleife

```csharp
for ($i = 0; $i -lt 100; $i++){
    write-host $i
}
```

## while-Schleife

```csharp
while ($i -le 5) {
    Write-Host $i; $i++
}
```

## do-while-Schleife

```csharp
do {
    Write-Host $i; $i++
}
while ($i -le 5)
```

## do-until-Schleife

```csharp
do {
    Write-Host $i; $i++
}
until ($i -gt 5)
```

## foreach-Schleife

```csharp
foreach($element in $array) {
    Write-Host $element
}
```

## foreach-Object

Foreach-Object ist ein Cmdlet. 

```csharp
Get-ADUser -Filter *| %{
    Write-Host $_
}
```

## Schleifensteuerung mit break und continue

Siehe [WindowsPro](http://www.windowspro.de/script/schleifen-powershell-foreach-while-do-until-continue-break "Schleifen in PowerShell: For, Foreach, While, Do-Until, Continue, Break")

## Timerschleife

```csharp
1..60 | foreach {write-host '.' -nonewline;sleep -Seconds 1}
```