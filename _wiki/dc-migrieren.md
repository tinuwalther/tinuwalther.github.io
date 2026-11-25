---
title: Domain Controller migrieren
date: '2015-02-27T14:42:41+01:00'
author: Tinu
excerpt: ''
categories:
- Active Directory
tags:
- Domain Controller
wordpress_id: 816
layout: post
permalink: /wiki/dc-migrieren/
render_with_liquid: false
---

## Domain Controller Installieren

### Windows Features installieren

```csharp
Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools
```

### DC promoten

 Check Server for DC-installation 

```csharp
Test-ADDSDomainControllerInstallation -DomainName $domain
```

 Install additional Domain Controller 

```csharp
$domain = ""; $site = ""; $repldc = ""
Install-ADDSDomainController -InstallDns -DomainName $domain -SiteName $site`
-ReplicationSourceDC $repldc -SafeModeAdministratorPassword -NoRebootOnCompletion` 
-DatabasePath "E:\NTDS" -LogPath "E:\NTDS" -SysvolPath "E:\SYSVOL"
```

### FSMO Roles transfer

 Transfer forest-wide FSMO Roles to Target DC (beide Rollen sollten auf dem selben DC sein). 

```csharp
$targetdc = ""
Move-ADDirectoryServerOperationMasterRole -Identity $targetdc` 
-OperationMasterRole SchemaMaster
Move-ADDirectoryServerOperationMasterRole -Identity $targetdc`
-OperationMasterRole DomainNamingMaster

```

 Transfer domain-wide FSMO Roles to Target DC (alle Rollen sollten auf dem selben DC sein). 

```csharp
$targetdc = ""
Move-ADDirectoryServerOperationMasterRole -Identity $targetdc` 
-OperationMasterRole PDCEmulator
Move-ADDirectoryServerOperationMasterRole -Identity $targetdc` 
-OperationMasterRole RIDMaster
Move-ADDirectoryServerOperationMasterRole -Identity $targetdc` 
-OperationMasterRole InfrastructureMaster

```

## DC de-installieren

 Der alte Domain Controller kann nun heruntergestuft und aus dem AD genommen werden. 

### DC demoten

```csharp
Uninstall-ADDSDomainController -NoRebootOnCompletion
```