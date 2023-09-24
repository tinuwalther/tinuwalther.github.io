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

List some properties of all ESXiHost with PowerCLI.

````powershell
Connect-ViServer -Server "vcenter.example.com"

$MgmtNic    = "key-vim.host.VirtualNic-vmk0"
$vMotionNic = "key-vim.host.VirtualNic-vmk1"

$EsxiProperties = @(
    @{N='Name';E={$PSItem.Name}}
    @{N='OverAllStatus';E={$PSItem.OverAllStatus}}
    @{N='Vendor';E={$PSItem.Hardware.SystemInfo.Vendor}}
    @{N='Model';E={$PSItem.Hardware.SystemInfo.Model}}
    @{N='BootTime';E={$PSItem.runtime.BootTime}}
    @{N='Version';E={$PSItem.Config.Product.Version}}
    @{N='Build';E={$PSItem.Config.Product.Build}}
    @{N='PowerState';E={$PSItem.runtime.PowerState}}
    @{N='StandbyMode';E={$PSItem.runtime.StandbyMode}}
    @{N='MaintenanceMode'; E={$PSItem.runtime.InMaintenanceMode}}
    @{
        N='IPv4Address'
        E={($PSItem.Config.Network.Vnic).Where({$_.Key -eq $MgmtNic}).Spec.Ip[0].IpAddress}}
    @{
        N='SubnetMask'
        E={($_.Config.Network.Vnic).Where({$_.Key -eq $MgmtNic}).Spec.Ip[0].SubnetMask}}
    @{
        N='vMotionIPv4Address'
        E={($PSItem.Config.Network.Vnic).Where({$_.Key -eq $vMotionNic}).Spec.Ip[0].IpAddress}
    }
    @{
        N='vMotionSubnetMask'
        E={($PSItem.Config.Network.Vnic).Where({$_.Key -eq $vMotionNic}).Spec.Ip[0].SubnetMask}
    }
    @{
        N='Cluster'
        E={(Get-View -ViewType ClusterComputeResource -Filter @{"Host" = $($PSItem.Config.Host.Value)}).Name}
    }
    @{N='VMs';E={$PSItem.Vm.Count}}
)

$AllVMHost = Get-View -ViewType HostSystem
$AllVMHost | Select-Object $EsxiProperties
````

Output

````Text
Name               : esxi002.example.com
OverAllStatus      : red
Vendor             : HPE
Model              : Synergy 480 Gen10
BootTime           : 22.09.2023 13:49:18
Version            : 7.0.3
Build              : 20328353
PowerState         : poweredOn
StandbyMode        : none
MaintenanceMode    : True
IPv4Address        : 10.x.y.z
SubnetMask         : 255.255.255.0
vMotionIPv4Address : 10.x.y.z
vMotionSubnetMask  : 255.255.255.0
Cluster            : Linux
VMs                : 20
````

# ESXCLI

The ESXCLI tool allows for remote management of ESXi hosts by using the ESXCLI command set.

## Native ESXCLI

You can use the native ESXCLI over ssh on ESXiHosts.

````bash
esxcli system boot device get
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
