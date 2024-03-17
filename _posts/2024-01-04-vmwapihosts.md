---
layout: post
title:  "API ESXi Hosts"
author: Tinu
categories: "VMware"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [ESXi Hosts](#esxi-hosts)
  - [vCenter Login](#vcenter-login)
  - [Get HostSummary of the specified ESXi Host by name](#get-hostsummary-of-the-specified-esxi-host-by-name)
- [See also](#see-also)

## ESXi Hosts

To list some properties of a ESXi Hosts, you need three steps.

- vCenter Login
- Get HostSummary of the specified ESXi Host by name

### vCenter Login

For the login to the vCenter Server see [vSphere REST API](https://tinuwalther.github.io/posts/vmwapivcenter.html)

### Get HostSummary of the specified ESXi Host by name

To get the identifier of an ESXi Host, you have to provide the name of the ESXi Host and set it to the filter in the API Url.

````powershell
#region Get the specified ESXi Host by name
$esxName = 'tunix666.companx.local'
$Properties = @{
    Uri             = "https://$($vCenterServer)/api/vcenter/host?names=$($esxName)"
    Method          = 'Get'
    Headers         = $ApiSessionHeaders
    UseBasicParsing = $true
    ContentType     = 'application/json'
    ErrorAction     = 'Stop'
}
$esxByName = Invoke-RestMethod @Properties
if(!$esxByName){
    Write-Warning "Could not find any ESXi Host with name $esxName"
    break
}
#endregion
````

Output HostSummary as PSCustomObject:

````text
host             : host-1024
name             : tunix666.companx.local
connection_state : CONNECTED
power_state      : POWERED_ON
````

If you need the HostSummary of all ESXi Hosts, change the API Url to `https://$($vCenterServer)/api/vcenter/host`. This will returns information about at most 2500 visible ESXi Hosts in vCenter.

## See also

[API Reference](https://developer.vmware.com/apis/vsphere-automation/v7.0U3/) on VMware Developper Documentation,
[Data Structure HostSummary](https://developer.vmware.com/apis/vsphere-automation/v7.0U3/vcenter/data-structures/Host/Summary/) on VMware Developper Documentation,
