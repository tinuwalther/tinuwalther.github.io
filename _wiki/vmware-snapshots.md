---
title: VMware Snapshots
date: '2016-07-21T07:17:00+02:00'
author: Tinu
excerpt: Mit PowerCLI auf die VIServer verbinden und Snapshots erstellen und löschen.
categories:
- Virtualisierung
tags:
- PowerCLI
- VMware
image: /assets/wiki/vmware-e1620821111224.png
wordpress_id: 1476
layout: post
permalink: /wiki/vmware-snapshots/
render_with_liquid: false
---

Mit PowerCLI auf VMware Snapshots erstellen oder löschen.

## Snapshot erstellen

Function Snapshot erstellen.

```
function Create-VMSnapshot{
    [CmdletBinding()]
    param(
       [Parameter(Mandatory = $true)]
       [String]$vmname,

       [Parameter(Mandatory = $true)]
       [String]$snapshotname,

       [Parameter(Mandatory = $true)]
       [String]$snapshotdescription
    )
    $ret = $null
    $function = $($MyInvocation.MyCommand.Name)
    Write-Verbose "Running $function"
    try
    {
        New-Snapshot -VM $vmname -Name $snapshotname -Description $snapshotdescription -Quiesce
        $ret = Get-Snapshot -VM $vmname | Select-Object VM,Created,Name,Description,PowerState
    }
    catch{
        Write-Verbose "Error on New-Snapshot for $($vmname): $($_.Exception.Message)" -Verbose
        $error.Clear()
    }
    return $ret
}
```

## Snapshot löschen

Function Snapshot löschen.

```
function Delete-VMSnapshot{
    [CmdletBinding()]
    param(
       [Parameter(Mandatory = $true)]
       [String]$vmname
    )
    $function = $($MyInvocation.MyCommand.Name)
    $ret = @()
    Write-Verbose "Running $function"
    try
    {
        Get-Snapshot -VM $vmname |% {
            Write-Verbose "Process Remove-Snapshot on $($vmname)" -Verbose
            $ret += Remove-Snapshot -Snapshot $_ -RemoveChildren -Confirm
        }
    }
    catch [Exception]
    {
        Write-Verbose "Error on New-Snapshot for $($vmname): $($_.Exception.Message)" -Verbose
        $error.Clear()
    }
    return $ret
}
```

## Aufruf der Functions

Aufruf der Functions und abspeichern als CSV-file.

```
$action           = 'create | delete'
$path             = 'C:\Temp\Snapshots'
$snapshots        = @()
$snapshotdate     = $(Get-Date -Format 'yyyyMMdd-HHmm')
$snapshotuser     = 'Automation'

if($action -like 'create'){
    $snapshots += Create-VMSnapshot -vmname 'VirtualMachine1' -snapshotname "$($snapshotdate)_$($snapshotuser)" -snapshotdescription "$($snapshotuser), Before MS Patching, $($snapshotdate)"
}
if($action -like 'delete'){
    $snapshots += Delete-VMSnapshot -vmname 'VirtualMachine1'
}
$snapshots | Export-Csv -Path "$($path)\VM-Snapshots.csv" -NoTypeInformation -Delimiter ';' -Force

```

