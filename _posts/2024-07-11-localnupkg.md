---
layout: post
title:  "Local Nuget Repositories"
author: Tinu
categories: "PowerShell-Repositories"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

## Table of Contents

<!-- TOC -->

- [Table of Contents](#table-of-contents)
- [Offline Installation of Nuget Packages](#offline-installation-of-nuget-packages)
    - [Download the Package](#download-the-package)
    - [Register a local Repository](#register-a-local-repository)
    - [Install the Module](#install-the-module)
- [See also](#see-also)

<!-- /TOC -->

## Offline Installation of Nuget Packages

To install a Nuget package without registering a remote repository, you must download the package, register a local path as a local repository and install the package from the local repository.

### Download the Package

Download the Package from a remote NuGet Repository:

````powershell
$RemoteRepoCreds  = Get-Credential
$RemoteRepository = 'http://nexus:8081/repository/PSModules' # https://www.powershellgallery.com/api/v2
$PackageName      = 'PsNetTools'
$PackageVersion   = '0.7.8'
$LocalPackagePath = '/home/nupkg'
$LocalRepoName    = 'LocalPackages'

$Properties = @{
  Uri        = "$($RemoteRepository)/$($PackageName)/$($PackageVersion)"
  OutFile    = "$($LocalPackagePath)/$($PackageName).nupkg"
  Credential = $RemoteRepoCreds
}
Invoke-WebRequest @Properties -Verbose
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

### Install the Module

Install the Module from the local Repository:

````powershell
Install-Module $PackageName -Scope AllUsers -Repository $LocalRepoName -Force
````

[ [Top](#table-of-contents) ] 

## See also

[Working with Private PowerShellGet Repositories](https://docs.microsoft.com/en-us/powershell/scripting/gallery/how-to/working-with-local-psrepositories?view=powershell-7.1) on Microsoft Docs.
