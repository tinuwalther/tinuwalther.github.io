---
layout: post
title:  "TLS and Cipher Suite"
author: Tinu
categories: "System-Engineering"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

## Table of Contents

- [Table of Contents](#table-of-contents)
  - [Get all cipher suites](#get-all-cipher-suites)
  - [Get all TLS versions](#get-all-tls-versions)
- [See also](#see-also)

### Get all cipher suites

The Get-TlsCipherSuite cmdlet gets an ordered collection of cipher suites for a computer that Transport Layer Security (TLS) can use.

````powershell
Get-TlsCipherSuite | Format-Table Name, Cipher*, Exchange
````

Output:

````powershell
Name                                    CipherBlockLength CipherLength CipherSuite Cipher Exchange
----                                    ----------------- ------------ ----------- ------ --------
TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA                     16          128       49171 AES    ECDH
TLS_RSA_WITH_AES_256_GCM_SHA384                        16          256         157 AES    RSA
TLS_PSK_WITH_AES_128_GCM_SHA256                        16          128         168 AES    PSK
...
````

### Get all TLS versions

The TLS versions are SubKeys of HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols.

````powershell
function Get-RegistryProperties{
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [String] $Hive
    )

    if(Test-path -Path $Hive){
        $root = Get-Item $Hive
        $ret = foreach($SubKey in $root.GetSubKeyNames()){
            $items = Get-Item "$Hive\$SubKey"
            if($items.SubKeycount -eq 0){
                foreach($Property in $items.Property){
                    [PSCustomObject]@{
                        Hive     = $Hive
                        Name     = $items.PSChildName
                        Property = $Property
                        Value    = Get-ItemPropertyValue -Path ("$Hive\$SubKey") -Name ($Property)
                    }
                }
            }
            else{
                ## Call the function recursive
                Get-RegistryProperties -Hive "$Hive\$SubKey"
            }
        }
    }
    return $ret
}

$RegKey = 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols'
Get-RegistryProperties -Hive $RegKey | Sort-Object Hive, Name | Format-Table
````

Output:

Value 1 = True, 0 = False

````powershell
Hive                                                                                Name   Property          Value
----                                                                                ----   --------          -----
HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2 Client DisabledByDefault     0
HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2 Client Enabled               1
...
````

## See also

[Get all cipher suites](https://learn.microsoft.com/en-us/powershell/module/tls/get-tlsciphersuite?view=windowsserver2022-ps), [Protocols in TLS/SSL (Schannel SSP)](https://learn.microsoft.com/en-us/windows/win32/secauthn/protocols-in-tls-ssl--schannel-ssp-), [Transport Layer Security (TLS) registry settings](https://learn.microsoft.com/en-us/windows-server/security/tls/tls-registry-settings?tabs=diffie-hellman) on Microsoft.

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]
