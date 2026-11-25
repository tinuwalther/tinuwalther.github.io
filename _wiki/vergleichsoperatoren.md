---
title: Vergleichsoperatoren
date: '2014-11-26T22:42:42+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Vergleichsoperatoren
wordpress_id: 175
layout: post
permalink: /wiki/vergleichsoperatoren/
render_with_liquid: false
---

# Zahlen-/Zeichen-Vergleiche

## Equal (-eq, -ne)

gleich 

```csharp
12 -eq 11 #ergibt False

```

ungleich 

```csharp
12 -ne 11 #ergibt True

```

## Less than (-lt, -le)

kleiner als kleiner oder gleich 

## Greater than (-gt, -ge)

grösser als grösser oder gleich 

# Zeichenketten-Vergleiche

## Like (-like, -notlike)

Ermitteln, ob eine bestimmte Zeichenkette in einer anderen enthalten ist. Like ignoriert die Gross- Kleinschreibung. 

```csharp
"Nebel" -like "Nebel" #ergibt True
"Nebel" -like "ebe" #ergibt False

```

Wenn die beiden Strings nicht identisch sind, dann benötigt man dafür Wildcards. Der Stern (\*) kann mehrere Zeichen ersetzen und das Fragezeichen (?) nur ein einziges. 

```csharp
"Nebel" -like "?ebe*" #ergibt True

```

## Match (-match, -notmatch)

Substrings durchsuchen ohne Wildcards. 

```csharp
"Martin" -match "art" #ergibt True

```

## Contains (-contains, -notcontains)

Suche in Collections, dient zum prüfen, ob in Arrays ein bestimmtes Element enthalten ist. Wildcards wie in -like verwendet, werden nicht unterstützt. Erforderlich ist eine exakte Übereinstimmung mit einem Element der Collection wie bei -eq. 

```csharp
$Months = @("Januar","Februar","Maerz","April")
$Months -contains "Februar" #ergibt True

```