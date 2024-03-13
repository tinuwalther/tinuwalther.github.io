---
layout: post
title:  "API Virtual Machines"
author: Tinu
categories: "VMware"
tags:   PowerShell News
permalink: /posts/:title:output_ext
---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Virtual Machines](#virtual-machines)
  - [vCenter Login](#vcenter-login)
  - [Get the identifier of a virtual machine by name](#get-the-identifier-of-a-virtual-machine-by-name)
  - [Get properties of the specified virtual machine by id](#get-properties-of-the-specified-virtual-machine-by-id)
- [See also](#see-also)

## Virtual Machines

To list some properties of a virtual machine, you need three steps.

- vCenter Login
- Get the identifier of a virtual machine by name
- Get properties of the specified virtual machine by id

### vCenter Login

For the login to the vCenter Server see [vSphere REST API](https://tinuwalther.github.io/posts/vmwapivcenter.html)

### Get the identifier of a virtual machine by name

To get the identifier of a virtual machine, you have to provide the name of the virtual machine and set it to the filter in the API Url.

````powershell
#region Get the specified VM by name
$vmName = 'tunix666'
$Properties = @{
    Uri             = "https://$($vCenterServer)/api/vcenter/vm?names=$($vmName)"
    Method          = 'Get'
    Headers         = $ApiSessionHeaders
    UseBasicParsing = $true
    ContentType     = 'application/json'
    ErrorAction     = 'Stop'
}
$vmByName = Invoke-RestMethod @Properties
if(!$vmByName){
    Write-Warning "Could not find any virtual machine with name $vmName"
    break
}
#endregion
````

Output VMSummary as PSCustomObject:

````text
memory_size_MiB : 4096
vm              : vm-12293
name            : tunix666
power_state     : POWERED_ON
cpu_count       : 2
````

If you need the VMSummary of all VMs, change the API Url to `https://$($vCenterServer)/api/vcenter/vm`. This will returns information about at most 4000 visible virtual machines in vCenter.

### Get properties of the specified virtual machine by id

To list some properties of a virtual machine, you have to provide the identifier of the virtual machine.

````powershell
#region Get properties of the specified VM by name
$Properties = @{
    Uri             = "https://$($vCenterServer)/api/vcenter/vm/$($vmByName.vm)"
    Method          = 'Get'
    Headers         = $ApiSessionHeaders
    UseBasicParsing = $true
    ContentType     = 'application/json'
    ErrorAction     = 'Stop'
}
$vmProperties = Invoke-RestMethod @Properties
if(!$vmProperties){
    Write-Warning "Could not find any virtual machine with id $($vmByName.vm)"
    break
}
#endregion
````

Output VMInfo as PSCustomObject:

````text
instant_clone_frozen : False
cdroms               : @{16000=}
memory               : @{hot_add_increment_size_MiB=128; size_MiB=4096; hot_add_enabled=True; hot_add_limit_MiB=65536}
disks                : @{2000=}
parallel_ports       :
sata_adapters        : @{15000=}
cpu                  : @{hot_remove_enabled=False; count=2; hot_add_enabled=True; cores_per_socket=1}
scsi_adapters        : @{1000=}
power_state          : POWERED_ON
floppies             :
identity             : @{name=tunix666; instance_uuid=502dd304-3384-a5d7-2abc-4d92b4eee04a; bios_uuid=422df725-aec5-4af1-2b18-c0af354d8c54}
nvme_adapters        :
name                 : tunix666
nics                 : @{4000=}
boot                 : @{delay=0; efi_legacy_boot=False; retry_delay=10000; enter_setup_mode=False; network_protocol=IPV4; type=EFI; retry=False}
serial_ports         :
boot_devices         : {}
guest_OS             : RHEL_8_64
hardware             : @{upgrade_policy=NEVER; upgrade_status=NONE; version=VMX_14}
````

## See also

[API Reference](https://developer.vmware.com/apis/vsphere-automation/v7.0U3/) on VMware Developper Documentation,
[Data Structure VMSummary](https://developer.vmware.com/apis/vsphere-automation/v7.0U3/vcenter/data-structures/VM/Summary/) on VMware Developper Documentation,
[Data Structure VMInfo](https://developer.vmware.com/apis/vsphere-automation/v7.0U3/vcenter/data-structures/VM/Info/) on VMware Developper Documentation.

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]
