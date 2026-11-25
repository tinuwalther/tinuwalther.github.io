---
title: DHCP Failover
date: '2015-02-27T14:40:20+01:00'
author: Tinu
excerpt: ''
categories:
- Windows Server
tags:
- DHCP Server
wordpress_id: 814
layout: post
permalink: /wiki/dhcp-failover/
render_with_liquid: false
---

## DHCP Failover Windows Server 2012

Zwei DHCP Server werden so konfiguriert, dass sie Leases aus demselben Adresspool vergeben. Dann replizieren die beiden Server gegenseitig die Daten, wodurch jeder Server in der Lage ist allein die Leasevergabe zu übernehmen wenn ein Server ausfällt. 

### Hot-Standby Mode

- Leases werden vom primären Server vergeben
- Der sekundäre übernimmt nur bei Ausfall des pimären Servers
- Primärer Server in Hauptsitz, sekundäre Server in jeder Aussenstelle
- die DHCP Server der Aussenstellen vergeben Adressen in der eigenen Aussenstelle
- der DHCP Server des Hauptsitzes vergibt Adressen im Hauptsitz und ist sekundärer Server für die Aussenstellen

[Technet](https://technet.microsoft.com/en-us/library/hh831385.aspx "Step-by-step: Configure DHCP for Failover")

### Load Balance Mode

- Beide Server vergeben gleichermassen Leases
- Verfügbarkeit und Lastausgleich ist damit gewährleistet
- zwei DHCP Server am selben geografischen Standort

## Implementieren von DHCP Failover

Zwei DHCP Server installieren, DHCP Scopes erstellen oder importieren, DHCP Failover auf erstem Scope konfigurieren, alle weiteren Scopes zum Failover hinzufügen und beide Server im Active Directory autorisieren.

```csharp
Add-WindowsFeature -IncludeManagementTools dhcp
```

### Post-Installation Tasks

```csharp
#Creating DHCP security groups
netsh dhcp add securitygroups
Restart-service dhcpserver
#Authorizing the DHCP server in Active Directory
Add-DhcpServerInDC <hostname of the DHCP server> <IP address of the DHCP server>
#Remove ServerManager Flag
Set-ItemProperty –Path HKLM:\SOFTWARE\Microsoft\ServerManager\Roles\12 `
–Name ConfigurationState –Value 2
```

### DHCP Failover Load Balance Mode erstellen

```csharp
function create-dhcp-failover{
    param (
        [Parameter(Mandatory=$true)][String] $dhcpserver1,
        [Parameter(Mandatory=$true)][String] $dhcpserver2,
        [Parameter(Mandatory=$true)][Array] $dhcpscope
    )
    $dhcpfailovername = "$($dhcpserver1)-$($dhcpserver2)"
    Add-DhcpServerv4Failover -ComputerName $($dhcpserver1) `
    -Name $($dhcpfailovername) -PartnerServer $($dhcpserver2) `
    -LoadBalancePercent 50 -ScopeId $dhcpscope -PassThru
}
```

### DHCP Failover Hot Standby Mode erstellen

```csharp
function create-dhcp-failover{
    param (
        [Parameter(Mandatory=$true)][String] $dhcpserver1,
        [Parameter(Mandatory=$true)][String] $dhcpserver2,
        [Parameter(Mandatory=$true)][Array] $dhcpscope
    )
    $dhcpfailovername = "$($dhcpserver1)-$($dhcpserver2)"
    Add-DhcpServerv4Failover -ComputerName $dhcpserver1 ` 
     -Name $dhcpfailovername -PartnerServer $dhcpserver2 `
     -ReservePercent 10 -ScopeId $dhcpscope -PassThru
}
```

### DHCP Scope zum Failover hinzufügen

Jeder Scope muss zum Failover hinzugefügt werden. Bereich wird auf dem Partnerserver hinzugefügt und deaktiviert. Failoverkonfiguration wird auf beiden Servern erstellt. Bereich wird auf dem Partnerserver aktiviert. Scopes müssen bereits bestehen bevor sie in den Failover aufgenommen werden können. 

```csharp
function add-dhcp-scope-failover{
    param (
        [Parameter(Mandatory=$true)][String] $dhcpserver1,
        [Parameter(Mandatory=$true)][String] $dhcpserver2,
        [Parameter(Mandatory=$true)][array] $dhcpscope
    )
    $dhcpfailovername = "$($dhcpserver1)-$($dhcpserver2)"
    Add-DhcpServerv4FailoverScope -ComputerName $($dhcpserver1) `
     -Name $($dhcpfailovername) -ScopeId $dhcpscope
}

```

### DHCP Failover löschen

```csharp
function add-dhcp-scope-failover{
    param (
        [Parameter(Mandatory=$true)][String] $dhcpserver1,
        [Parameter(Mandatory=$true)][String] $dhcpserver2
    )
    $dhcpfailovername = "$($dhcpserver1)-$($dhcpserver2)"
    Remove-DhcpServerv4Failover -ComputerName $dhcpserver1 -Name $dhcpfailovername
}
```