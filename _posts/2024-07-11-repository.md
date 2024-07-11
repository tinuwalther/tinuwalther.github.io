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
- [Offline Installation NuPkg](#offline-installation-nupkg)
- [See also](#see-also)

<!-- /TOC -->

## Offline Installation NuPkg

1. Download the Package:

````powershell
$RemoteRepository = 'http://nexus:8081/repository/PSModules'
$PackageName      = 'PsNetTools'
$PackageVersion   = '0.7.8'
$LocalPackagePath = '/home/nupkg'
$LocalRepoName    = 'LocalPackages'

$Properties = @{
  Uri     = "$($RemoteRepository)/$($PackageName)/$($PackageVersion)"
  OutFile = "$($LocalPackagePath)/$($PackageName).nupkg"
}
Invoke-WebRequest @Properties -Verbose
````

2. Register a local path as local Repository:

````powershell
Register-PSRepository -Name $LocalRepoName -SourceLocation $LocalPackagePath -InstallationPolicy Trusted
````

3. Install the Module from the local Repository:

````powershell
Install-Module $PackageName -Scope AllUsers -Repository $LocalRepoName -Force
````

[ [Top](#table-of-contents) ] 

## See also

[Working with Private PowerShellGet Repositories](https://docs.microsoft.com/en-us/powershell/scripting/gallery/how-to/working-with-local-psrepositories?view=powershell-7.1) on Microsoft Docs.
