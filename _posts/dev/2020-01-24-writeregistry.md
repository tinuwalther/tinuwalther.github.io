---
layout: post
title:  "Write Value to the Registry"
author: Tinu
categories: "PowerShell-Registry"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Write Single-Value to the Registry](#write-single-value-to-the-registry)
- [See also](#see-also)

Copy items from a local to a remote computer using a psremote-session.

# Write Single-Value to the Registry

````powershell
function Set-RegistryValue {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$false)]
        [Object]$args
    )
    $ret = $null
    if(-not(Test-Path "$($args.Hive):\$($args.Path)")){
        New-Item -Path "$($args.Hive):\$($args.Path)" -Force
    }

    Try{
        $ret = Set-ItemProperty -Path "$($args.Hive):\$($args.Path)" -Name $($args.Property) -value $($args.Value) -PassThru
    }
    catch{
        $ret = $null
    }

    return $ret
}

$params = @{
    Hive     = 'HKLM'
    Path     = 'SOFTWARE\Company\Settings'
    Property = 'CompanyGroupId'
    Value    = '123456'
}

Set-RegistryValue -args $params
````

# See also

[Set-ItemPropertyValue](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-itemproperty?view=powershell-6) on Microsoft Docs.

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]