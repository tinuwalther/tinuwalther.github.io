---
title: Troubleshooting Authentication
date: '2015-04-02T19:25:55+02:00'
author: Tinu
excerpt: ''
categories:
- Active Directory
tags:
- Authentication
- Kerberos
- Windows Server
wordpress_id: 1090
layout: post
permalink: /wiki/authentication/
render_with_liquid: false
---

Betrifft Windows Server 2012 R2 Domain Controller und Windows 8.1 mit NAS (NetApp-Filer).

## Symptom

- Zugriff auf mit Namen verbundenes Netzlaufwerk (\\\\&lt;Filer&gt;\\&lt;Share&gt;) gibt **Access denied** zurück (Kerberos Authentication)
- Zugriff auf mit IP Adresse verbundenes Netzlaufwerk (\\\\10.20.30.40\\&lt;Share&gt;) funktioniert fehlerfrei (Fallback NTLM Authentication)
 

## Problem

- Kerberos is used to authenticate the user's session to the NAS device
- The kerberos ticket used in the session setup was issued by a KDC running Windows Server 2012
- The NAS device does not understand Resource SID Compression, which is a new feature for Kerberos in Windows Server 2012
 

## Lösung

 Resource SID Compression entweder auf dem NAS Objekt im AD oder auf allen Windows Server 2012 DCs ausschalten (disable Resource Group Compression bit). Siehe Microsoft Support [Resource SID Compression in Windows Server 2012 may cause authentication problems on NAS devices](http://support.microsoft.com/en-us/kb/2774190)

### Registry Key auflisten

 Eventuell existiert der Registry Key noch nicht. 

```csharp
ls HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\System\Kdc\Parameters
```

### SID Compression komplett ausschalten

```csharp
$regpath = "HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\System\Kdc\Parameters"
New-Item $regpath -Force
Set-ItemProperty -Path $regpath DisableResourceGroupsFields -Value 1 -Force
Get-ItemProperty $regpath

```

## KDC SID Resource Compression

 In älteren Windows Betriebssystemen war die Kerberos Token Size oft ein Problem. Microsoft hat darauf reagiert und ein neues Feature "KDC SID Resource Compression" eingeführt. Das Feature entfernt die identische Domain SID (S-1-5-21-3419695430-3854377854) und fügt nur die RID (1466) in das Kerberos Token, somit kann das Token viel kleiner gehalten werden: 

```
S-1-5-21-3419695430-3854377854-<b>1234</b>
 -<b>1466</b>
 -<b>1675</b>
S-1-5-21-4533280865-6432248977-<b>6523</b>
 -<b>6578</b>
```

 Diverse Systeme (NAS, Exchange, Webapplikationen. etc.) können nur mit der kompletten SID eines Objektes umgehen und lösen den oben genannten **Access denied** Fehler aus. 

### NetApp Ontap

 Ontap 8.1.2P2 ist bisher die einzige Version, die mit KDC Resource SID Compression umgehen kann.