---
title: Windows Firewall
date: '2015-03-12T08:10:33+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Firewall
image: /assets/wiki/firewall-e1620744165429.png
wordpress_id: 891
layout: post
permalink: /wiki/windows-firewall/
render_with_liquid: false
---

## Windows Server 2008 and above

The Windows Firewall service (**MpsSvc**) and its supporting driver must be running to provide the core firewall functionality and to manage the firewall and connection security rules that define how the firewall operates. When appropriate auditing events are enabled, Windows reports successes and failures in starting the required software components, or when the components stop operating due to a failure. **Note:** Because the Windows Firewall services applies Windows service hardening rules to standard Windows Networking services, **Microsoft does not support stopping the Windows Firewall service**. If you do not want to use Windows Firewall, turn the firewall features off without stopping the service. 

### Get Advanced Windows Firewall Profiles

```
netsh advfirewall show allprofiles
Get-NetFirewallProfile | select Name, Enabled, LogFileName | ft -auto
```

### Enable Windows Firewall Profiles

```
netsh advfirewall set AllProfiles state on
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
```

### Allow all traffic

```
netsh advfirewall set AllProfiles firewallpolicy "allowinbound,allowoutbound"
Set-NetFirewallProfile -DefaultInboundAction Allow -DefaultOutboundAction Allow
```

## Effects of Stopping or Disabling the Firewall Service

Effects of Stopping or Disabling the Windows Firewall Service in Windows Server 2008 and Above: In Windows Server 2008 and later versions, however, the Windows Firewall service has been completely rewritten and is an integral part of the operating system's network stack. **Microsoft no longer recommends stopping or disabling the service** **under any circumstances**; in fact, this is now an unsupported configuration. Stopping or disabling the service will cause a number of network-related problems, including the following: 

- The server will not respond to pings
- You will be unable to connect to the server via Remote Desktop. If the service is stopped within in RDP session, the session will disconnect and will fail to reconnect
- You will be unable to connect to shares on the server, and "Network path not found" will be the resulting error
- If the server is a DNS server, it will not respond to queries
- If the server is a DC, Active Directory replication with other DCs will fail
- If the server is a DHCP server, DHCP clients on the network will not be able to lease or renew IP addresses

**In short, it will appear to other machines as though the server has been disconnected from the network**, although network operations initiated from that server will succeed for the most part: it will be able to ping other machines, connect to remote shares, and browse the internet, for example. In some situations, it is necessary to turn off the Windows Firewall (for example, if a third-party firewall has been installed and is causing conflicts), **but this should not be done by stopping or disabling the service**. To turn off the firewall using **Netsh** or Windows **PowerShell**: 

```
netsh advfirewall set AllProfiles state off
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False
```

### References

<http://www.dell.com/support/article/ch/de/chbsdt1/SLN156677/DE><https://technet.microsoft.com/en-us/library/cc733276(v=ws.10).aspx><https://technet.microsoft.com/en-us/library/cc766337(v=ws.10).aspx>