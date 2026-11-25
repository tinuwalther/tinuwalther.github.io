---
title: DNS Serveradresse ändern
date: '2016-06-27T22:00:10+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Netzwerk
- PSObject
wordpress_id: 1499
layout: post
permalink: /wiki/dns-serveradresse-aendern/
render_with_liquid: false
---

DNS Serveradresse auf Interface mit bestimmter IP Adresse ändern.

```
function Get-Interface{
    <#
         Get-Interface with the given ipaddress in NameServer
    #>
    param(
        [Parameter(Mandatory=$true)][String]$ipaddress = ''
    )
    $function = $($MyInvocation.MyCommand.Name)
    try
    {
        $key = 'HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces'
        Get-ChildItem -Path $key | % {
            $start      = $_.Name.LastIndexOf('{')
            $interface  = $_.Name.Substring($start)
            $nameserver = (Get-ItemProperty -Path "$key\$interface" -Name 'NameServer').NameServer
            if($nameserver -like $ipaddress){
                return "$key\$interface"
            }
        }
    }
    catch [Exception]
    {
        write-host "$($function): $($_.Exception.Message)" -ForegroundColor Red
        $error.clear()
    }
}

function Get-Interface{
    <# Get-Interface with the given ipaddress in NameServer #>
    param(
        [Parameter(Mandatory=$true)][String]$ipaddress = ''
    )
    $ret = @()
    $function = $($MyInvocation.MyCommand.Name)
    $key = 'HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces'
    Get-ChildItem -Path $key | % {
        $obj = New-Object PSObject
        $nameserver   = $null
        $nicipaddress = $null
        $start        = $_.Name.LastIndexOf('{')
        $interface    = $_.Name.Substring($start)
        $nicipaddress = (Get-ItemProperty -Path "$key\$interface" -Name 'IPAddress').IPAddress
        try
        {
            $nameserver   = (Get-ItemProperty -Path "$key\$interface" -Name 'NameServer').NameServer
        }
        catch
        {
            $nameserver   = $null
        }
        if($nameserver -match $ipaddress){
            Add-Member -InputObject $obj -MemberType NoteProperty -Name Interface -Value "$key\$interface"
            Add-Member -InputObject $obj -MemberType NoteProperty -Name IPAddress -Value $nicipaddress
            Add-Member -InputObject $obj -MemberType NoteProperty -Name NameServer -Value $nameserver
        }
        $ret += $obj
    }
    return $ret
}
$ErrorActionPreference = 'SilentlyContinue'
Get-Interface -ipaddress '193.223.16.15'

function Set-NameServer{
    <#
         Set-NameServer
    #>
    param(
        [Parameter(Mandatory=$true)][String]$interface = '',
        [Parameter(Mandatory=$true)][String]$ipaddress = ''
    )
    $function = $($MyInvocation.MyCommand.Name)
    $ret = $null
    try
    {
        $ret = (Set-ItemProperty -Path $interface -Name 'NameServer' -Value $ipaddress -PassThru).NameServer
    }
    catch [Exception]
    {
        write-host "$($function): $($_.Exception.Message)" -ForegroundColor Red
        $error.clear()
    }
    return $ret
}

$interface = Get-Interface -ipaddress '127.0.0.1'
if(!([string]::IsNullOrEmpty($interface)))
{
    Set-NameServer -interface $interface -ipaddress '192.168.0.3'
}
```