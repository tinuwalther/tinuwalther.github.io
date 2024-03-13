---
layout: post
title:  "Query VirtualMachines"
author: Tinu
categories: "VMware"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

# Table of Contents

<!-- TOC -->autoauto- [Table of Contents](#table-of-contents)auto- [PowerCLI](#powercli)auto    - [Get-View vs. Get-VM](#get-view-vs-get-vm)auto    - [Fast listing of old Snapshots](#fast-listing-of-old-snapshots)auto- [See also](#see-also)autoauto<!-- /TOC -->

# PowerCLI

## Get-View vs. Get-VM

The performance with Get-View is much better than Get-VM:

````powershell
Connect-ViServer -Server "vcenter.example.com"

$Stopwatch = [System.Diagnostics.Stopwatch]::new()
$Stopwatch.Start()

$OverheadVMs = Get-VM
$OverheadVMs | Get-Snapshot | Select-Object -Property VM, Name, Description

$Stopwatch.Stop()
$Stopwatch.Elapsed.TotalSeconds
````

Output

````Text
0.8237531 seconds
````

````powershell
$Stopwatch = [System.Diagnostics.Stopwatch]::new()
$Stopwatch.Start()

$FastVMs = Get-View -ViewType VirtualMachine
$FastVMs | Select-Object -Property @{N='VM';E={$PSItem.Name}},
 @{N='Description';E={$PSItem.Snapshot.RootSnapshotList[0].Description}}, 
 @{N='Snapshot';E={$PSItem.Snapshot.RootSnapshotList[0].Name}} | Where-Object Snapshot

$Stopwatch.Stop()
$Stopwatch.Elapsed.TotalSeconds
````

Output

````Text
0.1823357 seconds
````

## Fast listing of old Snapshots

````powershell
$Stopwatch = [System.Diagnostics.Stopwatch]::new()
$Stopwatch.Start()

$FastVMs  = Get-View -ViewType VirtualMachine -Filter @{'Config.Template' = 'false'; 'Snapshot' = '.*'}
$Snapshot = $FastVMs | ForEach-Object {
    $CreateTime = Get-Date ($_.Snapshot.RootSnapshotList[0].CreateTime)
    [PSCustomObject][Ordered] @{
        CreateTime       = Get-Date ($CreateTime) -Format 'yyyy-MM-dd HH:mm:ss'
        VMName           = $_.Name
        Snapshot         = $_.Snapshot.RootSnapshotList[0].Name -replace '%2f', '/'
        Description      = $_.Snapshot.RootSnapshotList[0].Description
        TotalDays        = [Math]::Round((New-TimeSpan -Start $CreateTime -End (Get-Date)).TotalDays,0)
        ChildSnapshot    = $_.Snapshot.RootSnapshotList[0].ChildSnapshotList
        ChildDescription = $_.Snapshot.RootSnapshotList[0].ChildSnapshotList.Description
        ChildCreateTime  = $_.Snapshot.RootSnapshotList[0].ChildSnapshotList.CreateTime
    }
} | Sort-Object CreateTime 
$Snapshot.Where( {$_.Description -notmatch 'do not delete' -and $_.TotalDays -gt $day} ) | Format-Table -AutoSize

$Stopwatch.Stop()
$Stopwatch.Elapsed.TotalSeconds
````

# See also

[API Reference](https://developer.vmware.com/apis/vsphere-automation/v7.0U3/) on VMware Developper Documentation.

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]
