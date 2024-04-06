---
layout: post
title:  "From PowerShellGet to PSResourceGet"
author: Tinu
categories: "PowerShell-Module"
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
- [Get installed Modules](#get-installed-modules)
- [See also](#see-also)

<!-- /TOC -->

## PowerShell Gallery

[PowerShell Gallery API v2](https://www.powershellgallery.com/api/v2)

## Install PSResourceGet

Required PowerShellGet v2.

In PowerShell version 7.4 the PSResourceGet is installed with version 1.0.1, to install the newest version add the -Force parameter to the Install-Module-Command.

````powershell
Install-Module -Name Microsoft.PowerShell.PSResourceGet -Scope AllUsers -Verbose -Force
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
Get-Command -Module Microsoft.PowerShell.PSResourceGet | Sort-Object Name

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Cmdlet          Find-PSResource                                    1.0.4.1    Microsoft.PowerShell.PSResourceGet
Cmdlet          Get-InstalledPSResource                            1.0.4.1    Microsoft.PowerShell.PSResourceGet
Alias           Get-PSResource                                     1.0.4.1    Microsoft.PowerShell.PSResourceGet
Cmdlet          Get-PSResourceRepository                           1.0.4.1    Microsoft.PowerShell.PSResourceGet
Cmdlet          Get-PSScriptFileInfo                               1.0.4.1    Microsoft.PowerShell.PSResourceGet
Function        Import-PSGetRepository                             1.0.4.1    Microsoft.PowerShell.PSResourceGet
Cmdlet          Install-PSResource                                 1.0.4.1    Microsoft.PowerShell.PSResourceGet
Cmdlet          New-PSScriptFileInfo                               1.0.4.1    Microsoft.PowerShell.PSResourceGet
Cmdlet          Publish-PSResource                                 1.0.4.1    Microsoft.PowerShell.PSResourceGet
Cmdlet          Register-PSResourceRepository                      1.0.4.1    Microsoft.PowerShell.PSResourceGet
Cmdlet          Save-PSResource                                    1.0.4.1    Microsoft.PowerShell.PSResourceGet
Cmdlet          Set-PSResourceRepository                           1.0.4.1    Microsoft.PowerShell.PSResourceGet
Cmdlet          Test-PSScriptFileInfo                              1.0.4.1    Microsoft.PowerShell.PSResourceGet
Cmdlet          Uninstall-PSResource                               1.0.4.1    Microsoft.PowerShell.PSResourceGet
Cmdlet          Unregister-PSResourceRepository                    1.0.4.1    Microsoft.PowerShell.PSResourceGet
Cmdlet          Update-PSModuleManifest                            1.0.4.1    Microsoft.PowerShell.PSResourceGet
Cmdlet          Update-PSResource                                  1.0.4.1    Microsoft.PowerShell.PSResourceGet
Cmdlet          Update-PSScriptFileInfo                            1.0.4.1    Microsoft.PowerShell.PSResourceGet
````

### The content of PSResourceGet

List the content of the PSResourceGet-Module.

````powershell
Get-ChildItem -Path /usr/local/share/powershell/Modules/Microsoft.PowerShell.PSResourceGet/1.0.4.1

UnixMode         User Group         LastWriteTime         Size Name
--------         ---- -----         -------------         ---- ----
drwxr-xr-x       root root       04/06/2024 10:03         4096 dependencies
-rw-r--r--       root root       04/05/2024 21:21         1095 LICENSE
-rw-r--r--       root root       04/05/2024 21:21       343584 Microsoft.PowerShell.PSResourceGet.dll
-rw-r--r--       root root       04/05/2024 21:21        26144 Microsoft.PowerShell.PSResourceGet.psd1
-rw-r--r--       root root       04/05/2024 21:21        17926 Microsoft.PowerShell.PSResourceGet.psm1
-rw-r--r--       root root       04/05/2024 21:21       158819 Notice.txt
-rw-r--r--       root root       04/05/2024 21:21        23512 PSGet.Format.ps1xml
-rw-r--r--       root root       04/06/2024 10:03        30507 PSGetModuleInfo.xml
````

List the content of the dependencies-folder to understand what is included. As we can see, NuGet is included.

````powershell
Get-ChildItem -Path /usr/local/share/powershell/Modules/Microsoft.PowerShell.PSResourceGet/1.0.4.1/dependencies/

UnixMode         User Group         LastWriteTime         Size Name
--------         ---- -----         -------------         ---- ----
-rw-r--r--       root root       04/05/2024 21:21        26656 Microsoft.Bcl.AsyncInterfaces.dll
-rw-r--r--       root root       04/05/2024 21:21       722160 Newtonsoft.Json.dll
-rw-r--r--       root root       04/05/2024 21:21       613824 NuGet.Commands.dll
-rw-r--r--       root root       04/05/2024 21:21       122800 NuGet.Common.dll
-rw-r--r--       root root       04/05/2024 21:21       170424 NuGet.Configuration.dll
-rw-r--r--       root root       04/05/2024 21:21        67616 NuGet.Credentials.dll
-rw-r--r--       root root       04/05/2024 21:21        93728 NuGet.DependencyResolver.Core.dll
-rw-r--r--       root root       04/05/2024 21:21       131104 NuGet.Frameworks.dll
-rw-r--r--       root root       04/05/2024 21:21        56760 NuGet.LibraryModel.dll
-rw-r--r--       root root       04/05/2024 21:21       689088 NuGet.Packaging.dll
-rw-r--r--       root root       04/05/2024 21:21       219056 NuGet.ProjectModel.dll
-rw-r--r--       root root       04/05/2024 21:21       786368 NuGet.Protocol.dll
-rw-r--r--       root root       04/05/2024 21:21        65984 NuGet.Versioning.dll
-rw-r--r--       root root       04/05/2024 21:21        20856 System.Buffers.dll
-rw-r--r--       root root       04/05/2024 21:21       142240 System.Memory.dll
-rw-r--r--       root root       04/05/2024 21:21       115856 System.Numerics.Vectors.dll
-rw-r--r--       root root       04/05/2024 21:21        18024 System.Runtime.CompilerServices.Unsafe.dll
-rw-r--r--       root root       04/05/2024 21:21        79024 System.Text.Encodings.Web.dll
-rw-r--r--       root root       04/05/2024 21:21       642832 System.Text.Json.dll
-rw-r--r--       root root       04/05/2024 21:21        25984 System.Threading.Tasks.Extensions.dll
-rw-r--r--       root root       04/05/2024 21:21        25232 System.ValueTuple.dll
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
Register-PSResourceRepository -PSGallery -Verbose
Get-PSResourceRepository -Name PSGallery
````

Register the PSGallery v2.

````powershell
$parameters = @{
  Name     = 'PSGalleryV2'
  Uri      = 'https://www.powershellgallery.com/api/v2'
  Trusted  = $true
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

Set the PSGallery as trusted.

````powershell
Set-PSResourceRepository -Name "PSGallery" -Priority 25 -Trusted -PassThru
````

Install a Module.

````powershell
Install-PSResource -Name PsNetTools -Scope AllUsers -Verbose
````

Re-install a Module.

````powershell
Install-PSResource -Name PsNetTools -Scope AllUsers -Reinstall -Verbose
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

[ [Top](#table-of-contents) ]

## See also

[Microsoft.PowerShell.PSResourceGet](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.psresourceget/?view=powershellget-3.x) on Microsoft Learn.
