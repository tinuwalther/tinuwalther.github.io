---
title: Certificate Store
date: '2018-09-13T09:45:20+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Certificate
image: /assets/wiki/powershell-1.png
wordpress_id: 2510
layout: post
permalink: /wiki/certificate-store/
render_with_liquid: false
---

## Certificates auflisten

```
$ret = @()
$Issuer = '*'
$certs = Get-ChildItem Cert:\LocalMachine -Recurse | Where-Object Issuer -match "CN=$Issuer"
foreach($item in $certs){
    $obj = [PSCustomObject]@{
        Issuer = $item.Issuer
        NotBefore = $item.NotBefore.Date
        NotAfter = $item.NotAfter.Date
        KeySize = $item.PublicKey.Key.KeySize
    }
    $ret += $obj
}
$ret
```