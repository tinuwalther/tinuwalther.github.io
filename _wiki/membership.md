---
title: MemberShip
date: '2018-01-24T19:51:31+01:00'
author: Tinu
excerpt: User und seine Gruppenmitgliedschaft mit dem ADSI-Provider auflisten.
categories:
- Active Directory
- PowerShell
tags:
- Accounts
- Active Directory
- Groups
image: /assets/wiki/powershell-1.png
wordpress_id: 2452
layout: post
permalink: /wiki/membership/
render_with_liquid: false
---

## Alle Gruppen eines Users auflisten

### AD-Commandlet

```
Get-ADUser (Read-Host 'Enter the username to search') -properties memberof | select -expandproperty memberof
```

### ADSI Methode

```
function Get-UsersMemberOf{

[CmdletBindings()]
 param($input)

 $adsi        = [adsisearcher]""
 $adsi.Filter = "name=$($input)" 
 $adsiobject  = $adsi.FindOne() 
 $adobject    = [ADSI]"$($adsiobject.Path)"
 $MemberOf    = $adobject.MemberOf | ForEach-Object {[ADSI]"LDAP://$_"} | Select Name,info,description,distinguishedName,managedBy

 @{"Name"=$adobject.Name}
 @{"description"=$adobject.description}
 @{"distinguishedName"=$adobject.distinguishedName}
 $MemberOf | Select -Property Name,info,description | sort name | ft -AutoSize

}
Get-UsersMemberOf -input (Read-Host 'Enter the username to search')
```

## Alle Members einer Gruppe auflisten

### AD-Group Commandlet

```
Get-ADGroupMember -Identity (Read-Host 'Enter the groupname to search') ...
```

### ADSI Methode

```
function Get-GroupMembers{

[CmdletBindings()]
 param($input)

 $adsi = [adsisearcher]"" 
 $adsi.Filter = "name=$($input)"
 $adsiobject = $adsi.FindOne() 
 $adobject = [ADSI]"$($adsiobject.Path)"
 $Members = $adobject.Member | ForEach-Object {[ADSI]"LDAP://$_"} | Select givenName,sn,name,displayName,description,distinguishedName

 @{"Name"=$adobject.Name}
 @{"description"=$adobject.description}
 @{"distinguishedName"=$adobject.distinguishedName}
 $Members | Select -Property Name,givenName,sn,description | sort name | ft -AutoSize

}
Get-GroupMembers -input (Read-Host 'Enter the groupname to search')
```

```
```