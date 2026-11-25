---
title: Troubleshooting SMB
date: '2015-04-01T20:58:07+02:00'
author: Tinu
excerpt: ''
categories:
- Active Directory
tags:
- Authentication
- Filer
- SMB
wordpress_id: 1085
layout: post
permalink: /wiki/troubleshooting-smb/
render_with_liquid: false
---

Betrifft Windows Server 2012 R2 Domain Controller und Windows 8.1 mit NetApp-Filer.

## SMB Versionen

- Windows Server 2012 R2 -&gt; SMB 3.2
- Windows Server 2012 -&gt; SMB 3.0
- Windows Server 2008 R2 -&gt; SMB 2.1
- Windows Server 2008 -&gt; SMB 2.0
- Windows Server 2000 -&gt; SMB 1.0
- Windows NT 4.0 -&gt; CIFS
 

## SMB Version auflisten

### Ab PowerShell 4.0

 Auf einem Computer mit den verbundenen SMB-Shares folgenden PowerShell Befehl ausführen: 

```csharp
Get-SmbConnection
```

### Die lokale SMB Version auflisten:

 In einem PowerShell Fenster 

```csharp
dir \\File\SMB-Share
```

 und innerhalb von 10 Sekunden den PowerShell Befehl 

```csharp
Get-SmbConnection -ServerName localhost
```

 ausführen. 

### Vorherige PowerShell Versionen

 Mit einem Wireshark-Trace die Kommunikation zwischen Client und NetApp-Filer sniffern. 

## Symptome

 Beim Verbinden auf einen NetApp-Share tritt ein Fehler auf: 

- Verbinden per UNC Pfad: an **extended** **error** has occured
- Verbinden per net use: System error **2148073478** has occured
- Verbinden per dir: **Invalide** **Signature**
 
 This problem is caused by the **Secure Negotiate feature** that was added to **SMB 3.0** for **Windows Server 2012 and Windows 8**. This feature depends upon the correct signing of error responses by all SMBv2 servers, including servers that support only protocol versions 2.0 and 2.1. Some third-party file servers do not return a signed error response. Therefore, the connection fails. 

## Lösung

 Auf dem Filer RequireSecuritySignature einschalten 

```csharp
Set-SmbClientConfiguration -RequireSecuritySignature $true
```

 oder Auf den Clients RequireSecuritySignature ausschalten 

```csharp
$regpath = "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters"
Set-ItemProperty -Path $regpath RequireSecureNegotiate -Value 0 -Force
```

   Siehe Support Microsoft [System error 2148073478, ...](http://support.microsoft.com/de-de/kb/2686098/en-us)