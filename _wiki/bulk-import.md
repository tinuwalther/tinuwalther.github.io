---
title: Bulk Import
date: '2015-01-13T23:01:43+01:00'
author: Tinu
excerpt: ''
categories:
- Active Directory
tags:
- Accounts
- Active Directory
wordpress_id: 548
layout: post
permalink: /wiki/bulk-import/
render_with_liquid: false
---

# Active Directory Bulk Import

 Ein Massenimport von Gruppen in ein Active Directory. Die Definitionen werden in einem CSV-File gemacht. 

## PowerShell-Script

 Download [BulkImport.ps1](https://github.com/tinuwalther/active-directory "Download Scripts") from GitHub. In das Feld **Notes** wird automatisch der Timestamp des Imports geschrieben. Dies kann natürlich beliebig geändert werden, z.b. mit dem String 'Auto import'. 

```csharp
$now = <span class="pl-k">$(</span><span class="pl-s3">get-date</span> <span class="pl-k">-f</span> <span class="pl-s1">'yyyy-MM-dd HH:mm:ss'</span><span class="pl-k">)
<span class="pl-s3">Set-ADGroup</span> <span class="pl-k">$(</span><span class="pl-en">GroupName</span><span class="pl-k">)</span> <span class="pl-k">-Replace</span> @{info<span class="pl-k">=</span>”Auto import: $($now)”}</span>
```

## CSV-File

 Das CSV-File muss mindestens folgende Spalten enthalten: 

| **Spalte/Feld** | **Bemerkung** |
|---|---|
| GroupName | Name der Gruppe wie sie im Active Directory heissen soll (DG\_HR\_Assistents, DL\_R\_XXX, DL\_W\_XXX) |
| GroupType | Typ der Gruppe (DomainLocal oder Global) |
| GroupLocation | DistinguishedName der Ziel-OrganizationalUnit (OU=Import,DC=contoso,DC=com) |
| GroupDescription | Beschreibung der Gruppe (Role HR-Assistents, Read-Permission to XXX, Write-Permission to XXX) |

 Weitere Felder können selbstverständlich aufgenommen und ausprogrammiert werden.