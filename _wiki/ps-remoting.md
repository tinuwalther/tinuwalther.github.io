---
title: PS-Remoting
date: '2017-06-15T19:30:35+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Remote Commands
wordpress_id: 2047
layout: post
permalink: /wiki/ps-remoting/
render_with_liquid: false
---

PowerShell 2.0 or later

## WinRM

 WSMan-Protocol must have a listener configured, an inbound firewall rule for TCP port 5985/86 must be enabled, and the WinRM service must be started. 

```
winrm quickconfig
```

 Enabled on Windows Server 2012 Operating Systems or later. Disabled by default on all Client and earlier Server OS’s. 

```
Enable-PSRemoting -Force
```

## Trusted-Hosts

 Computers in a workgroup, or different domain, should be added to allow authentication. 

```
Get-Item WSMan:\localhost\Client\TrustedHosts
Set-Item WSMan:\localhost\Client\TrustedHosts -value [IP, Computer, Domain]
Restart-Service WinRm
```

## Remoting-Cmdlets

```
Get-Services -ComputerName ...
```

## Enter-PSSession

 The **Enter-PSSession** cmdlet starts an interactive session with a single remote computer. During the session, the commands that you type run on the remote computer, just as though you were typing directly on the remote computer. You can have only one interactive session at a time. Typically, you use the **ComputerName** parameter to specify the name of the remote computer. However, you can also use a session that you create by using the **New-PSSession** cmdlet for the interactive session. However, you cannot use the Disconnect-PSSession, Connect-PSSession, or Receive-PSSession cmdlets to disconnect from or re-connect to an interactive session. 

### -EnableNetworkAccess

 Indicates that this cmdlet adds an interactive security token to loopback sessions. The interactive token lets you run commands in the loopback session that get data from other computers. For example, you can run a command in the session that copies XML files from a remote computer to the local computer. 

### -RunAsAdministrator

 Indicates that the **PSSession** runs as administrator. 

### Exit-PSSession

 To end the interactive session and disconnect from the remote computer, use the Exit-PSSession cmdlet, or type "exit". 

```
Enter-PSSession -ComputerName ...
```

 *Quelle: MSDN*

## Invoke-Command

 The **Invoke-Command** cmdlet runs commands on a local or remote computer and returns all output from the commands, including errors. By using a single **Invoke-Command** command, you can run commands on multiple computers. To run a single command on a remote computer, use the *ComputerName* parameter. To run a series of related commands that share data, use the New-PSSession cmdlet to create a **PSSession** (a persistent connection) on the remote computer, and then use the *Session* parameter of **Invoke-Command** to run the command in the PSSession. To run a command in a disconnected session, use the *InDisconnectedSession* parameter. To run a command in a background job, use the *AsJob* parameter. You can also use **Invoke-Command** on a local computer to evaluate or run a string in a script block as a command. Windows PowerShell converts the script block to a command and runs the command immediately in the current scope, instead of just echoing the string at the command line. To start an interactive session with a remote computer, use the Enter-PSSession cmdlet. To establish a persistent connection to a remote computer, use the **New-PSSession** cmdlet. 

```
Invoke-Command -ComputerName ...
```

 *Quelle: MSDN*

### -FilePath

 Es kann ein PowerShell-Script (Pfad) angegeben werden. Invoke-Command -ComputerName BigServer -FilePath "C:\\Services.ps1" 

### -ScriptBlock

 Es kann ein PowerShell-ScriptBlock mitgegeben werden. Invoke-Command -ComputerName BigServer -ScriptBlock {Get-Culture}