---
title: Chocolatey
date: '2016-08-23T21:12:52+02:00'
author: Tinu
excerpt: ''
categories:
- DevOps
tags:
- Cloud
- Package Manager
wordpress_id: 1538
layout: post
permalink: /wiki/chocolatey/
render_with_liquid: false
---

## Chocolatey Installation

```
Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
choco search <String>
choco list -lo
```

## Posh GIT Installation

```
choco install poshgit -y
choco uninstall poshgit -y
choco upgrade poshgit
```