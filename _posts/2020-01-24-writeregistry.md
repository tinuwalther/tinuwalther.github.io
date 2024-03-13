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
  - [Volatile registry key](#volatile-registry-key)
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

## Volatile registry key

If you use the New-Item-Cmdlet, the subkey is created as stable key. Sometimes you need a subkey that will be deleted after a reboot, you can create a volatile subkey.

````powershell
$HKLM   =[Microsoft.Win32.RegistryKey]::OpenBaseKey('LocalMachine','default')
$SubKey = $HKLM.OpenSubKey('SOFTWARE\Company\Settings', $true)
$SubKey.CreateSubKey('Volatile', $true , [Microsoft.Win32.RegistryOptions]::Volatile)
$SubKey.CreateSubKey('Non-Volatile', $true , [Microsoft.Win32.RegistryOptions]::None)
````

# See also

[Set-ItemPropertyValue](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-itemproperty?view=powershell-6) on Microsoft Docs.

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]