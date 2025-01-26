---
layout: post
title:  "Local Nuget Repositories"
author: Tinu
categories: "PowerShell-Repositories"
tags:   PowerShell News
permalink: /posts/:title:output_ext
---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Offline Installation of Nuget Packages](#offline-installation-of-nuget-packages)
  - [Find the Package](#find-the-package)
  - [Download the Package](#download-the-package)
  - [Register a local Repository](#register-a-local-repository)
  - [Install the Module](#install-the-module)
- [Extract the Nuget Package](#extract-the-nuget-package)
- [CleanUp](#cleanup)
- [See also](#see-also)

## Offline Installation of Nuget Packages

To install a Nuget package without registering a remote repository, you must download the package, register a local path as a local repository and install the package from the local repository.

### Find the Package

Find the Package and Version in a remote NuGet Repository:

````powershell
$RemoteRepoCreds  = Get-Credential
$RemoteRepository = 'http://nexus:8081/repository/PSModules' # https://www.powershellgallery.com/api/v2
$PackageName      = 'PsNetTools'

$Properties = @{
  Uri        = "$($RemoteRepository)/FindPackagesById()?id='$($PackageName)'"
  Credential = $RemoteRepoCreds
}
$Response = Invoke-WebRequest @Properties -AllowUnencryptedAuthentication -Verbose
[xml]$xml = $Response.Content
````

### Download the Package

Download the Package from a remote NuGet Repository:

````powershell
$RemoteRepoCreds  = Get-Credential
$PackageName      = $xml.feed.entry.properties.Title
$PackageVersion   = $xml.feed.entry.properties.Version
$LocalPackagePath = '/tmp/nupkg'
$LocalRepoName    = 'LocalPackages'
if(-not(Test-Path $LocalPackagePath)){New-Item -Path $LocalPackagePath -ItemType Directory -Force}

$Properties = @{
  Uri        = "$($RemoteRepository)/$($PackageName)/$($PackageVersion)"
  OutFile    = "$($LocalPackagePath)/$($PackageName).nupkg"
  Credential = $RemoteRepoCreds
  PassThru   = $true
}
Invoke-WebRequest @Properties -AllowUnencryptedAuthentication -Verbose
Get-ChildItem $LocalPackagePath
````

Output:

````powershell
VERBOSE: Requested HTTP/1.1 GET with 0-byte payload
VERBOSE: Received HTTP/1.1 21510-byte response of content type application/zip

StatusCode        : 200
StatusDescription : OK
Content           : {80, 75, 3, 4…}
RawContent        : HTTP/1.1 200 OK
                    Date: Fri, 12 Jul 2024 07:28:48 GMT
                    Server: Nexus/3.70.1-02
                    Server: (OSS)
                    X-Content-Type-Options: nosniff
                    Content-Security-Policy: sandbox allow-forms allow-modals allow-popups allow-p…
Headers           : {[Date, System.String[]], [Server, System.String[]], [X-Content-Type-Options, System.String[]], [Co
                    ntent-Security-Policy, System.String[]]…}
RawContentLength  : 21510
RelationLink      : {}

VERBOSE: File Name: PsNetTools.nupkg
    Directory: /tmp/nupkg

UnixMode         User Group         LastWriteTime         Size Name
--------         ---- -----         -------------         ---- ----
-rw-r--r--       root root       07/12/2024 08:57        21510 PsNetTools.nupkg
````

### Register a local Repository

Register a local path as local Repository:

````powershell
$Properties = @{
  Name               = $LocalRepoName
  SourceLocation     = $LocalPackagePath
  InstallationPolicy = 'Trusted'
}
Register-PSRepository @Properties -Verbose
````

Output:

````powershell
VERBOSE: Repository details, Name = 'PSGallery', Location = 'https://www.powershellgallery.com/api/v2'; IsTrusted = 'False'; IsRegistered = 'True'.
VERBOSE: Performing the operation "Register Module Repository." on target "Module Repository 'LocalPackages' (/tmp/nupkg) in provider 'PowerShellGet'.".
VERBOSE: The specified PackageManagement provider name 'NuGet'.
VERBOSE: Successfully registered the repository 'LocalPackages' with source location '/tmp/nupkg'.
VERBOSE: Repository details, Name = 'LocalPackages', Location = '/tmp/nupkg'; IsTrusted = 'True'; IsRegistered = 'True'.
````

### Install the Module

Install the Module from the local Repository:

````powershell
$Properties = @{
  Name       = $PackageName
  Repository = $LocalRepoName
  Scope      = 'AllUsers'
  Force      = $true
}
Install-Module @Properties -Verbose
````

Output:

````powershell
VERBOSE: Suppressed Verbose Repository details, Name = 'LocalPackages', Location = '/tmp/nupkg'; IsTrusted = 'True'; IsRegistered = 'True'.
VERBOSE: Repository details, Name = 'LocalPackages', Location = '/tmp/nupkg'; IsTrusted = 'True'; IsRegistered = 'True'.
VERBOSE: Using the provider 'PowerShellGet' for searching packages.
VERBOSE: Using the specified source names : 'LocalPackages'.
VERBOSE: Getting the provider object for the PackageManagement Provider 'NuGet'.
VERBOSE: The specified Location is '/tmp/nupkg' and PackageManagementProvider is 'NuGet'.
VERBOSE: Total package yield:'1' for the specified package 'PsNetTools'.
VERBOSE: Performing the operation "Install-Module" on target "Version '0.7.8' of module 'PsNetTools'".
VERBOSE: The installation scope is specified to be 'AllUsers'.
VERBOSE: The specified module will be installed in '/usr/local/share/powershell/Modules'.
VERBOSE: The specified Location is 'NuGet' and PackageManagementProvider is 'NuGet'.
VERBOSE: Downloading module 'PsNetTools' with version '0.7.8' from the repository '/tmp/nupkg'.
VERBOSE: InstallPackageLocal' - name='PsNetTools', version='0.7.8',destination='/tmp/1676781311'
VERBOSE: Validating the 'PsNetTools' module contents under '/tmp/1676781311/PsNetTools.0.7.8' path.
VERBOSE: Test-ModuleManifest successfully validated the module manifest file '/tmp/1676781311/PsNetTools.0.7.8'.
VERBOSE: Module 'PsNetTools' was installed successfully to path '/usr/local/share/powershell/Modules/PsNetTools/0.7.8'.
````

[ [Top](#) ] 

## Extract the Nuget Package

It's also possible, to expand the Nuget Package:

````powershell
$Properties = @{
  Path            = "$($LocalPackagePath)/$($PackageName).nupkg"
  DestinationPath = "/tmp/$($PackageName)/$($PackageVersion)"
  PassThru        = $true
  Force           = $true
}
Expand-Archive @Properties -Verbose
````

Output:

````powershell
    Directory: /tmp/nupkg/PsNetTools/0.7.8

UnixMode         User Group         LastWriteTime         Size Name
--------         ---- -----         -------------         ---- ----
drwxr-xr-x       root root       07/12/2024 08:34         4096 _rels
-rw-r--r--       root root       04/29/2023 14:28         2032 PsNetTools.nuspec
-rw-r--r--       root root       01/17/2023 07:17        28979 PsNetTools.md
-rw-r--r--       root root       04/29/2023 12:08         5196 PsNetTools.psd1
-rw-r--r--       root root       04/29/2023 12:08       108025 PsNetTools.psm1
-rw-r--r--       root root       04/29/2023 14:28          592 [Content_Types].xml

    Directory: /tmp/nupkg/PsNetTools/0.7.8/package/services/metadata

UnixMode         User Group         LastWriteTime         Size Name
--------         ---- -----         -------------         ---- ----
drwxr-xr-x       root root       07/12/2024 08:34         4096 core-properties

    Directory: /tmp/nupkg/PsNetTools/0.7.8/package/services/metadata/core-properties

UnixMode         User Group         LastWriteTime         Size Name
--------         ---- -----         -------------         ---- ----
-rw-r--r--       root root       04/29/2023 14:28         2004 2034ad0f68304a1980ce799ce4615f52.psmdcp
````

You need only the following files:

- PsNetTools.md 
- PsNetTools.psd1 
- PsNetTools.psm1

All others can be removed:

````powershell
$Properties = @{
  Path    = "/tmp/$($PackageName)/$($PackageVersion)"
  Exclude = @('PsNetTools.ps*', 'PsNetTools.md')
  Recurse = $true
  Force   = $true
}
Remove-Item @Properties -Verbose
````

Output:

````powershell
VERBOSE: Performing the operation "Remove Directory" on target "/tmp/PsNetTools/0.7.8/_rels".
VERBOSE: Performing the operation "Remove Directory" on target "/tmp/PsNetTools/0.7.8/package".
VERBOSE: Performing the operation "Remove File" on target "/tmp/PsNetTools/0.7.8/[Content_Types].xml".
VERBOSE: Performing the operation "Remove File" on target "/tmp/PsNetTools/0.7.8/PsNetTools.nuspec".
````

[ [Top](#) ] 

## CleanUp

CleanUp Module:

````powershell
Uninstall-Module -Name $PackageName -Force
Remove-Item "/tmp/$($PackageName)/" -Recurse -Force
````

CleanUp Repository:

````powershell
Unregister-PSRepository -Name $LocalRepoName
Remove-Item $LocalPackagePath -Recurse -Force
````

[ [Top](#table-of-contents) ] 

## See also

[Working with Private PowerShellGet Repositories](https://docs.microsoft.com/en-us/powershell/scripting/gallery/how-to/working-with-local-psrepositories?view=powershell-7.1) on Microsoft Docs.
