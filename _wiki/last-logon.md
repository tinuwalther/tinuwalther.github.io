---
title: Last Logon
date: '2015-04-08T12:30:22+02:00'
author: Tinu
excerpt: ''
categories:
- Active Directory
- PowerShell
tags:
- Logon
wordpress_id: 1123
layout: post
permalink: /wiki/last-logon/
render_with_liquid: false
---

Immer wieder kommt die Frage "wie kann ich die letzte Anmeldung eines Users im AD feststellen"? Es gibt zwei Attribute dafür; das LastLogon und das LastLogonTimeStamp.

## LastLogon

 Das LastLogon Attribut wird auf dem jeweiligen Logon Server (DC) eingetragen und nicht im Active Directory repliziert. 

## LastLogonTimestamp

 Betrifft Windows Server 2003 functional level und höher. Das LastLogonTimestamp Attribut wird im Active Directory repliziert und gibt Auskunft über die letzte Anmeldung des Users im AD. 

### Und wie man es mit PowerShell auslesen kann

```csharp
$sAM = (read-host 'Enter the samAccountName')
get-aduser -filter {samaccountname -eq $sAM} -property lastlogontimestamp | ft `
UserPrincipalName, @{
    N='LastDomainLogon'; E={[DateTime]::FromFileTime($_.LastLogonTimestamp)}
} -auto
```