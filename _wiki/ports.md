---
title: Ports
date: '2015-02-25T08:50:43+01:00'
author: Tinu
excerpt: ''
categories:
- Active Directory
tags:
- Ports
wordpress_id: 797
layout: post
permalink: /wiki/ports/
render_with_liquid: false
---

# Active Directory Ports

### Dynamischer RPC Port Range ab Windows Server 2008

| Protokoll | Transport | Port |
|---|---|---|
| RPC Windows Server 2008 | tcp | 49152 bis 65535 |

### User Login und Authentication

| Protokoll | Transport | Port |
|---|---|---|
| DNS | tcp/udp | 53 |
| LDAP | tcp/udp | 389 |
| Kerberos Authentication | tcp/udp | 88 |
| Kerberos Password Transmission | tcp/udp | 464 |
| \*Microsoft RPC | tcp | 1025 |
| Microsoft DS | tcp/udp | 445 |
| LDAP Global Catalog | tcp | 3268 |
| Endpoint Mapper | tcp | 135 |
| RPC Windwos Server 2008 | tcp | 49152 |

### Computer Join, Login, Authentication und Betrieb

| Protokoll | Transport | Port |
|---|---|---|
| DNS | tcp/udp | 53 |
| LDAP | tcp/udp | 389 |
| Kerberos Authentication | tcp/udp | 88 |
| Join Windwos Server 2003 | tcp | 1026 |
| \*Microsoft RPC | tcp | 1025 |
| RPC Windwos Server 2008 | tcp | 49152 |
| Join Windwos Server 2008 | tcp | 49153 |
| Microsoft DS | tcp/udp | 445 |
| NTP | udp | 123 |

### Explizite Trusterstellung zwischen Domains

| Protokoll | Transport | Port |
|---|---|---|
| DNS | tcp/udp | 53 |
| LDAP | tcp/udp | 389 |
| Kerberos Authentication | tcp/udp | 88 |
| \*Microsoft RPC | tcp | 1025 |
| Microsoft DS | tcp/udp | 445 |
| RPC Windwos Server 2008 | tcp | 49152 |

### Überprüfen und Authentisieren eines Trusts

| Protokoll | Transport | Port |
|---|---|---|
| DNS | tcp/udp | 53 |
| LDAP | tcp/udp | 389 |
| Kerberos Authentication | tcp/udp | 88 |
| \*Microsoft RPC | tcp | 1025 |
| RPC Windwos Server 2008 | tcp | 49152 |
| Microsoft DS | tcp/udp | 445 |
| Endpoint Mapper | tcp | 135 |
| Net Logon Service | tcp | \* random (EMAP) |

### Group Policy anwenden

| Protokoll | Transport | Port |
|---|---|---|
| Link speed determination | ICMP | ping |
| Link speed determination Windows Server 2008 | tcp | 135 |
| File access using SMB | tcp/udp | 445 |

### Active Directory Replikation

| Protokoll | Transport | Port |
|---|---|---|
| DNS | tcp/udp | 53 |
| LDAP | tcp/udp | 389 |
| File access using SMB | tcp/udp | 445 |
| Kerberos Authentication | tcp/udp | 88 |
| Directory Service RPC traffic | tcp | 49150 |
| FRS dynamic RPC port | tcp | 49151 |
| DFSR port | tcp | 49159 |