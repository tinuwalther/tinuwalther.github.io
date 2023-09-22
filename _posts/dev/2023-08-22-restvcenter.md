---
layout: post
title:  "REST APIs v7.0U3"
author: Tinu
categories: "VMware"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

# Table of Contents

- [Table of Contents](#table-of-contents)
- [APIs](#apis)
    - [CIS REST APIs](#cis-rest-apis)
    - [Appliance REST APIs](#appliance-rest-apis)
- [Examples](#examples)
    - [Get an API Token](#get-an-api-token)
    - [Get all ESXiHosts](#get-all-esxihosts)
- [See also](#see-also)

# APIs

## CIS REST APIs

The CIS API provides VMware common infrastructure services such as session management, tags, and task management. 

## Appliance REST APIs

The appliance API provides services to manage vCenter Appliance configuration.

- The Health service provides operations to retrieve the appliance health information.
- The HealthCheckSettings service provides operations to enable/disable health check settings in vCenter Server.
- The LocalAccounts service provides operations to manage local user account.
- Monitoring service provides operations Get and list monitoring data for requested item.
- The Networking service provides operations Get Network configurations.
- Ntp service provides operations Gets NTP configuration status and tests connection to ntp servers.
- The Recovery service provides operations to invoke an appliance recovery (backup and restore).
- The Service service provides operations to manage a single/set of appliance services.
- Shutdown service provides operations Performs reboot/shutdown operations on appliance.
- The SupportBundle service provides operations to create support bundle task, cancel, list, delete and list components.
- Timesync service provides operations Performs time synchronization configuration.
- The Update service provides operations to get the status of the appliance update.

# Examples

## Get an API Token

To connect to a vCenter Server with REST API, the first thing is to get your API Token.

Creates a session with the API. This is the equivalent of login. This operation exchanges user credentials supplied in the security context for a session token that is to be used for authenticating subsequent calls. To authenticate subsequent calls clients are expected to include the session token. For REST API calls the HTTP vmware-api-session-id header field should be used for this.

````powershell
$vCenterServer  = 'Your-vCenterServer'
$ApiCredentials = Get-Credential -Message 'vCenter Credentials' -UserName "$($env:USERDOMAIN)\$($env:USERNAME)"

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
````

Output:

````
Your Token from the vCenter Server
````

## Get all ESXiHosts

For each connection, it's required to set the API Token in Header Parameters as vmware-api-session-id.

````powershell
$vCenterServer  = 'Your-vCenterServer'

#Create the header Authorization
$headers = @{
    'Content-Type'          = 'application/json'
    'vmware-api-session-id' = $Token
}

$Properties = @{
    Uri             = "https://$($vCenterServer)/api/vcenter/host/"
    Method          = 'Get'
    Headers         = $headers
    UseBasicParsing = $true
    ContentType     = 'application/json'
    ErrorAction     = 'Stop'
}
Invoke-RestMethod @Properties
````

Output:

````
host      name                 connection_state power_state
----      ----                 ---------------- -----------
host-1234 esxi1234.company.com CONNECTED        POWERED_ON 
host-1567 esxi1567.company.com CONNECTED        POWERED_ON
````

# See also

https://communities.vmware.com/t5/VMware-Aria-Automation/Getting-vCenter-alarms-and-it-properties/m-p/2954710

[API Reference](https://developer.vmware.com/apis/vsphere-automation/v7.0U3/) on VMware Developper Documentation.

https://docs.vmware.com/en/VMware-Pulse-IoT-Center/2.0.2/pulse-api/GUID-4C6DB085-B2FB-4C0B-9EB8-20D348055071.html
entity.entity.type

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]
