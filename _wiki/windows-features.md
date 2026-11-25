---
title: Windows Features
date: '2014-11-30T11:17:36+01:00'
author: Tinu
excerpt: ''
categories:
- Windows Server
tags:
- Features
- Windows Server
wordpress_id: 291
layout: post
permalink: /wiki/windows-features/
render_with_liquid: false
---

# Features auslesen

## Ein Features abfragen

Get-WindowsFeature \| Where-Object {$\_.Name -like "Backup\*"} 

## Mehrere Features abfragen

Get-WindowsFeature \| Where-Object {$\_.Name -like "Desktop\*" -or $\_.Name -like "Web-DAV\*"} 

## Installierte Features auflisten

Get-WindowsFeature \| Where InstallState -like installed 

# Features on Demand

Windows Server Update Services (WSUS) is not configurable as a recovery source for Features on Demand! If you wanted to install some feature like NetFx3 (.NET Framework 3.5), that feature is not included in any edition and is therefore not in the wim at all! 

## GPO

Computer Configuration, Administrative Templates, System, Specify settings for optional component installation and component repair oder wenn da nicht gefunden, dann über All Settings... 

## Registry

```csharp
if (Test-Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\Servicing"){
    Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\Servicing
}
```

### Possible registry values include

Enables use of Windows Update as an installation source, this is the default if nothing is configured. **LocalSourcePath**Specifies location to use for installation source. Can specify more than one source when separated with a ';'. Valid sources include a network folder path or a WIM file (using the syntax wim:&lt;path to wim&gt;:&lt;index&gt;) LocalSourcePath, REG\_EXPAND\_SZ, "wim:c:\\install.wim:2" **RepairContentServerSource**Value 2 will contact Windows Update directly to download repair content instead of Windows Server Update Services (WSUS). **UseWindowsUpdate**Value 2 will prevent the installation from attempting to contact Windows Update/WSUS Servers. UseWindowsUpdate, REG\_DWORD, 2 

## WIM

DISM /online /enable-feature /featurename:WindowsServerBackup /source:wim:c:\\install.wim:2 /limitaccess The **limitaccess** switch will prevent the installation from attempting to contact Windows Update/WSUS Servers. 

### Index

1 = Server Standard Core 2 = Server Standard GUI 3 = Server Datacenter Core 4 = Server Datacenter GUI 

## Example

Voraussetzungen: ISO an Server anhängen Index suchen 

```
dism /get-wiminfo /wimfile:D:\sources\install.wim
Details for image : D:\sources\install.wim
 Index : 2
 Name : Windows Server 2012 R2 SERVERSTANDARD
 Description : Windows Server 2012 R2 SERVERSTANDARD
 Size : 11 676 579 164 bytes
```

WimFile mounten 

```
dism /mount-wim /wimfile:D:/sources/install.wim /index:2 /mountdir:C:/mountdir /ReadOnly
 Mounting image
 [==========================100.0%==========================]
 The operation completed successfully.
```

WimFile unmounten 

```
dism /unmount-wim /mountdir:C:/mountdir /discard
```

Windows Feature .NET Framework 3.5 installieren 

```
Dism /online /enable-feature /featurename:NetFx3 /All /Source:D:\sources\sxs /LimitAccess
Enabling feature(s)
[==========================100.0%==========================]
The operation completed successfully.
```

Windows Feature .NET Environment 3.5 (für Asp .Net) installieren 

```
Dism /online /enable-feature /featurename:WAS-NetFxEnvironment /All /Source:D:\sources\sxs /LimitAccess
Enabling feature(s)
[==========================100.0%==========================]
The operation completed successfully.
```

## PowerShell

Install-WindowsFeature Web-Server -IncludeAllSubFeature -Source D:\\sourses\\sxs  