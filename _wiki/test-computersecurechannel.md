---
title: Test-ComputerSecureChannel
date: '2018-07-20T10:16:39+02:00'
author: Tinu
excerpt: Mit PowerShell den Secure Channel zwischen einem Computers und seiner Domäne
  prüfen und reparieren.
categories:
- PowerShell
tags:
- Active Directory
image: /assets/wiki/powershell-1.png
wordpress_id: 2495
layout: post
permalink: /wiki/test-computersecurechannel/
render_with_liquid: false
---

## Tests and repairs the secure channel

Im Systemlog Event ID 5719 Source NETLOGON und 7043 This cmdlet works much like NetDom.exe. Both NetDom and Test-ComputerSecureChannel use the NetLogon service to perform the actions. Test a channel between the local computer and a domain controller 

```
Test-ComputerSecureChannel
```

Reset the channel between the local computer and its domain **PowerShell fix repair The trust relationship between this workstation and the primary domain failed**

```
$DomJoinCreds = Get-Credential -message 'Enter credentials of a user with join-domain permissions'
Test-ComputerSecureChannel -Repair -Credential $DomJoinCreds
```

Display detailed information about the test 

```
Test-ComputerSecureChannel -verbose
```

[More information](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.management/test-computersecurechannel?view=powershell-5.1)