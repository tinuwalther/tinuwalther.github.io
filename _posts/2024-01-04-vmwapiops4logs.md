---
layout: post
title:  "API Aria Operations for Logs"
author: Tinu
categories: "VMware"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Operations for Logs API](#operations-for-logs-api)
    - [Request your sessionId](#request-your-sessionid)
    - [Retrieve version information](#retrieve-version-information)
    - [Get properties of the specified virtual machine by id](#get-properties-of-the-specified-virtual-machine-by-id)
- [See also](#see-also)

# Operations for Logs API

To list some properties of your VMware Aria Operations for Logs you need:

- Your Operations for Logs Login
- https://<ops4logs.company.com>/rest-api/v2#Getting-started-with-the-VMware-Aria-Operations-for-Logs-REST-API

## Request your sessionId

Get the sessionId for your account:

````powershell
function Get-Ops4LogsToken {
    [CmdletBinding()]
    Param (
        [Parameter(Mandatory=$true)]
        [String]$Server,

        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [PSCredential]$Credentials
    )

    try{
        $headers = @{
            "Content-Type"  = "application/json"
        }

        $body = [PSCustomObject] @{
                username = $Credentials.UserName
                password = $Credentials.GetNetworkCredential().Password
                provider = "ActiveDirectory"
        }

        $Properties = @{
            Uri             = "https://$($Server):9543/api/v2/sessions"
            Method          = 'POST'
            Headers         = $headers
            Body            = $body | ConvertTo-Json
            UseBasicParsing = $true
            ErrorAction     = 'Stop'
        }
        $response = Invoke-RestMethod @Properties      
        return "Bearer $($response.sessionId)"
    }catch{
        Write-Warning $('ScriptName:', $($_.InvocationInfo.ScriptName), 'LineNumber:', $($_.InvocationInfo.ScriptLineNumber), 'Message:', $($_.Exception.Message) -Join ' ')
        $Error.Clear()
    }
}
````

Set the SslProtocol:

````powershell
$SslProtocol      = 'Tls12'
$CurrentProtocols = ([System.Net.ServicePointManager]::SecurityProtocol).toString() -split ', '
if (!($SslProtocol -in $CurrentProtocols)){
    [System.Net.ServicePointManager]::SecurityProtocol += [System.Net.SecurityProtocolType]::$($SslProtocol)
}
````

Get the token (sessionId):

````powershell
$ops4logsServer    = '<ops4logs.company.com>'
$ApiCredentials    = Get-Credential -Message 'Ops4Logs Credentials' -UserName "$($env:USERDOMAIN)\$($env:USERNAME)"
$AuthToken         = Get-Ops4LogsToken -Credentials $ApiCredentials -Server $ops4logsServer
````

## Retrieve version information

Retrieve Log Insight version information, in the form Major.Minor.Patch-Build of all Ops4Logs Instances:

````powershell
$ApiSessionHeaders = @{
    "Accept"        = "application/json"
    "Content-Type"  = "application/json"
    'Authorization' = $AuthToken
}

$LogInstances = @(
    'Primary Node'
    'Secondary Node'
    'Third Node'
    'Virtual Node'
)

$ret = foreach($s in $LogInstances){
    $Properties = @{
        Uri             = "https://$($s):9543/api/v2/version"
        Method          = 'Get'
        Headers         = $ApiSessionHeaders
        UseBasicParsing = $true
        ContentType     = 'application/json'
        ErrorAction     = 'Stop'
    }
    $version = Invoke-RestMethod @Properties
    $version | Add-Member NoteProperty server $s
    $version
}
$ret | Format-Table server,releaseName,version
````

# See also

[API Reference](https://developer.vmware.com/apis/1458/) on VMware Developper Documentation,

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]
