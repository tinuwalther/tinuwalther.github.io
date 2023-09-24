---
layout: post
title:  "Query ESXiHosts"
author: Tinu
categories: "VMware"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

# Table of Contents

<!-- TOC -->

- [Table of Contents](#table-of-contents)
- [PowerCLI](#powercli)
- [ESXCLI](#esxcli)
    - [Native ESXCLI](#native-esxcli)
    - [Get-EsxCli](#get-esxcli)
- [See also](#see-also)

<!-- /TOC -->

# PowerCLI

List some properties from an ESXiHost with PowerCLI.

````powershell
Connect-ViServer -Server "vcenter.example.com"

$AllVMHost = Get-View -ViewType HostSystem
$AllVMHost | Select-Object -Property Name,  
 @{N='BootTime';E={$PSItem.runtime.BootTime}}, 
 @{N='PowerState';E={$PSItem.runtime.PowerState}}, 
 @{N='StandbyMode';E={$PSItem.runtime.StandbyMode}}, 
 @{N='MaintenanceMode';E={$PSItem.runtime.InMaintenanceMode}}},
 @{N='IPv4Address';E={($PSItem.Config.Network.Vnic).Where({$_.Key -eq "key-vim.host.VirtualNic-vmk0"}).Spec.Ip[0].IpAddress}}
````
Output

````Text
Name                  BootTime            PowerState StandbyMode MaintenanceMode IPv4Address 
----                  --------            ---------- ----------- --------------- ----------- 
esx703.example.com  27.06.2023 20:35:05  poweredOn none                  False 10.x.y.z
esx704.example.com  15.06.2023 14:38:53  poweredOn none                  False 10.x.y.z
esx793.example.com  24.08.2023 14:47:28  poweredOn none                  False 10.x.y.z
esx790.example.com  25.08.2023 06:56:17  poweredOn none                  False 10.x.y.z
esx791.example.com  25.08.2023 06:57:17  poweredOn none                  False 10.x.y.z
esx792.example.com  25.08.2023 07:04:31  poweredOn none                  False 10.x.y.z
esx002.example.com  22.09.2023 13:49:18  poweredOn none                   True 10.x.y.z
````

# ESXCLI

The ESXCLI tool allows for remote management of ESXi hosts by using the ESXCLI command set.

## Native ESXCLI

You can use the native ESXCLI over ssh on ESXiHosts.

````bash
system boot device get
````

## Get-EsxCli

You can use ESXCLI as PowerShell command.

````powershell
Connect-ViServer -Server "vcenter.example.com"

$EsxCli = Get-EsxCli -VMHost "esx01.example.com" -V2
$EsxCli.hardware.Power.policy.get.Invoke()
````

Output

````Text
Id Name     ShortName
-- ----     ---------
2  Balanced dynamic
````

Example: Update the Power policy settings on all host to balanced.

````powershell
Connect-ViServer -Server "vcenter.example.com"
$AllVMHost = Get-View -ViewType HostSystem
foreach($item in $AllVMHost){
    $EsxCli = Get-EsxCli -VMHost $item.Name -V2
    $EsxCli.hardware.Power.policy.set.Invoke(@{id="2")})
}
````

# See also

[ESXCLI](https://developer.vmware.com/web/tool/7.0/esxcli) on VMware Developper Documentation.

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]
