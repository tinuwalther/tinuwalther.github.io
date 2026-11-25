---
title: VMware vCenter abfragen
date: '2016-09-15T08:42:00+02:00'
author: Tinu
excerpt: Mit PowerCLI auf die VIServer verbinden und alle Windows Systeme abfragen.
categories:
- Virtualisierung
tags:
- PowerCLI
- VMware
image: /assets/wiki/vmware-e1620821111224.png
wordpress_id: 1461
layout: post
permalink: /wiki/vmware-vcenter-abfragen/
render_with_liquid: false
---

Mit den PowerCLI Commandlets kann mit PowerShell VMWare automatisiert werden.

## Connect to VIServer

### VIServer Mode

VIServer Mode von Single auf Multiple switchen, damit auf mehr als nur ein VIServer zugegriffen werden kann.

```
if((Get-PowerCLIConfiguration).DefaultVIServerMode -match 'Single'){
    $DefaultVIServerMode = Set-PowerCLIConfiguration -DefaultVIServerMode Multiple -Confirm:$false -Scope Session 
    ($DefaultVIServerMode | Select Scope,DefaultVIServerMode | Format-Table | Out-String).Trim() | ForEach-Object {
        Write-Host $_ -ForegroundColor Green
    }
}
```

### Connect to multiple VIServers

```
$ConnectToServer = 'vCenter1', 'vCenter2'
$creds = (Get-Credential -Message "Enter the credentials to connect to VIServer" -UserName $($env:USERNAME))

if([String]::IsNullOrEmpty((Get-Module VMware.VimAutomation.Core))){
    Import-Module VMware.VimAutomation.Core
}

Connect-VIServer -Server $ConnectToServer -Credential $creds -WarningAction SilentlyContinue | `
Select Name,User | Format-Table | Out-String | ForEach-Object {Write-Host $_ -ForegroundColor Green}
```

### Define Properties

Properties definieren, welche ausgelesen werden sollen.

```
$VMProperties = @(
    'Name','PowerState','Notes',
    'Guest','NumCpu','CoresPerSocket','MemoryGB',
    'Folder','UsedSpaceGB','ProvisionedSpaceGB','CreateDate'
)
$VMExtensionData = @(
    'Name','Snapshot','RootSnapshot',
    'GuestHeartbeatStatus','OverallStatus','ConfigStatus',
    'RecentTask','TriggeredAlarmState'
)
$VMExtensionDataGuest = @(
    'GuestFamily','GuestFullName','HostName',
    'IpAddress','GuestState','ToolsStatus',
    'ToolsVersionStatus','ToolsVersionStatus2','ToolsRunningStatus',
    'ToolsVersion','ToolsInstallType','AppHeartbeatStatus',
    'GuestKernelCrashed','GuestOperationsReady'
)
```

### Alle Windows Systeme abfragen

Mit PowerCLI alle Windows VMs abfragen

```
$VMName   = Read-Host -message 'Enter a VMName'
$VMFolder = 'Customer A'

$ret = foreach($item in $global:DefaultVIServers){

    # Define the query
    if([String]::IsNullOrEmpty($VMName)){
        $WinVM = Get-Folder $VMFolder -Server $item.Name | Get-VM | Where-Object Guest -match Windows
    }else{
        $WinVM = Get-Folder $VMFolder -Server $item.Name | Get-VM | Where-Object PowerState -match PoweredOn | Where-Object Guest -match Windows | Where-Object Name -match $VMName
    }

    # Loop through data
    foreach($vm in $WinVM){

        "`n$($vm.Name)" | Out-String | ForEach-Object {
            Write-Host $_ -ForegroundColor Cyan
        }

        $DefaultProperties = $vm | Select-Object $VMProperties
        ($DefaultProperties | Format-List * | Out-String).Trim() | ForEach-Object {
            Write-Host $_ -ForegroundColor Green
        }

        "`nExtensionData" | Out-String | ForEach-Object {
            Write-Host $_ -ForegroundColor Cyan
        }

        $ExtendedProperties = $vm.ExtensionData | Select-Object $VMExtensionData
        ($ExtendedProperties | Format-List * | Out-String).Trim() | ForEach-Object {
            Write-Host $_ -ForegroundColor Green
        }

        "`nExtensionDataGuest" | Out-String | ForEach-Object {
            Write-Host $_ -ForegroundColor Cyan
        }

        $ExtendedGuestProperties = $vm.ExtensionData.Guest | Select-Object $VMExtensionDataGuest
        ($ExtendedGuestProperties | Format-List * | Out-String).Trim() | ForEach-Object {
            Write-Host $_ -ForegroundColor Green
        }

        "`nConfigTools" | Out-String | ForEach-Object {
            Write-Host $_ -ForegroundColor Cyan
        }

        $ConfigTools = $vm | ForEach-Object { get-view $_.id } | Select-Object @{Name="ToolsUpgradePolicy"; Expression={$_.config.tools.ToolsUpgradePolicy}} 
        ($ConfigTools | Format-List | Out-String).Trim() | ForEach-Object {
            Write-Host $_ -ForegroundColor Green
        }
    }
}

($ret | Format-Table | Out-String).Trim() | ForEach-Object {
    Write-Host $_ -ForegroundColor Green
}

"Matches found: $($ret.name.Count) PoweredOn Windows VMs in Folder $($Script:VMFolder)" | Out-String | ForEach-Object {
    Write-Host $_ -ForegroundColor Green
}
```

## Disconnect from VIServer

Logoff von allen VIServern.

```
Disconnect-VIServer -Confirm:$false
```

