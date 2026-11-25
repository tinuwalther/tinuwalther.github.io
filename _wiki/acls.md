---
title: ACLs bearbeiten
date: '2015-02-17T10:08:51+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- ACL
wordpress_id: 674
layout: post
permalink: /wiki/acls/
render_with_liquid: false
---

ACLs mit PowerShell auflisten und schreiben.

## ACLs auflisten

```csharp
Get-Acl C:\Windows\Temp | select AccessToString | fl

AccessToString : CREATOR OWNER Allow  268435456
NT AUTHORITY\SYSTEM Allow  FullControl
NT AUTHORITY\SYSTEM Allow  268435456
BUILTIN\Administrators Allow  FullControl
BUILTIN\Administrators Allow  268435456
BUILTIN\Users Allow  CreateFiles, AppendData, ExecuteFile, Synchronize
```

## ACLs schreiben

 Gewünschte ACLs auf einem File schreiben und in Object einlesen: 

```csharp
$NewAcl = Get-Acl File.txt
```

 Neu gesetzte ACLs als Vorlage auf anderen Pfad (rekursive) schreiben: 

```csharp
Get-ChildItem C:\temp -Recurse -Include *.txt -Force | Set-Acl -AclObject $NewAcl
```