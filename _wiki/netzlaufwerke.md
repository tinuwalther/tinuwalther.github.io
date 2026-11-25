---
title: Netzlaufwerke
date: '2016-10-13T10:53:22+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Devices
- Netzwerk
wordpress_id: 1606
layout: post
permalink: /wiki/netzlaufwerke/
render_with_liquid: false
---

Ab PowerShell 3.0 könnte ein Netzlaufwerk-Mapping in etwa so gemacht werden:

```
function Map-Networkdrive
{
    param(
        [ValidateSet('P','Q','R','S','T','U','V','W','X','Y','Z')]
        [Parameter(Mandatory=$true)]
        [String] $Letter = 'Z',
        [Parameter(Mandatory=$true)]
        [String] $Descri = 'Netzlaufwerk',
        [Parameter(Mandatory=$true)]
        [String] $Share  = '\\server\share',
        [Parameter(Mandatory=$false)]
        [Switch] $credentials = $false
    )
    $function = $($MyInvocation.MyCommand.Name)
    Write-Verbose $function -Verbose
    if(credentials)
    {
        $Creds = Get-Credential
        New-PSDrive -Name $Letter -Description $Descri -PSProvider FileSystem -Root $Share -Credential $Creds
    }
    else
    {
        New-PSDrive -Name $Letter -Description $Descri -PSProvider FileSystem -Root $Share
    }
}
function Get-MappedDrives
{
    $function = $($MyInvocation.MyCommand.Name)
    Write-Verbose $function -Verbose
    Get-WmiObject Win32_NetworkConnection | Format-Table -AutoSize
}

if(Test-NetConnection -ComputerName 'server' -InformationLevel Quiet -CommonTCPPort SMB)
{
    if(Test-Path -Path 'Z:')
    {
        Get-MappedDrives -Letter 'Z:' -Descri 'NetApp Share' -Share '\\netapp\data'
    }
    else
    {
        Map-Networkdrive
    }
}
```

Test-NetConnection benötigt PowerShell v4 von Windows 8.1 bzw. Server 2012 R2.