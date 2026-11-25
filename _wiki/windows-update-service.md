---
title: Windows Update Service
date: '2017-07-27T11:33:48+02:00'
author: Tinu
excerpt: ''
categories:
- Windows Server
tags:
- Security
- Windows Server
- Windows Update Service
wordpress_id: 2294
layout: post
permalink: /wiki/windows-update-service/
render_with_liquid: false
---

## Assembly

 Lädt eine Assembly aus dem Anwendungsverzeichnis oder dem globalen Assemblycache. 

```
[void][reflection.assembly]::LoadWithPartialName("Microsoft.UpdateServices.Administration")
```

 [Microsoft.UpdateServices.Administration Namespace](https://msdn.microsoft.com/en-us/library/microsoft.updateservices.administration(v=vs.85).aspx)

### Downstreamserver auflisten

```
$Upstreamserver = "$($env:COMPUTERNAME).$($env:USERDNSDOMAIN)"
$ret = @()
[void][reflection.assembly]::LoadWithPartialName("Microsoft.UpdateServices.Administration")
$wsus = [Microsoft.UpdateServices.Administration.AdminProxy]::getUpdateServer($Upstreamserver,$false, 8530)
$wsus.GetDownstreamServers() | %{
    $obj = [PSCustomObject]@{
        UpdateServer              = $_.UpdateServer
        DownstreamServer          = $_.FullDomainName
        LastSyncTime              = $_.LastSyncTime
        ParentServerId            = $_.ParentServerId
        SyncsFromDownstreamServer = $_.SyncsFromDownstreamServer
        LastRollupTime            = $_.LastRollupTime
        Version                   = $_.Version
        IsReplica                 = $_.IsReplica
    }
    $ret += $obj
}
$ret | ft
```

## Cmdlets Windows Server 2012 R2

```
Get-Command -Module UpdateServices

Add-WsusComputer
Approve-WsusUpdate
Deny-WsusUpdate
Get-WsusClassification
Get-WsusComputer
Get-WsusProduct
Get-WsusServer
Get-WsusUpdate
Invoke-WsusServerCleanup
Set-WsusClassification
Set-WsusProduct
Set-WsusServerSynchronization
```

### Invoke-WSUSServerCleanup

```
Get-WsusServer | Invoke-WsusServerCleanup -CleanupObsoleteComputers –CleanupObsoleteUpdates
```

### Alle Computer Gruppen auflisten

```
[reflection.assembly]::LoadWithPartialName("Microsoft.UpdateServices.Administration") 
$wsus = [Microsoft.UpdateServices.Administration.AdminProxy]::getUpdateServer() 
$ret  = @()
foreach( $group in $wsus.GetComputerTargetGroups() ) 
{ 
    $obj = [PSCustomObject]@{
        Group = $group.Name
        Members = $group.GetComputerTargets().Count
    }
    $ret += $obj
} 
$ret | Sort Group | ft -AutoSize
```