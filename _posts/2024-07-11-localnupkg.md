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
- [Offline Installation Nuget Package](#offline-installation-nuget-package)
- [See also](#see-also)

<!-- /TOC -->

## Offline Installation Nuget Package

Download the Package from a remote NuGet Repository:

````powershell
$RemoteRepoCreds  = Get-Credential
$RemoteRepository = 'http://nexus:8081/repository/PSModules'
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

Register a local path as Nuget Repository:

````powershell
$Properties = @{
  Name               = $LocalRepoName
  SourceLocation     = $LocalPackagePath
  InstallationPolicy = 'Trusted'
}
Register-PSRepository @Properties -Verbose
````

Install the Module from the local Repository:

````powershell
Install-Module $PackageName -Scope AllUsers -Repository $LocalRepoName -Force
````

[ [Top](#table-of-contents) ] 

## See also

[Working with Private PowerShellGet Repositories](https://docs.microsoft.com/en-us/powershell/scripting/gallery/how-to/working-with-local-psrepositories?view=powershell-7.1) on Microsoft Docs.
