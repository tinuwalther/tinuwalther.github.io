---
title: Format string
date: '2017-09-20T20:58:15+02:00'
author: Tinu
excerpt: .NET verfügt über eine Methode zur Formatierung von Zeichenketten, mit der
  Nummern formatiert werden können.
categories:
- PowerShell
tags:
- Format
- Random
image: /assets/wiki/powershell-1.png
wordpress_id: 2357
layout: post
permalink: /wiki/formatting-numbers/
render_with_liquid: false
---

## .NET Framework formatting methods

Einfache .NET Framework Methode zum Formatieren von Zahlen.

```
"{0:N2}" -f 554.22272, 2345555
```

0 = Index number of the item to be formatted  
N = Datentyp (**N**umeric, **D**igits, **C**urrency, **P**ercentage, He**X**adecimal, 0 = leading zero)  
2 = Anzahl Nachkommastellen

### More Fun With Formatting Numbers

Variable mit einer Nummer abfüllen:

```
$number = 6348
```

Numeric mit zwei Nachkommastellen

```
"{0:N2}" -f $number
```

Output

```
6'348.00
```

The value is displayed using the number of digits; if needed, leading zeroes are added to the beginning of the number.

```
"{0:D8}" -f $number
```

Output

```
00006348
```

Währung mit zwei Nachkommastellen

```
"{0:C2}" -f $number
```

Output

```
CHF 6'348.00
```

The value is multiplied by 100 and displayed as a percentage.

```
"{0:P0}" -f $number
```

Output

```
634'800%
```

The value is displayed as a hexadecimal number.

```
"{0:X0}" -f $number
```

Output

```
18CC
```

### Leading zeroes

Randomize Zeit zusammenstellen:

```
"{0:d2}" -f (Get-Random -Maximum 23) + ":" + "{0:d2}" -f (Get-Random -Maximum 59) + ":" + "{0:d2}" -f (Get-Random -Maximum 59)
```

Output

```
08:38:55
```

IBAN oder so was ähnliches generieren:

```
"{0:CH00}" -f (Get-Random -Maximum 99) + " " + "{0:0000}" -f (Get-Random -Maximum 9999) + " " + "{0:0000}" -f (Get-Random -Maximum 9999) + " " + "{0:0000}" -f (Get-Random -Maximum 9999)
```

Output

```
CH68 1706 6845 5030
```

1000 Dateien anlegen:

```
1..1000 | ForEach-Object { 
    $FileName = "Test_{0:d4}.txt" -f $_
    New-Item -ItemType File -Name $FileName -WhatIf
}
```

### Zeitangaben formatieren

Will man eine Zeitspanne formatiert ausgeben, kann dies wie folgt gemacht werden:

```
$(New-TimeSpan -Start ((Get-Date).AddDays(-3)) -End (Get-Date) | % { "{0:0d} {1:0}h {2:0}m {3:0}s {4:000}ms" -f $_.Days, $_.Hours, $_.Minutes, $_.Seconds, $_.Milliseconds })
```

Output

```
3d 0h 0m 0s 001ms
```