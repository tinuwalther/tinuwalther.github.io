---
title: String Manipulationen
date: '2015-01-23T21:41:38+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- String
wordpress_id: 2443
layout: post
permalink: /wiki/string-manipulationen/
render_with_liquid: false
---

## Ein String

 Alle Beispiele sind von folgendem String ausgehend: 

```
$text = ' ...Hello 4 my 15 world... '
```

## Die Methoden

### Clone

### CompareTo

### Contains

### CopyTo

### EndsWith

 Prüfen ob ein Text auf ein bestimmtes Zeichen (oder eine Zeichenkette) endet: 

```
$text.EndsWith('world')

False
```

### Equals

 Prüfen ob ein Text mit einem bestimmten String identisch ist: 

```
$text.Equals('Hello')

False

$text.Equals(' ...Hello 4 my 15 world... ')

True
```

### GetEnumerator

### GetHashCode

### GetType

 Mit GetType() kann der Datentyp abgefragt werden. 

```
$text.GetType()

IsPublic IsSerial Name    BaseType                                                                                                                  
-------- -------- ----    --------                                                                                                                  
True     True     String  System.Object 
```

### GetTypeCode

### IndexOf

 IndexOf() liefert die erste Stelle des abgefragten Zeichens zurück: 

```
$text.IndexOf('o')
10
```

### IndexOfAny

### Insert

 Ein oder mehrere Zeichen an einer bestimmten Stelle einfügen: 

```
$text.Insert(0,'XXX')

XXX ...Hello 4 my 15 world...
```

### IsNormalized

### LastIndexOf

 LastIndexOf() liefert die letzte Stelle des abgefragten Zeichens zurück: 

```
$text.LastIndexOf('o')
21
```

### LastIndexOfAny

### Normalize

### PadLeft

### PadRight

### Remove

 Mit Remove() kann ab der Startlänge eine bestimmte Länge an Zeichen entfernt werden: 

```
$text.Remove(0,$text.IndexOf('H'))

Hello 4 my 15 world...
```

```
$StartIndex = $text.IndexOf('H')
$left = $text.Remove(0,$text.IndexOf('H'))
$left.Remove($left.LastIndexOf('d') + 1, 5)

Hello 4 my 15 world
```

### Replace

 Besser als Remove ist da Replace(), damit können bestimmte Zeichen entfernt werden: 

```
$text.Replace('.','!')

 !!!Hello 4 my 15 world!!!
```

### Split

 Mit Split() kann ein String auf ein bestimmtes Zeichen in ein Array aufgetrennt werden: 

```
$collection = $text.Split(' ')
for($i = 0; $i -lt $collection.GetUpperBound(0); $i++){
    Write-Host "$($i) - $($collection[$i])"
}

0 - 
1 - 
2 - 
3 - ...Hello
4 - 4
5 - my
6 - 15
7 - world...
8 -
```

### StartsWith

 Prüfen ob ein Text auf ein bestimmtes Zeichen (oder eine Zeichenkette) beginnt: 

```
$text.StartsWith(' ...H')

True
```

### Substring

 Mit Substring() kann ein Teil des Strings ausgelesen werden: 

```
$text.Substring(6,19) 
Hello 4 my 15 world
```

 Kombiniert mit IndexOf() und LastIndexOf(): 

```
$StartIndex = $text.IndexOf('...') + 3
$length     = $text.LastIndexOf('...') - $StartIndex
$text.Substring($StartIndex,$length)

Hello 4 my 15 world
```

### ToBoolean

### ToByte

### ToChar

### ToCharArray

### ToDateTime

### ToDecimal

### ToDouble

### ToInt16

### ToInt32

### ToInt64

### ToLower

 Mit ToLower() werden alle Zeichen klein geschrieben: 

```
$text.ToLower()

 ...hello 4 my 15 world...
```

### ToLowerInvariant

### ToSByte

### ToSingle

### ToString

### ToType

### ToUInt16

### ToUInt32

### ToUInt64

### ToUpper

 Mit ToUpper() werden alle Zeichen gross geschrieben: 

```
$text.ToUpper()

 ...HELLO 4 MY 15 WORLD...
```

### ToUpperInvariant

### Trim

 Mit Trim() können die Leerzeichen vor- und nach dem eigentlichen Text entfernt werden: 

```
$text.Trim()

...Hello 4 my 15 world...
```

### TrimEnd

 Mit TrimEnd() können die Leerzeichen nach dem eigentlichen Text entfernt werden: 

```
$text.TrimEnd()

 ...Hello 4 my 15 world...
```

### TrimStart

 Mit TrimStart() können die Leerzeichen vor dem eigentlichen Text entfernt werden: 

```
$text.TrimStart()

...Hello 4 my 15 world...
```

## Die Properties

### Chars

 Datentyp Char 

```
$text.Chars(14)
m
```

### Length

 Datentyp Integer 

```
$text.Length

30
```