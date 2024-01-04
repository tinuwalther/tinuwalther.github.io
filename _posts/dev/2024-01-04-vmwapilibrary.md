---
layout: post
title:  "Content Library"
author: Tinu
categories: "VMware"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Rest API](#rest-api)
  - [Login to vCenter](#login-to-vcenter)
  - [Get the VM for cloning](#get-the-vm-for-cloning)
  - [Get the Content Library](#get-the-content-library)
  - [Create the Library Item](#create-the-library-item)
- [See also](#see-also)

# Rest API

Before you can execute a Rest API call, be sure that you have configured the SSL:

````powershell
#region SslProtocol
$SslProtocol      = 'Tls12'
$CurrentProtocols = ([System.Net.ServicePointManager]::SecurityProtocol).toString() -split ', '
if (!($SslProtocol -in $CurrentProtocols)){
    [System.Net.ServicePointManager]::SecurityProtocol += [System.Net.SecurityProtocolType]::$($SslProtocol)
}
#endregion
````

Define your vCenter Server:

````powershell
# Define your vCenter Server and set the credentials
$vCenterServer  = 'vCenterServer.company.local'
$ApiCredentials = Get-Credential -Message 'vCenter Credentials' -UserName "$($env:USERDOMAIN)\$($env:USERNAME)"
````

## Login to vCenter

Login to vCenter and get an API Token:

````powershell
#region Login vCenter
#Required basic authentication header. Takes in a Base64 encoded value of your username:password
$pair = "$($ApiCredentials.UserName):$($ApiCredentials.GetNetworkCredential().Password)"

#Encode the string to the RFC2045-MIME variant of Base64, except not limited to 76 char/line.
$bytes  = [System.Text.Encoding]::ASCII.GetBytes($pair)
$base64 = [System.Convert]::ToBase64String($bytes)

#Create the Auth value as the method, a space, and then the encoded pair Method Base64String
$basicAuthValue = "Basic $base64"
#Create the header Authorization
$headers = @{
    'Content-Type'  = 'application/json'
    'Authorization' = $basicAuthValue
}

$Properties = @{
    Uri             = "https://$($vCenterServer)/api/session"
    Method          = 'Post'
    Headers         = $headers
    UseBasicParsing = $true
    ContentType     = 'application/json'
    ErrorAction     = 'Stop'
}

$Token = Invoke-RestMethod @Properties
#endregion
````

````powershell
#region Token for authorization
$headers = @{
    'Content-Type'          = 'application/json'
    'vmware-api-session-id' = $Token
}
#endregion
````

## Get the VM for cloning

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
    Headers         = $headers
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
    Headers         = $headers
    UseBasicParsing = $true
    ContentType     = 'application/json'
    ErrorAction     = 'Stop'
}
$vm = Invoke-RestMethod @Properties
$libraryObject | Add-Member -MemberType NoteProperty -Name 'runtime' -Value $(Get-Date -f 'yyyy-MM-dd HH:mm:ss.fff') -Force
$libraryObject | Add-Member -MemberType NoteProperty -Name 'vmName' -Value $($vm.name)
#endregion
````

## Get the Content Library

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
    Headers         = $headers
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

## Create the Library Item

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
    Headers         = $headers
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

List the referenceObject:

````powershell
$libraryObject | Format-List
````

List the Content Library Item:

````powershell
$Properties = @{
    Uri             = "https://$($vCenterServer)/api/content/library/item/$($libraryObject.libraryItemId)"
    Method          = 'Get'
    Headers         = $headers
    UseBasicParsing = $true
    ContentType     = 'application/json'
    ErrorAction     = 'Stop'
}
$myItem = Invoke-RestMethod @Properties
$myItem | Format-List
````

# See also

[API Reference](https://developer.vmware.com/apis/vsphere-automation/v7.0U3/) on VMware Developper Documentation.

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]
