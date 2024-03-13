---
layout: post
title:  "Query ESXiHosts"
author: Tinu
categories: "VMware"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [PowerCLI](#powercli)
- [ESXCLI](#esxcli)
  - [Native ESXCLI](#native-esxcli)
  - [Get-EsxCli](#get-esxcli)
- [See also](#see-also)

## PowerCLI

List some properties of all ESXiHost with PowerCLI in a fast way.

````powershell
# Connect to your VIServer
Connect-ViServer -Server "vcenter.example.com"

# Enable StopWatch to calculate the runtime
# $Stopwatch = [System.Diagnostics.Stopwatch]::new()
# $Stopwatch.Start()

# Specify the Management and vMotion Nic
$MgmtNic    = "key-vim.host.VirtualNic-vmk0"
$vMotionNic = "key-vim.host.VirtualNic-vmk1"

# Specify the Hardware properties
$Hardware = @(
    @{
        N='Vendor'
        E={
            $PSItem.Hardware.SystemInfo.Vendor
        }
    }
    @{
        N='Model'
        E={
            $PSItem.Hardware.SystemInfo.Model
        }
    }
)

# Specify the Runtime properties
$Runtime = @(
    @{
        N='BootTime'
        E={
            $PSItem.runtime.BootTime
        }
    }
    @{
        N='PowerState'
        E={
            $PSItem.runtime.PowerState
        }
    }
    @{
        N='StandbyMode'
        E={
            $PSItem.runtime.StandbyMode
        }
    }
    @{
        N='MaintenanceMode'
        E={
            $PSItem.runtime.InMaintenanceMode
        }
    }
)

# Specify the Network properties
$Network = @(
    @{
        N='IPv4Address'
        E={
            ($PSItem.Config.Network.Vnic).Where({$_.Key -eq $MgmtNic}).Spec.Ip[0].IpAddress
        }
    }
    @{
        N='SubnetMask'
        E={
            ($PSItem.Config.Network.Vnic).Where({$_.Key -eq $MgmtNic}).Spec.Ip[0].SubnetMask
        }
    }
    @{
        N='DefaultGateway'
        E={
            $PSItem.Config.Network.IpRouteConfig.DefaultGateway
        }
    }
    @{
        N='vMotionIPv4Address'
        E={
            ($PSItem.Config.Network.Vnic).Where({$_.Key -eq $vMotionNic}).Spec.Ip[0].IpAddress
        }
    }
    @{
        N='vMotionSubnetMask'
        E={
            ($PSItem.Config.Network.Vnic).Where({$_.Key -eq $vMotionNic}).Spec.Ip[0].SubnetMask
        }
    }
    @{
        N='Network'
        E={
            $VMHost.Network.Value | ForEach-Object {
                (Get-View -ViewType Network | Where-Object Key -eq $PSItem).Name
            }
        }
    }
)

# Specify the Product properties
$Product = @(
    @{
        N='Version'
        E={
            $PSItem.Config.Product.Version
        }
    }
    @{
        N='Build'
        E={
            $PSItem.Config.Product.Build
        }
    }
)

# Specify the general properties
$Properties = @(
    @{
        N='Name'
        E={
            $PSItem.Name
        }
    }
    @{
        N='OverAllStatus'
        E={
            $PSItem.OverAllStatus
        }
    }
    @{
        N='NtpServer'
        E={
            $PSItem.Config.DateTimeInfo.NtpConfig.Server
        }
    }
    @{
        N='VM'
        E={
            $VMHost.Vm.Value | ForEach-Object {
                (Get-View -ViewType VirtualMachine | Where-Object MoRef -match $PSItem).Name
            }
        }
    }
    @{
        N='Cluster'
        E={
            (Get-View -ViewType ClusterComputeResource -Filter @{"Host" = $($PSItem.Config.Host.Value)}).Name
        }
    }
    @{
        N='Datastore'
        E={
            $VMHost.Datastore.Value | ForEach-Object {
                (Get-View -ViewType Datastore | Where-Object MoRef -match $PSItem).Name
            }
        }
    }
)

# Get all or one ESXiHost
$VMHost = Get-View -ViewType HostSystem #-Filter @{"Name" = "esxi002.example.com"}
# Display the specified properties
$output = $VMHost | Select-Object @($Properties + $Product + $Hardware + $Runtime + $Network)
$output

# Enable StopWatch to calculate the runtime
# $Stopwatch.Stop()
# $Stopwatch.Elapsed.TotalSeconds
````

Output

````Text
Name               : esxi002.example.com
OverAllStatus      : red
Vendor             : HPE
Model              : Synergy 480 Gen10
NtpServer          : {ntp1.example.com, ntp2.example.com}
BootTime           : 22.09.2023 13:49:18
Version            : 7.0.3
Build              : 20328353
PowerState         : poweredOn
StandbyMode        : none
MaintenanceMode    : True
IPv4Address        : 10.x.y.z
SubnetMask         : 255.255.255.0
DefaultGateway     : 10.x.y.z
vMotionIPv4Address : 10.x.y.z
vMotionSubnetMask  : 255.255.255.0
Cluster            : Linux
VM                 : {...}
Network            : {...}
Datastore          : {...}
````

There are a lot of more properties, which you can define. Enter $VMHost. and navigate to the property that you need.

## ESXCLI

The ESXCLI tool allows for remote management of ESXi hosts by using the ESXCLI command set.

### Native ESXCLI

You can use the native ESXCLI over ssh on ESXiHosts.

````bash
esxcli system boot device get
````

### Get-EsxCli

If the ESXiHost is connected to a vCenter, then you can use ESXCLI as PowerShell command.

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
    $EsxCli.hardware.Power.policy.set.Invoke(@{id="2"})
}
````

## See also

[ESXCLI](https://developer.vmware.com/web/tool/7.0/esxcli) on VMware Developper Documentation.  
[How to use ESXCLI v2 Commands in PowerCLI](https://www.virten.net/2016/11/how-to-use-esxcli-v2-commands-in-powercli/) on virten.net.

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]
