---
title: Regex kurz erklärt
date: '2017-08-08T18:53:42+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Regex
wordpress_id: 2306
layout: post
permalink: /wiki/regex-kurz-erklaert/
render_with_liquid: false
---

## Regex Pattern

Wichtige Regex Pattern: 

```
\d digit [0-9]
\w alpha numeric [a-zA-Z0-9_]
\s whitespace character
.  any character except newline
() sub-expression 
\  escape the next character
```

## Cmdlets

```
Get-Content
Select-String
Select-Object
Split
Replace
```

## Aus einem Logfile einen Wert exportieren

Dazu benötigen wir ein Logfile und die Cmdlets Select-String und Select-Object mit ihren Parametern. 

```
$content = Get-Content C:\Windows\WindowsUpdate.log
```

$content enthält nun: *Windows Update logs are now generated using ETW (Event Tracing for Windows).* *Please run the Get-WindowsUpdateLog PowerShell command to convert ETW traces into a readable WindowsUpdate.log.**For more information, please visit http://go.microsoft.com/fwlink/?LinkId=518345*

### Select-String

Mit Select-String schränken wir den Inhalt auf die Zeilen ein, welche 'PowerShell' enthalten. 

```
$ret = $content | Select-String -Pattern 'PowerShell' -AllMatches
```

$ret ist zu einem System.Object umgewandelt worden und enthält nun: *Please run the Get-WindowsUpdateLog PowerShell command to convert ETW traces into a readable WindowsUpdate.log.*Dieses Object können wir nun nach deren Properties und Methods befragen: 

```
$ret | Get-Member

<em>TypeName: Microsoft.PowerShell.Commands.MatchInfo</em>

<em>Name         MemberType Definition</em>
<em>----         ---------- ----------</em>
<em>Equals       Method   bool Equals(System.Object obj)</em>
<em>GetHashCode  Method   int GetHashCode()</em>
<em>GetType      Method   type GetType()</em>
<em>RelativePath Method   string RelativePath(string directory)</em>
<em>ToString     Method   string ToString(), string ToString(string directory)</em>
<em>Context      Property Microsoft.PowerShell.Commands.MatchInfoContext Context {get;set;}</em>
<em>Filename     Property string Filename {get;}</em>
<em>IgnoreCase   Property bool IgnoreCase {get;set;}</em>
<em>Line         Property string Line {get;set;}</em>
<em>LineNumber   Property int LineNumber {get;set;}</em>
<em>Matches      Property System.Text.RegularExpressions.Match[] Matches {get;set;}</em>
<em>Path         Property string Path {get;set;}</em>
<em>Pattern      Property string Pattern {get;set;}</em>
```

Für uns interessant ist das Property Matches, welches wir um weitere Properties befragen (können): 

```
$ret.Matches

<em>Groups   : {0}</em>
 <em> Success  : True</em>
 <em> Name     : 0</em>
 <em> Captures : {0}</em>
 <em> Index    : 36</em>
 <em> Length   : 10</em>
 <em> Value    : PowerShell
</em>
```

### Select-Object

Nun interessiert uns ja eigentlich nur ob 'PowerShell' im Value steht und dies wollen wir zurückgeben: 

```
$ret.Matches | Select-Object -ExpandProperty value
```

*PowerShell*

### Hier die Kurzfassung

```
$content = Get-Content C:\Windows\WindowsUpdate.log
$ret = $content | Select-String -Pattern 'PowerShell' -AllMatches | `
Select-Object -ExpandProperty matches | Select-Object -ExpandProperty value
```

Sind nun mehr als eine Zeile mit den gesuchten Werten im Return, kann z.B. der letzte mit Select-Object ausgegeben werden: 

```
$ret | Select-Object -Last 1
```

### Split

```
$ret -split ':')
```

### Replace

```
$ret -replace '\s+','''
```

  Weitere Informationen zu Regex siehe [Kevin Marquette](https://kevinmarquette.github.io/2017-07-31-Powershell-regex-regular-expression/?utm_source=twitter&utm_medium=blog&utm_content=bottomlink).