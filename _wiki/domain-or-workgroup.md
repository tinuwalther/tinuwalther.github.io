---
title: Domain- or Workgroup Member
date: '2015-10-08T20:18:32+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Domain
- Workgroup
wordpress_id: 1397
layout: post
permalink: /wiki/domain-or-workgroup/
render_with_liquid: false
---

## Prüfen, ob der Computer Domain- oder Workgroup Member ist.

 Ab PowerShell Version 3.0 

```
function GetDomainOrWorkgroup{
    <# Check if the computer is domain- or workgroup member #>
    $function = $($MyInvocation.MyCommand.Name)
    try{
        if($psdebug){write-verbose "Running $($function) ..." -verbose}
        $objcomputer = (gwmi win32_computersystem)
        $DomainOrWorkgroupName = $null; $DomainOrWorkgroup = $null
        if (($objcomputer).partofdomain -eq $true) {
            $DomainOrWorkgroupName = $(($objcomputer).Domain)
            $DomainOrWorkgroup = "Domain"
        }
        else{
            $DomainOrWorkgroupName = $(($objcomputer).Workgroup)
            $DomainOrWorkgroup = "Workgroup"
        }
        [PSCustomObject]@{
            MemberOf = $DomainOrWorkgroup
            Name = $DomainOrWorkgroupName
        }
    }
    catch [Exception]{
          write-host "$($function): $($_.Exception.Message)" -ForegroundColor Red
          $error.clear()
    }
    return
}
GetDomainOrWorkgroup
```