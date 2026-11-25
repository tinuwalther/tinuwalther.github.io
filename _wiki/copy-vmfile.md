---
title: Copy-VMFile
date: '2017-09-12T20:13:44+02:00'
author: Tinu
excerpt: Files vom physischen (HyperV) Host auf eine VM kopieren.
categories:
- PowerShell
- Virtualisierung
tags:
- Hyper-V
image: /assets/wiki/hyperv-icon.png
wordpress_id: 2343
layout: post
permalink: /wiki/copy-vmfile/
render_with_liquid: false
---

Files vom physischen (HyperV) Host auf VMs kopieren

**Voraussetzungen:** Im Hyper-V-Manager unter Integrationsdienste die Gastdienste aktivieren.

```
Enable-VMIntegrationService -VMName "*" -Name "Guest Service Interface"
```

This example copies the file "C:\\Daten\\Bginfo.exe" from the host operating system into the guest operating system of the virtual machine "W2K16RC-SRV01". It will create the directory "C:\\Work" inside the guest operating system if it does not exist already.

```
$vmname = 'W2K16RC-SRV01'
$source = 'C:\Daten\Bginfo.exe'
$target = 'C:\Work\Bginfo.exe'
Copy-VMFile $vmname -SourcePath $source -DestinationPath $target -CreateFullPath -FileSource Host
```

This example copies the content from "C:\\Daten\\Templates" from the host operating system into the guest operating system of the virtual machine "W2K16RC-SRV01". It will create the directory "C:\\Daten\\Templates" inside the guest operating system if it does not exist already.

```
$vmname  = 'W2K16RC-SRV01'
$sources = Get-ChildItem -Path 'C:\Daten\Templates' -Recurse

foreach($item in $sources){
    Copy-VMFile -FileSource Host -VMName $vmname -SourcePath "$($item.FullName)" -DestinationPath "$($item.FullName)" -CreateFullPath -Force
}
```