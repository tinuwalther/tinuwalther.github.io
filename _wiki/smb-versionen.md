---
title: SMB Versionen
date: '2017-06-28T10:51:19+02:00'
author: Tinu
excerpt: ''
categories:
- Windows Server
tags:
- Security
- SMB
- Windows Server
wordpress_id: 2231
layout: post
permalink: /wiki/smb-versionen/
render_with_liquid: false
---

Aktuell sind verschiedene Attacken mit Ransomware im Umlauf, welche die SMB Version 1 ausnutzen.

## SMB Versionen

- CIFS – The ancient version of SMB that was part of Microsoft **Windows NT 4.0** in 1996. SMB1 supersedes this version.
- **SMB 1.0 (or SMB1) – The version used in Windows 2000, Windows XP, Windows Server 2003 and Windows Server 2003 R2**
- SMB 2.0 (or SMB2) – The version used in Windows Vista (SP1 or later) and **Windows Server 2008**
- SMB 2.1 (or SMB2.1) – The version used in Windows 7 and **Windows Server 2008 R2**
- SMB 3.0 (or SMB3) – The version used in Windows 8 and **Windows Server 2012**
- SMB 3.02 (or SMB3) – The version used in Windows 8.1 and **Windows Server 2012 R2**
 

### Determine whether SMB clients use SMB 1.0

 To determine whether any SMB clients are currently connected to the server running SMB 1.0, type the following script in Windows PowerShell: 

```
Get-SmbSession | Select Dialect,ClientComputerName,ClientUserName | ? Dialect -lt 2
```

 You should run this script repeatedly over the course of a week (multiple times each day) to build an audit trail. You could also run this as a scheduled task 

### SMB Settings auf dem Server auslesen

```
Get-SmbServerConfiguration | Select EnableSMB*
```

 oder 

```
Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" -name SMB*
```

## SMB V1 deaktivieren

 Um SMBv1 auf dem SMB-Server zu aktivieren oder zu deaktivieren, konfigurieren Sie den folgenden Registrierungsschlüssel: 

Registrierungsunterschlüssel: **HKEY\_LOCAL\_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\LanmanServer\\Parameters**Registrierungseintrag: SMB1 REG\_DWORD: 0  = Deaktiviert REG\_DWORD: 1   = Aktiviert Standardwert: 1     = Aktiviert

 Deaktivieren mit PowerShell: 

```
Set-SmbServerConfiguration -EnableSMB1Protocol:$false -Force
```

 oder 

```
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" SMB1 -Type DWORD -Value 0 -Force
```

### Alternative method for customers running Windows 8.1 or Windows Server 2012 R2 and later

 For client operating systems: 

1. Open **Control Panel**, click **Programs**, and then click **Turn Windows features on or off.**
2. In the Windows Features window, clear the **SMB1.0/CIFS File Sharing Support** checkbox, and then click **OK** to close the window.
3. Restart the system.
 
 For server operating systems: 

1. Open **Server Manager** and then click the **Manage** menu and select **Remove Roles and Features**.
2. In the Features window, clear the **SMB1.0/CIFS File Sharing Support** check box, and then click **OK** to close the window.
3. Restart the system.
 
 **Impact of workaround.** The SMBv1 protocol will be disabled on the target system.