---
title: Environment
date: '2014-11-26T21:40:14+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Environment
wordpress_id: 166
layout: post
permalink: /wiki/environment/
render_with_liquid: false
---

# Environment Variablen

Arbeiten mit Environment Variablen? Nichts ist einfacher als das! Auflisten aller Environment Variablen: 

```csharp
Get-ChildItem Env:
```

Erstellen einer neuen Environment Variablen: 

```csharp
$env:TestVariable = "This is a test environment variable."
```

Löschen einer Environment Variablen: 

```csharp
Remove-Item Env:\TestVariable
```

## Beispiel

Aktuell angemeldeter Benutzer auflisten: 

```csharp
$env:username
```