---
layout: post
title:  "Query VirtualMachines"
author: Tinu
categories: "VMware"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

# Table of Contents

<!-- TOC -->

- [Table of Contents](#table-of-contents)
- [PowerCLI](#powercli)
    - [Get-View vs. Get-VM](#get-view-vs-get-vm)
- [See also](#see-also)

<!-- /TOC -->

# PowerCLI

## Get-View vs. Get-VM

The performance wiht Get-View is much better than Get-VM:

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

# See also

[API Reference](https://developer.vmware.com/apis/vsphere-automation/v7.0U3/) on VMware Developper Documentation.

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]
