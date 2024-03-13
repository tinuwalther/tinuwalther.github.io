---
layout: post
title:  "No match was found for the specified search criteria and module name"
author: Tinu
categories: "PowerShell-Errors"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [No match was found for the specified search criteria and module name](#no-match-was-found-for-the-specified-search-criteria-and-module-name)
  - [Problem](#problem)
  - [Cause](#cause)
  - [Solution](#solution)
  - [See also](#see-also)

## No match was found for the specified search criteria and module name

Find-Module could not connect to the specified uri in the registered repositories.

### Problem

````powershell
Find-Module -Name PSWriteHTML

PackageManagement\Find-Package : No match was found for the specified search criteria and module name 'PSWriteHTML'.
Try Get-PSRepository to see all available registered module repositories.
At C:\Program Files\WindowsPowerShell\Modules\PowerShellGet\2.2\PSModule.psm1:8871 char:9
+ PackageManagement\Find-Package @PSBoundParameters | Microsoft ...
+ CategoryInfo          : ObjectNotFound: (Microsoft.Power...ets.FindPackage:FindPackage) [Find-Package], Exception
+ FullyQualifiedErrorId : NoMatchFoundForCriteria,Microsoft.PowerShell.PackageManagement.Cmdlets.FindPackage
````

### Cause

TLS 1.2 is set to be the default for the PowerShell Gallery since April 2020, but this is not set on the computer.

### Solution

To Fix TLS issue on the current session, run below command:

````powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
````

````powershell
[4] I ♥ PS U:\ > Find-Module -Name PSWriteHTML

Version              Name                                Repository           Description
-------              ----                                ----------           -----------
0.0.122              PSWriteHTML                         PSGallery            Module that allows creating HTML content/reports ...
````

or set strong cryptography on .Net Framework (version 4 and above) for all sessions in the future:

````powershell
try{
    $value = Get-ItemPropertyValue -Path 'HKLM:\SOFTWARE\Wow6432Node\Microsoft\.NetFramework\v4.0.30319' -Name 'SchUseStrongCrypto'
}catch{
    $value = 0
}
if($value -ne 1){
    Set-ItemProperty -Path 'HKLM:\SOFTWARE\Wow6432Node\Microsoft\.NetFramework\v4.0.30319' -Name 'SchUseStrongCrypto' -Value '1' -Type DWord
}

try{
    $value = Get-ItemPropertyValue -Path 'HKLM:\SOFTWARE\Microsoft\.NetFramework\v4.0.30319' -Name 'SchUseStrongCrypto'
}catch{
    $value = 0
}
if($value -ne 1){
    Set-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\.NetFramework\v4.0.30319' -Name 'SchUseStrongCrypto' -Value '1' -Type DWord
}
Restart-Computer
````

### See also

[PowerShell Gallery TLS Support](https://devblogs.microsoft.com/powershell/powershell-gallery-tls-support/)
