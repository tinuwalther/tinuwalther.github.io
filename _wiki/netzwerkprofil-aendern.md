---
title: Netzwerkprofil ändern
date: '2017-12-16T10:59:34+01:00'
author: Tinu
excerpt: Windows kennt drei verschiedene Netzwerkprofile. Es kommt vor, dass der Computer
  ein falsches Netzwerkprofil einstellt und somit die falschen Firewallsettings ziehen.
categories:
- PowerShell
tags:
- Netzwerk
- Windows Server
image: /assets/wiki/powershell-1.png
wordpress_id: 2415
layout: post
permalink: /wiki/netzwerkprofil-aendern/
render_with_liquid: false
---

## Netzwerkprofil abfragen/setzen

Windows kennt drei verschiedene Netzwerkprofile. Es kommt vor, dass der Computer ein falsches Netzwerkprofil einstellt und somit die falschen Firewallsettings ziehen. Public, Private und DomainAuthenticated. DomainAuthenticated kann nicht mit PowerShell gesetzt werden, sie sollte aufgrund der Domänenzugehörigkeit (NIC erkennt Domain Controller mit DNS lookups) automatisch erkannt werden. 

| Profile | Description |
|---|---|
| Domain | Applied to a network adapter when it is connected to a network on which it can detect a domain controller of the domain to which the computer is joined. |
| Private | Applied to a network adapter when it is connected to a network that is identified by the user or administrator as a private network. A private network is one that is not connected directly to the Internet, but is behind some kind of security device, such as a network address translation (NAT) router or hardware firewall. For example, this could be a home network, or a business network that does not include a domain controller. The Private profile settings should be more restrictive than the Domain profile settings. |
| Public | Applied to a network adapter when it is connected to a public network such as those available in airports and coffee shops. When the profile is not set to Domain or Private, the default profile is Public. The Public profile settings should be the most restrictive because the computer is connected to a public network where the security cannot be controlled. For example, a program that accepts inbound connections from the Internet (like a file sharing program) may not work in the Public profile because the Windows Firewall default setting will block all inbound connections to programs that are not on the list of allowed programs. |

### PowerShell

```
$netprof = Get-NetConnectionProfile
$netprof | fl *
Set-NetConnectionProfile -InterfaceIndex $netprof.InterfaceIndex -NetworkCategory Private|Public
```

### Netsh

```
netsh advfirewall show currentprofile
netsh advfirewall set domainprofile state on

privateprofile
domainprofile
publicprofile
```

### Network Connection Properties

Tipp von [Evan A Barr](http://evansblog.thebarrs.info/2013/02/windows-server-force-your-network.html): We will be adding a DNS suffix so that NLA can properly locate the domain controller which is how it knows to mark the location as “Domain network”. Go to Network Connections (from the Network and Sharing Center, click on "Change adapter settings".) Go to the properties of one network connection marked as "Unidentified" but on the private LAN. Go to the properties for IPv4. Click the "Advanced..." button. Select the DNS tab. Enter your domain name into the text box for "DNS suffix for this connection:". Disable and then enable the connection to get NLA to re-identify the location. After enabling the connection, the Status should change to the domain name and Network Category to "Domain network". Depending on your setup, it is likely that you only need to "fix" one connection to get all the related connections to see the domain. 

### Registry

HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\NetworkList\\Profiles 0 = public 1 = private 2 = domain