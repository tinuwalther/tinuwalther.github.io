---
layout: post
title:  "Unable to resolve package source https://www.powershellgallery.com/api/v2"
author: Tinu
categories: "PowerShell-Errors"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Unable to resolve package source https://www.powershellgallery.com/api/v2](#unable-to-resolve-package-source-httpswwwpowershellgallerycomapiv2)
  - [Problem](#problem)
  - [Cause](#cause)
  - [Solution](#solution)

# Unable to resolve package source https://www.powershellgallery.com/api/v2

Find-Module will result in a meaningless warning if you search for a known module in the Powershell gallery.

## Problem

````powershell
Find-Module -Name PSWriteHTML
WARNING: Unable to resolve package source 'https://www.powershellgallery.com/api/v2'.
````

and the following Error is from a [TLS](./FindModuleError.html) issue:

````powershell
PackageManagement\Find-Package : No match was found for the specified search criteria and module name 'PSWriteHTML'. 
Try Get-PSRepository to see all available registered module repositories.
At C:\Program Files\WindowsPowerShell\Modules\PowerShellGet\2.2\PSModule.psm1:8871 char:9
+ PackageManagement\Find-Package @PSBoundParameters | Microsoft ...
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

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]