---
layout: post
title:  "Network Tools"
author: Tinu
tags:   SystemEngineering
---

- [PsNetTools](#psnettools)
  - [Usage](#usage)
- [PsNetDig](#psnetdig)
  - [Get-Help PsNetDig](#get-help-psnetdig)
  - [Example PsNetDig](#example-psnetdig)
- [PsNetTping](#psnettping)
  - [Get-Help PsNetTping](#get-help-psnettping)
  - [Example PsNetTping](#example-psnettping)
- [PsNetUping](#psnetuping)
  - [Get-Help PsNetUping](#get-help-psnetuping)
  - [Example PsNetUping](#example-psnetuping)
- [PsNetWping](#psnetwping)
  - [Get-Help PsNetWping](#get-help-psnetwping)
  - [Example PsNetWping](#example-psnetwping)

# PsNetTools

PsNetTools is a cross platform PowerShell module to test some network features on Windows and Mac.  

## Usage

Import Module:  

````powershell
Import-Module .\PsNetTools.psd1 -Force
````

List all ExportedCommands:  

````powershell
Get-Module PsNetTools

ModuleType Version Name       ExportedCommands
---------- ------- ----       ----------------
Script     0.1.2   PsNetTools {PsNetDig, PsNetTping, PsNetUping, PsNetWping}
````

# PsNetDig

PsNetDig - domain information groper.  
Resolves a hostname to the IP addresses or an IP Address to the hostname.  

## Get-Help PsNetDig

PsNetDig -Destination

- Destination: Hostname or IP Address or Alias or WebUrl

## Example PsNetDig

````powershell
PsNetDig -Destination 'sbb.ch' | Format-List

TargetName  : sbb.ch
IpV4Address : 194.150.245.142
IpV6Address : 2a00:4bc0:ffff:ffff::c296:f58e
Duration    : 4ms
````

# PsNetTping

PsNetTping - tcp port scanner.  
It's like the cmdlet Test-NetConnection, but with the ability to specify a timeout in ms.  

## Get-Help PsNetTping

PsNetTping -Destination -TcpPort -Timeout

- Destination: Hostname or IP Address or Alias or WebUrl
- TcpPort:     Tcp Port to use
- Timeout:     Timeout in ms

## Example PsNetTping

````powershell
PsNetTping -Destination 'sbb.ch' -TcpPort 443 -Timeout 100

TargetName   : sbb.ch
TcpPort      : 443
TcpSucceeded : True
Duration     : 22ms
MaxTimeout   : 100ms
````

# PsNetUping

PsNetUping - udp port scanner.  
It's like the cmdlet Test-NetConnection, but with the ability to specify a timeout in ms and query for udp.  

## Get-Help PsNetUping

PsNetTping -Destination -UdpPort -Timeout

- Destination: Hostname or IP Address or Alias or WebUrl
- UdpPort:     Udp Port to use
- Timeout:     Timeout in ms

## Example PsNetUping

````powershell
PsNetUping -Destination 'sbb.ch' -UdpPort 53 -Timeout 100

TargetName   : sbb.ch
UdpPort      : 53
UdpSucceeded : False
Duration     : 103ms
MaxTimeout   : 100ms
````

# PsNetWping

PsNetWping - http web request scanner.  
It's like the cmdlet Invoke-WebRequest, but with the ability to specify 'noproxy' with PowerShell 5.1.  

## Get-Help PsNetWping

PsNetWping -Destination -Timeout [-NoProxy]

- Destination: WebUri
- Timeout:     Timeout in ms
- NoProxy:     Switch

## Example PsNetWping

````powershell
PsNetWping -Destination 'https://sbb.ch' -Timeout 1000 -NoProxy

TargetName  : https://sbb.ch
ResponseUri : https://www.sbb.ch/de/
StatusCode  : OK
Duration    : 231ms
MaxTimeout  : 1000ms
````
