---
title: Domain Trust
date: '2016-02-02T14:18:24+01:00'
author: Tinu
excerpt: ''
categories:
- Active Directory
tags:
- Active Directory
wordpress_id: 1423
layout: post
permalink: /wiki/domain-trust/
render_with_liquid: false
---

## Trusted Domains auflisten

```
Import-Module ActiveDirectory
$TrustedDomains = Get-ADTrust -Filter * | % {
    $domain += $_.Target
    [PSCustomObject]@{
        Source=$_.Source
        Target=$_.DistinguishedName
        Name=$_.Name
        TrustType=$_.TrustType
        Direction=$_.Direction
    }
}
$TrustedDomains | sort Name | ft -AutoSize
```

## Trusted Domains und DCs auflisten

```
Import-Module ActiveDirectory
$domain = @()
Get-ADTrust -Filter * | select Source, Target, TrustType, Direction | % {
  $domain += $_.Target
  [PSCustomObject]@{
    Source=$_.Source
    Target=$_.Target
    TrustType=$_.TrustType
    Direction=$_.Direction
  }
}
$domain |% {
  Write-Output `n$_
  try{
    Get-ADDomain -Identity $_ | select -ExpandProperty ReplicaDirectoryServers -EA SilentlyContinue |% {
     $dc= $_
     }
   }
   catch [Exception]{
     $dc= $($_.Exception.Message)
   }
   Write-Output $dc
}
```

## Trust verifizieren

```
netdom trust TrustingDomain.com /D:TrustedDomain.com /verify

netdom query /d:devgroup.example.com DOMAIN /verify
```

## Port Requirements

TCP Port Requirements for the Active Directory Domain Service:

<figure class="wp-block-table">

| **TCP Port** | **AD and AD DS Usage** | **Type of traffic** |
|---|---|---|
| 389 | Directory, Replication, User and Computer Authentication, Group Policy, Trusts | LDAP |
| 636 | Directory, Replication, User and Computer Authentication, Group Policy, Trusts | LDAP SSL |
| 3268 | Directory, Replication, User and Computer Authentication, Group Policy, Trusts | LDAP GC |
| 3269 | Directory, Replication, User and Computer Authentication, Group Policy, Trusts | LDAP GC SSL |
| 88 | User and Computer Authentication, Forest Level Trusts | Kerberos |
| 53 | User and Computer Authentication, Name Resolution, Trusts | DNS |
| 445 | Replication, User and Computer Authentication, Group Policy, Trusts | SMB,CIFS,SMB2, DFSN, LSARPC, NbtSS, NetLogonR, SamR, SrvSvc |
| 25 | Replication | SMTP |
| 135 | Replication | RPC, EPM |
| 49152..65535 | Replication, User and Computer Authentication, Group Policy, Trusts | RPC, DCOM, EPM, DRSUAPI, NetLogonR, SamR, FRS |
| 5722 | File Replication | RPC, DFSR (SYSVOL) |
| 464 | Replication, User and Computer Authentication, Trusts | Kerberos change/set password |
| 9389 | AD DS Web Services | SOAP |
| 139 | User and Computer Authentication, Replication | DFSN, NetBIOS Session Service, NetLogon |

<figcaption>tcp ports</figcaption></figure>UDP Port Requirements for the Active Directory Domain Service:

<figure class="wp-block-table">

| **UDP Port** | **AD and AD DS Usage** | **Type of traffic** |
|---|---|---|
| 389 | Directory, Replication, User and Computer Authentication, Group Policy, Trusts | LDAP |
| 88 | User and Computer Authentication, Forest Level Trusts | Kerberos |
| 53 | User and Computer Authentication, Name Resolution, Trusts | DNS |
| 445 | Replication, User and Computer Authentication, Group Policy, Trusts | SMB,CIFS,SMB2, DFSN, LSARPC, NbtSS, NetLogonR, SamR, SrvSvc |
| 123 | Windows Time, Trusts | Windows Time |
| 464 | Replication, User and Computer Authentication, Trusts | Kerberos change/set password |
| UDP Dynamic | Group Policy | DCOM, RPC, EPM |
| 138 | DFS, Group Policy | DFSN, NetLogon, NetBIOS Datagram Service |
| 67 | DHCP | DHCP, MADCAP |
| 2535 | DHCP | DHCP, MADCAP |
| 137 | User and Computer Authentication, | NetLogon, NetBIOS Name Resolution |

<figcaption>udp ports</figcaption></figure>[Active Directory and Active Directory Domain Services Port Requirements](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/dd772723(v=ws.10)?redirectedfrom=MSDN%20target=)## Test Communication to Domain Controllers

```
#Download and install PsNetTools
$ZipFile = "https://github.com/tinuwalther/PsNetTools/releases/download/v0.7.5/PsNetTools.zip"
$OutFile = "$($env:USERPROFILE)\Downloads\PsNetTools-v0.7.5.zip"

Invoke-WebRequest -Uri $ZipFile -OutFile $OutFile
$ExpandFolder = "$($env:USERPROFILE)\Downloads\PsNetTools"
if(-not(Test-Path $ExpandFolder)){$null = mkdir $ExpandFolder}
Expand-Archive -Path $OutFile -OutputPath $ExpandFolder -Force

Copy-Item -Path $ExpandFolder -Destination "C:\Program Files\WindowsPowerShell\Modules" -Recurse -Force -PassThru
```

```
#Test ports with PsNetTools
$TargetDC = 'your target Domain Controller'
$TcpPort = @(389,636,3268,3269,88,53,445,25,135,5722,464,9389,139,49152..65535)
Test-PsNetTping -Destination $TargetDC -TcpPort $TcpPort -MaxTimeout 1000 | Format-Table

$UdpPort = @(389,88,53,445,123,464,138,67,2535,137,49152..65535)
Test-PsNetUping -Destination $TargetDC -TcpPort $UdpPort -MaxTimeout 1000 | Format-Table
```