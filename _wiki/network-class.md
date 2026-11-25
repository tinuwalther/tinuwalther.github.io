---
title: Network Class
date: '2017-09-30T17:49:04+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Class
- Netzwerk
wordpress_id: 2366
layout: post
permalink: /wiki/network-class/
render_with_liquid: false
---

Ich stehe oft vor der Herausforderung, dass ich nicht nur die IPAdresse, SubnetMask und DefaultGateway eines Server abfragen will, sondern auch noch das Hostsfile und die Routingtable und alles bitte schön als Object zurückgeben. Also mit PowerShell eine eigene Klasse schreiben mit welcher eben diese Eigenschaften ausgelesen werden können - PSNetConfig entsteht.

## Eine Klasse erstellen

Wenn eine Klasse erstellt werden soll, sind die foldgenden Fragen zu beantworten: 1) Was will ich machen? 

- die IP-Konfiguration auslesen und
- das hostsfile auslesen und
- die Routingtable auslesen

2) Welche Eigenschaften benötige ich dafür? 

- IPAdresse
- SubnetMask
- DefaultGateway
- . . .
- Hostseinträge (127.0.0.1    localhost)
- Destination
- NextHop
- Metric
- . . .

3) Welche Methoden benötige ich dafür? 

- Eine Methode mit der Win32\_NetworkAdapterConfiguration-Class mit all den benötigten Eigenschaften
- Eine Methode mit der Win32\_IP4RouteTable-Class mit all den benötigten Eigenschaften
- Eine Methode mit der das Hostsfile ausgelesen und formatiert zurückgegeben werden kann

Danach können die Eigenschaften der Klasse bestimmt und im Konstuktor durch Methoden abgefüllt werden. 

## Die Klasse

Die Klasse mit ihren Eigenschaften und Methoden: 

```
Class PSNetConfig {

    #region Properties with default values
    [object] hidden $NetworkAdapterConfig   = $null
    [object] hidden $RoutingEntries         = $null
    [string]$HostName                       = $null
    [int]   $Index                          = $null
    [int]   $InterfaceIndex                 = $null
    [string]$NetworkInterfaceDescription    = $null
    [object]$IPV4Address                    = $null
    [object]$IPV6Address                    = $null
    [object]$IPV4SubnetMask                 = $null
    [object]$IPV6SubnetMask                 = $null
    [object]$IPV4DefaultGateway             = $null
    [object]$IPV6DefaultGateway             = $null
    [string]$MACAddress                     = $null
    [string]$DNSHostName                    = $null
    [string]$DNSDomain                      = $null
    [object]$DNSServerSearchOrder           = $null
    [object]$DNSDomainSuffixSearchOrder     = $null
    [object]$HOSTSrecords                   = $null
    [object]$ROUTEInterfaceIndex            = $null
    [object]$ROUTEDestination               = $null
    [object]$ROUTEMask                      = $null
    [object]$ROUTEGateway                   = $null
    [object]$ROUTEMetric1                   = $null
    #endregion
    
    #region Constructor
    PSNetConfig([int] $InterfaceIndex){

        #Assigning property values
        $this.HostName                    = $env:COMPUTERNAME
        $this.NetworkAdapterConfig        = [PSNetConfig]::GetNetworkAdapterConfig($InterfaceIndex)
        $this.Index                       = $this.NetworkAdapterConfig.Index
        $this.InterfaceIndex              = $this.NetworkAdapterConfig.InterfaceIndex
        $this.NetworkInterfaceDescription = $this.NetworkAdapterConfig.NetworkInterfaceDescription
        $this.IPV4Address                 = $this.NetworkAdapterConfig.IPV4Address
        $this.IPV6Address                 = $this.NetworkAdapterConfig.IPV6Address
        $this.IPV4SubnetMask              = $this.NetworkAdapterConfig.IPV4SubnetMask
        $this.IPV6SubnetMask              = $this.NetworkAdapterConfig.IPV6SubnetMask
        $this.IPV4DefaultGateway          = $this.NetworkAdapterConfig.IPV4DefaultGateway
        $this.IPV6DefaultGateway          = $this.NetworkAdapterConfig.IPV6DefaultGateway
        $this.MACAddress                  = $this.NetworkAdapterConfig.MACAddress
        $this.DNSHostName                 = $this.NetworkAdapterConfig.DNSHostName
        $this.DNSDomain                   = $this.NetworkAdapterConfig.DNSDomain
        $this.DNSServerSearchOrder        = $this.NetworkAdapterConfig.DNSServerSearchOrder
        $this.DNSDomainSuffixSearchOrder  = $this.NetworkAdapterConfig.DNSDomainSuffixSearchOrder
        
        $this.HOSTSrecords                = [PSNetConfig]::GetHostsEntries()
        
        $this.RoutingEntries              = [PSNetConfig]::GetRoutingEntries($InterfaceIndex)
        $this.ROUTEInterfaceIndex         = $this.RoutingEntries.InterfaceIndex
        $this.ROUTEDestination            = $this.RoutingEntries.Destination
        $this.ROUTEMask                   = $this.RoutingEntries.Mask
        $this.ROUTEGateway                = $this.RoutingEntries.NextHop
        $this.ROUTEMetric1                = $this.RoutingEntries.Metric1
    }
    #endregion

    #region methods
    [object]static GetNetworkAdapterConfig($InterfaceIndex){
        $ret = @{}
        $objWin32 = Get-WmiObject Win32_NetworkAdapterConfiguration | Where-Object {
            ($_.InterfaceIndex -eq $InterfaceIndex)
        }
        $ret.Index                       = $objWin32.Index
        $ret.InterfaceIndex              = $objWin32.InterfaceIndex
        $ret.NetworkInterfaceDescription = $objWin32.Description
        
        $pattern = '\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b'
        $ret.IPV4Address        = $objWin32.IPAddress -match $pattern
        $ret.IPV4DefaultGateway = $objWin32.DefaultIPGateway -match $pattern

        $pattern = '(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))'
        $ret.IPV6Address        = $objWin32.IPAddress -match $pattern
        $ret.IPV6DefaultGateway = $objWin32.DefaultIPGateway -match $pattern

        $pattern = '^(((255\.){3}(255|254|252|248|240|224|192|128|0+))|((255\.){2}(255|254|252|248|240|224|192|128|0+)\.0)|((255\.)(255|254|252|248|240|224|192|128|0+)(\.0+){2})|((255|254|252|248|240|224|192|128|0+)(\.0+){3}))$'
        $ret.IPV4SubnetMask = $objWin32.IPSubnet -match $pattern

        $pattern = '^\d+$'
        $ret.IPV6SubnetMask = $objWin32.IPSubnet -match $pattern

        $ret.DNSHostName                = $objWin32.DNSHostName
        $ret.DNSDomain                  = $objWin32.DNSDomain
        $ret.DNSServerSearchOrder       = $objWin32.DNSServerSearchOrder
        $ret.DNSDomainSuffixSearchOrder = $objWin32.DNSDomainSuffixSearchOrder
        $ret.MACAddress                 = $objWin32.MACAddress
        return $ret
    }

    [object]static GetHostsEntries(){
        $ret = @()
        $content = get-content "$env:windir\System32\drivers\etc\hosts"
        $content | ForEach-Object {
            $regexmatch = $_ -match "(?<IP>^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(?<HOSTNAME>\S+$)"
            if($regexmatch){
                $ret += "$($matches.hostname)=$($matches.ip)"
            }
        }
        return $ret
    }

    [object]static GetRoutingEntries($InterfaceIndex){
        $ret = @{}
        $objWin32 = Get-WmiObject Win32_IP4RouteTable | Where-Object {
            ($_.InterfaceIndex -eq $InterfaceIndex)
        }
        $ret.InterfaceIndex  = $objWin32.InterfaceIndex
        $ret.Destination     = $objWin32.Destination
        $ret.Mask            = $objWin32.Mask
        $ret.Metric1         = $objWin32.Metric1
        $ret.NextHop         = $objWin32.NextHop
        $ret.Description     = $objWin32.Description
        $ret.Caption         = $objWin32.Caption
        $ret.Information     = $objWin32.Information
        $ret.Name            = $objWin32.Name
        $ret.Type            = $objWin32.Type
        $ret.RELPATH         = $objWin32.__RELPATH
        return $ret
    }
    #endregion
}
```

