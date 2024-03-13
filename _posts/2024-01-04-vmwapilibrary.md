---
layout: post
title:  "API Content Library"
author: Tinu
categories: "VMware"
tags:   PowerShell News
permalink: /posts/:title:output_ext
---

## Table of Contents

- [Table of Contents](#table-of-contents)
  - [vCenter Login](#vcenter-login)
  - [Get the VM for cloning](#get-the-vm-for-cloning)
  - [Get the Content Library](#get-the-content-library)
  - [Create the Library Item](#create-the-library-item)
- [See also](#see-also)

### vCenter Login

For the login to the vCenter Server see [vSphere REST API](https://tinuwalther.github.io/posts/vmwapivcenter.html)

### Get the VM for cloning

Clone a virtual machine as OVF-Template in a Content Library.

````powershell
# Create an empty reference object
$libraryObject = New-Object PSObject
````

````powershell
#region Get the specified VM by name
$vmName = 'TPL-RHEL8'
$Properties = @{
    Uri             = "https://$($vCenterServer)/api/vcenter/vm?names=$($vmName)"
    Method          = 'Get'
    Headers         = $ApiSessionHeaders
    UseBasicParsing = $true
    ContentType     = 'application/json'
    ErrorAction     = 'Stop'
}
$vm = Invoke-RestMethod @Properties
if(!$vm){
    Write-Warning "Could not find any virtual machine with name $vmName"
    break
}
$libraryObject | Add-Member -MemberType NoteProperty -Name 'runtime' -Value $(Get-Date -f 'yyyy-MM-dd HH:mm:ss.fff') -Force
$libraryObject | Add-Member -MemberType NoteProperty -Name 'vmId' -Value $($vm.vm) -Force

$Properties = @{
    Uri             = "https://$($vCenterServer)/api/vcenter/vm/$($libraryObject.vmId)"
    Method          = 'Get'
    Headers         = $ApiSessionHeaders
    UseBasicParsing = $true
    ContentType     = 'application/json'
    ErrorAction     = 'Stop'
}
$vm = Invoke-RestMethod @Properties
$libraryObject | Add-Member -MemberType NoteProperty -Name 'runtime' -Value $(Get-Date -f 'yyyy-MM-dd HH:mm:ss.fff') -Force
$libraryObject | Add-Member -MemberType NoteProperty -Name 'vmName' -Value $($vm.name)
#endregion
````

### Get the Content Library

Get the id of the target Content Library:

````powershell
#region Get the specified Content Library by name
$librarySpec = @{
    "name" = "ContentLibrary"
    "type" = "LOCAL"
}

$Properties = @{
    Uri             = "https://$($vCenterServer)/api/content/library?action=find"
    Method          = 'Post'
    Headers         = $ApiSessionHeaders
    Body            = $librarySpec | ConvertTo-Json
    UseBasicParsing = $true
    ContentType     = 'application/json'
    ErrorAction     = 'Stop'
}
$libraryId = Invoke-RestMethod @Properties
if(!$libraryId){
    Write-Warning "Could not find any Content Library with name $($librarySpec.name)"
    break
}
$libraryObject | Add-Member -MemberType NoteProperty -Name 'runtime' -Value $(Get-Date -f 'yyyy-MM-dd HH:mm:ss.fff') -Force
$libraryObject | Add-Member -MemberType NoteProperty -Name 'libraryId' -Value $($libraryId)
$libraryObject | Add-Member -MemberType NoteProperty -Name 'libraryName' -Value $($librarySpec.name)
#endregion
````

### Create the Library Item

Clone the virtual machine as OVF-Template in the Content Library:

````powershell
#region Create Library Item
$libraryItemSpec = @{
    "create_spec"= @{
        "name" = "$($libraryObject.vmName)_OVF"
        "description" = "Description to use in the OVF descriptor stored in the library item. If unset, the server will use source’s current annotation."
    }
    "source"= @{
        "id" = "$($libraryObject.vmId)"
        "type" = "VirtualMachine"
    }
    "target"= @{
        "library_id" = "$($libraryObject.libraryId)"
    }
}

$Properties = @{
    Uri             = "https://$($vCenterServer)/api/vcenter/ovf/library-item"
    Method          = 'Post'
    Headers         = $ApiSessionHeaders
    Body            = $libraryItemSpec | ConvertTo-Json
    UseBasicParsing = $true
    ContentType     = 'application/json'
    ErrorAction     = 'Stop'
}
$libraryItem = Invoke-RestMethod @Properties
$libraryObject | Add-Member -MemberType NoteProperty -Name 'runtime' -Value $(Get-Date -f 'yyyy-MM-dd HH:mm:ss.fff') -Force
if($libraryItem.succeeded){
    $libraryObject | Add-Member -MemberType NoteProperty -Name 'libraryItemId' -Value $($libraryItem.'ovf_library_item_id')
}else{
    Write-Warning "$($libraryItem.error.errors.error.'error_type'), $($libraryItem.error.errors.error.messages.default_message)"
}
$libraryObject | Add-Member -MemberType NoteProperty -Name 'libraryItemSucceeded' -Value $($libraryItem.succeeded) -Force
$libraryObject | Add-Member -MemberType NoteProperty -Name 'libraryItemError' -Value $($libraryItem.error) -Force
#endregion
````

List the reference object:

````powershell
$libraryObject | Format-List
````

List the Content Library Item:

````powershell
$Properties = @{
    Uri             = "https://$($vCenterServer)/api/content/library/item/$($libraryObject.libraryItemId)"
    Method          = 'Get'
    Headers         = $ApiSessionHeaders
    UseBasicParsing = $true
    ContentType     = 'application/json'
    ErrorAction     = 'Stop'
}
$myItem = Invoke-RestMethod @Properties
$myItem | Format-List
````

## See also

[API Reference](https://developer.vmware.com/apis/vsphere-automation/v7.0U3/) on VMware Developper Documentation.

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]
