---
layout: post
title:  "PowerShell Known Errors"
author: Tinu
categories: "PowerShell-Errors"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Unable to resolve package source 'https://www.powershellgallery.com/api/v2'](#unable-to-resolve-package-source-httpswwwpowershellgallerycomapiv2)
  - [Problem](#problem)
  - [Cause](#cause)
  - [Solution](#solution)
- [No match was found for the specified search criteria and module name](#no-match-was-found-for-the-specified-search-criteria-and-module-name)
  - [Problem](#problem-1)
  - [Cause](#cause-1)
  - [Solution](#solution-1)
  - [Set strong cryptography on .Net Framework (version 4 and above)](#set-strong-cryptography-on-net-framework-version-4-and-above)
  - [See also](#see-also)

# Unable to resolve package source 'https://www.powershellgallery.com/api/v2'

## Problem

````powershell
[1] I ♥ PS U:\ > Find-Module -Name PSWriteHTML
WARNING: Unable to resolve package source 'https://www.powershellgallery.com/api/v2'.
PackageManagement\Find-Package : No match was found for the specified search criteria and module name 'PSWriteHTML'. Try Get-PSRepository to see all available registered module repositories.
At C:\Program Files\WindowsPowerShell\Modules\PowerShellGet\2.2\PSModule.psm1:8871 char:9
+         PackageManagement\Find-Package @PSBoundParameters | Microsoft ...
+         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (Microsoft.Power...ets.FindPackage:FindPackage) [Find-Package], Exception
    + FullyQualifiedErrorId : NoMatchFoundForCriteria,Microsoft.PowerShell.PackageManagement.Cmdlets.FindPackage
````

## Cause

Thats a good question, I didn't find something about this.

## Solution

Use NuGet provider to install the required module to the target location.

````powershell
Register-PackageSource -Name PSNuGet -Location https://www.powershellgallery.com/api/v2 -ProviderName NuGet
````

# No match was found for the specified search criteria and module name

## Problem

````powershell
[1] I ♥ PS U:\ > Find-Module -Name PSWriteHTML
PackageManagement\Find-Package : No match was found for the specified search criteria and module name 'PSWriteHTML'. Try Get-PSRepository to see all available registered module repositories.
At C:\Program Files\WindowsPowerShell\Modules\PowerShellGet\2.2\PSModule.psm1:8871 char:9
+         PackageManagement\Find-Package @PSBoundParameters | Microsoft ...
+         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (Microsoft.Power...ets.FindPackage:FindPackage) [Find-Package], Exception
    + FullyQualifiedErrorId : NoMatchFoundForCriteria,Microsoft.PowerShell.PackageManagement.Cmdlets.FindPackage
````

## Cause

This is a TLS Issue. As of April 2020, TLS 1.2 is set to be the default for the PowerShell Gallery.

## Solution

To Fix TLS issue: run below command

````powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

[4] I ♥ PS U:\ > Find-Module -Name PSWriteHTML

Version              Name                                Repository           Description
-------              ----                                ----------           -----------
0.0.122              PSWriteHTML                         PSGallery            Module that allows creating HTML content/reports in a easy way.
````

## Set strong cryptography on .Net Framework (version 4 and above)

````powershell
Set-ItemProperty -Path 'HKLM:\SOFTWARE\Wow6432Node\Microsoft\.NetFramework\v4.0.30319' -Name 'SchUseStrongCrypto' -Value '1' -Type DWord

Set-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\.NetFramework\v4.0.30319' -Name 'SchUseStrongCrypto' -Value '1' -Type DWord
````

## See also

[PowerShell Gallery TLS Support](https://devblogs.microsoft.com/powershell/powershell-gallery-tls-support/)

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]