---
title: Could not load file or assembly Newtonsoft.Json
date: '2024-05-02T14:21:42+02:00'
author: Tinu
excerpt: PowerCLI Get-Tag fails with ‘Could not load file or assembly ‘Newtonsoft.Json,
  Version=10.0.0.0’
categories:
- PowerShell
tags:
- VMware
image: /assets/wiki/powershell-1.png
wordpress_id: 4168
layout: post
permalink: /wiki/could-not-load-file-or-assembly-newtonsoft-json/
render_with_liquid: false
---

PowerCLI Get-Tag fails with ‘Could not load file or assembly ‘Newtonsoft.Json, Version=10.0.0.0’

Wird nach dem connecten auf ein vCenter die Tags ausgelesen, schlägt dies mit **Could not load file or assembly ‘Newtonsoft.Json’** fehl.

```
Connect-VIServer ...

Get-Tag

11/10/2018 21:06:20 Get-Tag Could not load file or assembly 'Newtonsoft.Json, Version=10.0.0.0,

Culture=neutral, PublicKeyToken=30ad4fe6b2a6aeed' or one of its dependencies.
The system cannot find the file specified.

```

SBC PureConsult hat dies bereits im Oktober 2018 analysiert und einen [Workaround](https://www.sbcpureconsult.co.uk/2018/10/11/powercli-get-tag-fails-with-could-not-load-file-or-assembly-newtonsoft-json-version10-0-0-0/) aufgelistet.

## Workaround

Retrieve the newer version of the file (supplied with the PowerCLI modules), located for instance in:

C:\\Users\\username\\Documents\\WindowsPowerShell\\Modules\\VMware.VimAutomation.Common\\net45

and place a copy in somewhere PowerShell is likely to find it, e.g.:

C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\Newtonsoft.Json.dll

This simple work-around proved successful for me, but you should check of course to verify all other functionality which might depend on this file before making a similar change in a production environment.

