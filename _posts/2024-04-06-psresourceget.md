---
layout: post
title:  "PSResourceGet"
author: Tinu
categories: "PowerShell-Repositories"
tags:   PowerShell News
permalink: /posts/:title:output_ext
---

## Table of Contents

<!-- TOC -->

- [Table of Contents](#table-of-contents)
- [PowerShell Gallery](#powershell-gallery)
- [Install PSResourceGet](#install-psresourceget)
    - [The content of PSResourceGet](#the-content-of-psresourceget)
- [Register NuGet-Repositories for PSResourceGet](#register-nuget-repositories-for-psresourceget)
- [Registers a repository for PSResourceGet](#registers-a-repository-for-psresourceget)
- [Find Modules](#find-modules)
- [Install Modules](#install-modules)
- [Remove a Module](#remove-a-module)
- [Get installed Modules](#get-installed-modules)
- [Remove PSRepository](#remove-psrepository)
- [See also](#see-also)

<!-- /TOC -->

## PowerShell Gallery

[PowerShell Gallery API v2](https://www.powershellgallery.com/api/v2)

## Install PSResourceGet

Required PowerShellGet v2.

In PowerShell version 7.4 the PSResourceGet is installed with version 1.0.1, to install the newest version add the -Force parameter to the Install-Module-Command.

````powershell
Install-Module -Name Microsoft.PowerShell.PSResourceGet -Scope AllUsers -PassThru -Force -Verbose
````

After the installation of the module, you can list all installed PSResourceGet-version.

````powershell
Get-Module -ListAvailable -Name Microsoft.PowerShell.PSResourceGet | Select-Object Version,Name

Version Name                               Path
------- ----                               ----
1.0.4.1 Microsoft.PowerShell.PSResourceGet /usr/local/share/powershell/Modules/...
1.0.1   Microsoft.PowerShell.PSResourceGet /opt/microsoft/powershell/7/Modules/...
````

List all commands of the PSResourceGet.

````powershell
Get-Command -Module Microsoft.PowerShell.PSResourceGet | Sort-Object Name | Select-Object Version,Name

Version     Name
-------     ----
1.0.4.1     Find-PSResource
1.0.4.1     Get-InstalledPSResource
1.0.4.1     Get-PSResource
1.0.4.1     Get-PSResourceRepository
1.0.4.1     Get-PSScriptFileInfo
1.0.4.1     Import-PSGetRepository
1.0.4.1     Install-PSResource
1.0.4.1     New-PSScriptFileInfo
1.0.4.1     Publish-PSResource
1.0.4.1     Register-PSResourceRepository
1.0.4.1     Save-PSResource
1.0.4.1     Set-PSResourceRepository
1.0.4.1     Test-PSScriptFileInfo
1.0.4.1     Uninstall-PSResource
1.0.4.1     Unregister-PSResourceRepository
1.0.4.1     Update-PSModuleManifest
1.0.4.1     Update-PSResource
1.0.4.1     Update-PSScriptFileInfo
````

### The content of PSResourceGet

List the content of the PSResourceGet-Module.

````powershell
$Path = '/usr/local/share/powershell/Modules/Microsoft.PowerShell.PSResourceGet/1.0.4.1'
Get-ChildItem -Path $Path | Sort-Object Name | Select-Object LastWriteTime,Size,Name

LastWriteTime           Size  Name
-------------           ----  ----
04/06/2024 10:03:10     4096  dependencies
04/05/2024 21:21:46     1095  LICENSE
04/05/2024 21:21:48   343584  Microsoft.PowerShell.PSResourceGet.dll
04/05/2024 21:21:46    26144  Microsoft.PowerShell.PSResourceGet.psd1
04/05/2024 21:21:46    17926  Microsoft.PowerShell.PSResourceGet.psm1
04/05/2024 21:21:46   158819  Notice.txt
04/05/2024 21:21:46    23512  PSGet.Format.ps1xml
04/06/2024 10:03:10    30507  PSGetModuleInfo.xml
````

List the content of the dependencies-folder to understand what is included. As we can see, NuGet is included.

````powershell
$Path = '/usr/local/share/powershell/Modules/Microsoft.PowerShell.PSResourceGet/1.0.4.1/dependencies/'
Get-ChildItem -Path $Path | Sort-Object Name | Select-Object LastWriteTime,Size,Name

LastWriteTime           Size  Name
-------------           ----  ----
04/05/2024 21:21:46   26656  Microsoft.Bcl.AsyncInterfaces.dll
04/05/2024 21:21:46  722160  Newtonsoft.Json.dll
04/05/2024 21:21:46  613824  NuGet.Commands.dll
04/05/2024 21:21:46  122800  NuGet.Common.dll
04/05/2024 21:21:46  170424  NuGet.Configuration.dll
04/05/2024 21:21:46   67616  NuGet.Credentials.dll
04/05/2024 21:21:46   93728  NuGet.DependencyResolver.Core.dll
04/05/2024 21:21:46  131104  NuGet.Frameworks.dll
04/05/2024 21:21:46   56760  NuGet.LibraryModel.dll
04/05/2024 21:21:46  689088  NuGet.Packaging.dll
04/05/2024 21:21:46  219056  NuGet.ProjectModel.dll
04/05/2024 21:21:48  786368  NuGet.Protocol.dll
04/05/2024 21:21:46   65984  NuGet.Versioning.dll
04/05/2024 21:21:46   20856  System.Buffers.dll
04/05/2024 21:21:46  142240  System.Memory.dll
04/05/2024 21:21:46  115856  System.Numerics.Vectors.dll
04/05/2024 21:21:46   18024  System.Runtime.CompilerServices.Unsafe.dll
04/05/2024 21:21:46   79024  System.Text.Encodings.Web.dll
04/05/2024 21:21:48  642832  System.Text.Json.dll
04/05/2024 21:21:46   25984  System.Threading.Tasks.Extensions.dll
04/05/2024 21:21:46   25232  System.ValueTuple.dll
````

## Register NuGet-Repositories for PSResourceGet

Finds the NuGet-Repositories registered with PowerShellGet and registers them for PSResourceGet.

The PSGallery repository is registered by default. This cmdlet doesn't import the PSGallery repository from PowerShellGet v2. If you need to reregister the PSGallery repository, use the Register-PSResourceRepository cmdlet with the PSGallery parameter.

````powershell
Import-PSGetRepository -Verbose
````

## Registers a repository for PSResourceGet

Registers the default PSGallery repository. The PSGallery repository is registered by default but can be removed.

````powershell
Register-PSResourceRepository -PSGallery -Trusted -PassThru -Verbose

Name      Uri                                      Trusted Priority
----      ---                                      ------- --------
PSGallery https://www.powershellgallery.com/api/v2 True    50
````

Register the PSGallery v2.

````powershell
$parameters = @{
  Name     = 'PSGalleryV2'
  Uri      = 'https://www.powershellgallery.com/api/v2'
  Trusted  = $true
  PassThru = $true
  Priority = 20 # default is 50
}
Register-PSResourceRepository @parameters -Verbose

Get-PSResourceRepository

Name        Uri                                      Trusted Priority
----        ---                                      ------- --------
PSGalleryV2 https://www.powershellgallery.com/api/v2 True    20
PSGallery   https://www.powershellgallery.com/api/v2 False   50
````

Registers a repository with credential information to be retrieved from a registered SecretManagement vault. Requires Microsoft.PowerShell.SecretManagement module installed.

````powershell
$parameters = @{
  Name     = 'PSGv3'
  Uri      = 'https://www.powershellgallery.com/api/v3'
  Trusted  = $true
  PassThru = $true
  Priority = 10 # default is 50
  CredentialInfo = [Microsoft.PowerShell.PSResourceGet.UtilClasses.PSCredentialInfo]::new(
    'LocalSecretStore', 'PSGv3Secret')
}
Register-PSResourceRepository @parameters -Verbose
````

## Find Modules

To find all Modules where the Name starts with PsNet.

````powershell
Find-PSResource -Name PsNet* -Repository PSGalleryV2 | Select-Object Version,Name,Repository,Description

Version Name              Repository  Description
------- ----              ----------  -----------
0.7.8   PsNetTools        PSGalleryV2 Cross platform PowerShell module to test network functions.
0.0.1   psNetSpell        PSGalleryV2 This module allows you to spell-check a document
0.5     PsNetSapiens      PSGalleryV2 This module is an API wrapper for NetSapiens.
1.2.6   PSNetboxFunctions PSGalleryV2 Connect to Netbox API with Token and manage its resources.
1.0.1   PSNetAddressing   PSGalleryV2 A PowerShell module for representing network IP addresses.
````

## Install Modules

Set the PSGallery as trusted if it's not.

````powershell
Set-PSResourceRepository -Name "PSGallery" -Priority 25 -Trusted -PassThru

Name      Uri                                      Trusted Priority
----      ---                                      ------- --------
PSGallery https://www.powershellgallery.com/api/v2 True    25
````

Install a Module.

````powershell
Install-PSResource -Name PsNetTools -Scope AllUsers -PassThru -Verbose

Name       Version Prerelease Repository Description
----       ------- ---------- ---------- -----------
PsNetTools 0.7.8              PSGallery  Cross platform PowerShell module to test network functions.
````

Re-install a Module.

````powershell
Install-PSResource -Name PsNetTools -Scope AllUsers -PassThru -Reinstall -Verbose

Name       Version Prerelease Repository Description
----       ------- ---------- ---------- -----------
PsNetTools 0.7.8              PSGallery  Cross platform PowerShell module to test network functions.
````

## Remove a Module

To remove a Module.

````powershell
Uninstall-PSResource -Name PsNetTools -Scope AllUsers -Verbose
````

## Get installed Modules

List installed modules of all PSModulePath.

````powershell
$Path = $env:PSModulePath -split [System.IO.Path]::PathSeparator
$Path | ForEach-Object { Get-InstalledPSResource -Path $PSItem | Select-Object Version,Name,InstalledLocation }

Version Name                               InstalledLocation
------- ----                               -----------------
2.3.4   PSReadLine                         /usr/local/share/powershell/Modules/PSReadLine/2.3.4
0.7.8   PsNetTools                         /usr/local/share/powershell/Modules/PsNetTools/0.7.8
0.0.8   linuxinfo                          /usr/local/share/powershell/Modules/linuxinfo/0.0.8
1.9.0   PSWorkItem                         /usr/local/share/powershell/Modules/PSWorkItem/1.9.0
0.13.0  mySQLite                           /usr/local/share/powershell/Modules/mySQLite/0.13.0
1.0.4.1 Microsoft.PowerShell.PSResourceGet /usr/local/share/powershell/Modules/Microsoft.PowerShell.PSResourceGet/1.0.4.1
````

## Remove PSRepository

To remove a reposotory.

````powershell
Unregister-PSResourceRepository -Name PSGalleryV2 -Verbose
````

[ [Top](#table-of-contents) ]

## See also

[Microsoft.PowerShell.PSResourceGet](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.psresourceget/?view=powershellget-3.x) on Microsoft Learn.
