---
layout: post
title:  "vSphere REST API"
author: Tinu
categories: "VMware"
tags:   PowerShell News
permalink: /posts/:title:output_ext
---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [vSphere REST API](#vsphere-rest-api)
  - [Authentication](#authentication)
    - [Get the base64-encoded Token](#get-the-base64-encoded-token)
    - [Create the Session Headers](#create-the-session-headers)
  - [Get all ESXiHosts](#get-all-esxihosts)
- [See also](#see-also)

## vSphere REST API

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

### Authentication

To connect to a vCenter Server with REST API, the first thing is to get your API Token.

Creates a session with the API. This is the equivalent of login. This operation exchanges user credentials supplied in the security context for a session token that is to be used for authenticating subsequent calls. To authenticate subsequent calls clients are expected to include the session token. For REST API calls the HTTP **vmware-api-session-id** header field should be used for this.

#### Get the base64-encoded Token

````powershell
function Get-vROAuthenticationToken {
    [CmdletBinding()]
    Param (
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [PSCredential]$Credentials
    )

    try{
        $pair      = "$($Credentials.UserName):$($Credentials.GetNetworkCredential().Password)"
        $bytes     = [System.Text.Encoding]::ASCII.GetBytes($pair)
        $base64    = [System.Convert]::ToBase64String($bytes)
        return "Basic $base64"
    }catch{
        Write-Warning $('ScriptName:', $($_.InvocationInfo.ScriptName), 'LineNumber:', $($_.InvocationInfo.ScriptLineNumber), 'Message:', $($_.Exception.Message) -Join ' ')
        $Error.Clear()
    }
}
````

#### Create the Session Headers

````powershell
function Invoke-vROAuthorization {
    [CmdletBinding()]
    Param (
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [String]$AuthenticationToken,

        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [String]$vCenterServer
    )

    try{
        $authorizationHeaders = @{
            'Content-Type'  = 'application/json'
            'Authorization' = $AuthenticationToken
        }

        $Properties = @{
            Uri             = "https://$($vCenterServer)/api/session"
            Method          = 'Post'
            Headers         = $authorizationHeaders
            UseBasicParsing = $true
            ContentType     = 'application/json'
            ErrorAction     = 'Stop'
        }

        $Token = Invoke-RestMethod @Properties

        $sessionHeaders = @{
            'Content-Type'          = 'application/json'
            'vmware-api-session-id' = $Token
        }
        return $sessionHeaders
    }catch{
        Write-Warning $('ScriptName:', $($_.InvocationInfo.ScriptName), 'LineNumber:', $($_.InvocationInfo.ScriptLineNumber), 'Message:', $($_.Exception.Message) -Join ' ')
        $Error.Clear()
    }
}
````

````powershell
#region Logon
$vCenterServer     = 'vCenterServer.company.local'
$ApiCredentials    = Get-Credential -Message 'vCenter Credentials' -UserName "$($env:USERDOMAIN)\$($env:USERNAME)"
$AuthToken         = Get-vROAuthenticationToken -Credentials $ApiCredentials
$ApiSessionHeaders = Invoke-vROAuthorization -vCenterServer $vCenterServer -AuthenticationToken $AuthToken
#endregion
````

### Get all ESXiHosts

For each connection, it's required to set the API Token in Header Parameters as vmware-api-session-id.

````powershell
$Properties = @{
    Uri             = "https://$($vCenterServer)/api/vcenter/host/"
    Method          = 'Get'
    Headers         = $ApiSessionHeaders
    UseBasicParsing = $true
    ContentType     = 'application/json'
    ErrorAction     = 'Stop'
}
Invoke-RestMethod @Properties
````

Output:

````text
host      name                 connection_state power_state
----      ----                 ---------------- -----------
host-1234 esxi1234.company.com CONNECTED        POWERED_ON 
host-1567 esxi1567.company.com CONNECTED        POWERED_ON
````

## See also

[API Reference](https://developer.vmware.com/apis/vsphere-automation/v7.0U3/) on VMware Developper Documentation.

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]
