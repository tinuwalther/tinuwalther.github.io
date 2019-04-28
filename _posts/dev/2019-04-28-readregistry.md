---
layout: post
title:  "Read Value from Registry"
author: Tinu
categories: "PowerShell-Registry"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Read-Value from Registry](#read-value-from-registry)
- [See also](#see-also)

Copy items from a local to a remote computer using a psremote-session.

# Read-Value from Registry

````powershell
function Get-RegistryValue {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$false)]
        [Object]$args
    )
    $ret = $null
    if(Test-Path "$($args.Hive):\$($args.Path)"){
        Try{
            $ret = Get-ItemPropertyValue -Path "$($args.Hive):\$($args.Path)" -Name $args.Property
        }
        catch{
            $ret = $null
        }
    }
    return $ret
}

$params = @{
    Hive     = 'HKLM'
    Path     = 'SOFTWARE\Microsoft\Windows NT\CurrentVersion'
    Property = 'ReleaseId'
}

return (Get-RegistryValue -args $params)
````

# See also

[Get-ItemPropertyValue](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-itempropertyvalue?view=powershell-6) on Microsoft Docs.

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]