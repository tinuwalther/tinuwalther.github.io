---
title: Powershell Ping
date: '2014-12-23T11:15:48+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Netzwerk
- Ping
wordpress_id: 512
layout: post
permalink: /wiki/powershell-ping/
render_with_liquid: false
---

# Test-Connection: Ping in PowerShell senden

Mit Test-Connection wird ein Ping abgesetzt; die Firewall muss auf den Zielcomputern nicht geöffnet werden. 

```csharp
$serverlist = @("Server1","Server2","Server3")
$serverlist | % {
    if (Test-Connection -ComputerName $($_) -Quiet){
        "Host available""
    }
    else{
        "Host not available"
    }
}
```