## Instanz erstellen

Um eine Instanz (ein Objekt mit den Eigenschaften und Methoden der Klasse) zu erstellen gibt es zwei verschiedene Möglichkeiten: 

```
$ipconfig = New-Object PSNetConfig(<InterfaceIndex>)
$ipconfig | Get-Member
$ipconfig 
```

IP Konfiguration aufzeigen (ipconfig): 

```
Get-WmiObject Win32_NetworkAdapterConfiguration | Where-Object {
    $_.DefaultIPGateway -ne $null
} | ForEach-Object {
    [PSNetConfig]::New($_.InterfaceIndex)
}
```

IP Konfiguration für alle Netzwerkkarten aufzeigen (ipconfig -all): 

```
Get-WmiObject Win32_NetworkAdapterConfiguration | ForEach-Object {
    [PSNetConfig]::New($_.InterfaceIndex)
}
```

## Members der Klasse

```
Name                        MemberType Definition                                   
----                        ---------- ----------                                   
Equals                      Method     bool Equals(System.Object obj)               
GetHashCode                 Method     int GetHashCode()                            
GetType                     Method     type GetType()                               
ToString                    Method     string ToString()                            
DNSDomain                   Property   string DNSDomain {get;set;}                  
DNSDomainSuffixSearchOrder  Property   string DNSDomainSuffixSearchOrder {get;set;} 
DNSServerSearchOrder        Property   string DNSServerSearchOrder {get;set;}       
HostName                    Property   string HostName {get;set;}                   
IPV4Address                 Property   string IPV4Address {get;set;}                
IPV4DefaultGateway          Property   string IPV4DefaultGateway {get;set;}         
IPV4SubnetMask              Property   string IPV4SubnetMask {get;set;}             
IPV6Address                 Property   string IPV6Address {get;set;}                
IPV6DefaultGateway          Property   string IPV6DefaultGateway {get;set;}         
IPV6SubnetMask              Property   string IPV6SubnetMask {get;set;}             
MACAddress                  Property   string MACAddress {get;set;}                 
NetworkInterfaceDescription Property   string NetworkInterfaceDescription {get;set;}
NetworkInterfaceIndex       Property   int NetworkInterfaceIndex {get;set;}    
...
```