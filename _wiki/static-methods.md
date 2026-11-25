---
title: Static Methods
date: '2016-03-02T23:16:48+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Scripting
wordpress_id: 1438
layout: post
permalink: /wiki/static-methods/
render_with_liquid: false
---

## String

```
[string] | Get-Member -Static
```

```
[string]::IsNullOrWhitespace($name)
```

```
[string]::IsNullOrEmpty($name)
```

## Environment

```
[System.Environment] | Get-Member -Static
```

## Convert

```
[convert] | Get-Member -Static
```

```
$decimal='255'
[convert]::ToString($decimal,2)
```

```
$binary='11111111'
[Convert]::ToInt64($binary,2)
```

## Math

```
[System.Math] | Get-Member -Static -MemberType Methods
```

```
[System.Math]::Round($value,$digits)
```

```
[System.Math]::Sqrt(9) = 3
```

```
[System.Math]::Pow(2,3) = 8
```

```
[System.Math]::Floor(3.3) = 3
```

```
[System.Math]::Floor(-3.3) = -4
```

```
[System.Math]::Ceiling(3.3) = 4
```

```
[System.Math]::Ceiling(-3.3) = -3
```

```
[System.Math]::Max(2,7) = 7
```

```
[System.Math]::Min(2,7) = 2
```

```
[System.Math]::Truncate(9.3) = 9
```

```
[System.Math]::Truncate(-9.3) = -9
```

## Guid

```
[System.Guid]::NewGuid()
```