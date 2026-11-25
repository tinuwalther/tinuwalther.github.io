---
title: Remote-Session Copy
date: '2017-09-15T21:59:02+02:00'
author: Tinu
excerpt: Mit PowerShell-Remoting muss nicht mehr über das Clipboard von einem Host
  zum anderen kopiert werden.
categories:
- PowerShell
tags:
- Remote Commands
image: /assets/wiki/powershell-1.png
wordpress_id: 2347
layout: post
permalink: /wiki/remote-session-copy/
render_with_liquid: false
---

## Copy over remote Session

Mit PowerShell-Remoting muss nicht mehr über das Clipboard von einem Host zum anderen kopiert werden. 

### TrustedHosts

Als erstes muss der Remote-Host lokal in die TrustedHosts aufgenommen werden: 

```
Set-Item WSMan:\localhost\Client\TrustedHosts -Value '192.168.1.1' -Force
Get-Item WSMan:\localhost\Client\TrustedHosts
```

### Session to Remote-Host

Danach kann eine PSSession zum Remote-Host erstellt werden: 

```
$remoteHost = New-PSSession -ComputerName '192.168.1.1'
$remoteHost | Format-List *
```

### Copy from Remote-Host

Mit dem Parameter FromSession kann vom Remote-Host zum lokalen Host kopiert werden: 

```
Copy-Item -FromSession $remoteHost "D:\Work\DSC\RemoteHost" -Recurse -Destination 'C:\Work\'
```

### Copy to Remote-Host

Mit dem Parameter ToSession kann vom lokalen Host zum Remote-Host kopiert werden: 

```
Copy-Item -ToSession $remoteHost "C:\Work\RemoteHost" -Recurse -Destination 'D:\Work\'
```

### TrustedHosts

Die TrustedHosts-Liste am Ende wieder leeren: 

```
Clear-Item WSMan:\localhost\Client\TrustedHosts -Force
Get-Item WSMan:\localhost\Client\TrustedHosts
```