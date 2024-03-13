---
layout: post
title:  "Module & Script Management"
author: Tinu
categories: "PowerShell-Module"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [PowerShell Gallery](#powershell-gallery)
- [Internal Gallery](#internal-gallery)
- [Publish Modules](#publish-modules)
- [Publish Scripts](#publish-scripts)
- [Script Template](#script-template)

## PowerShell Gallery

[PowerShell Gallery API](https://www.powershellgallery.com/api/v2)

## Internal Gallery

[Working with Private PowerShellGet Repositories](https://docs.microsoft.com/en-us/powershell/scripting/gallery/how-to/working-with-local-psrepositories?view=powershell-7.1)

NuGet.exe must be available in:
- C:\ProgramData\Microsoft\Windows\PowerShell\PowerShellGet\
- C:\Users\info\AppData\Local\Microsoft\Windows\PowerShell\PowerShellGet\
- NuGet.exe can be downloaded from https://aka.ms/psget-nugetexe

HTTPS-Repository or an SMB-Share...

````powershell
$Modules = @{
    Name                 = "HomeGallery"
    SourceLocation       = "\\Server\psrepo\modules"
    ScriptSourceLocation = "\\Server\psrepo\modules"
    InstallationPolicy   = 'Trusted'
}
$Scripts = @{
    Name                 = "HomeGallery"
    SourceLocation       = "\\Server\psrepo\scripts"
    ScriptSourceLocation = "\\Server\psrepo\scripts"
    InstallationPolicy   = 'Trusted'
}
Register-PSRepository @Modules
Register-PSRepository @Scripts
Get-PSRepository | Select-Object Name,Trusted,SourceLocation,ScriptSourceLocation,Registered,PackageManagementProvider | ft -a
````

## Publish Modules

Publish a Module to a file share repo - the NuGet API key must be a non-blank string.

````powershell
Publish-Module -Path 'D:\temp\PsNetTools' -Repository HomeGallery -NuGetApiKey 'AnyStringWillDo'
````

## Publish Scripts

````powershell
$Script  = 'Add-MongoDBDocument'
$Metadata = @{
    Version     = '1.0.0'
    Author      = 'it@martin-walther.ch'
    Guid        = New-Guid
    Description = 'Add a document in the inventory-table of the local MongoDB'
    Path        = "D:\temp\Database\$($Script).ps1"
}
Update-ScriptFileInfo @Metadata
Publish-Script -Path "D:\temp\Database\$($Script).ps1" -Repository HomeGallery -Force
````

[ [Top](#table-of-contents) ]

## Script Template

````powershell
<#PSScriptInfo

.VERSION 0.0.0

.GUID a9742dfa-3693-4538-ae02-851b26117334

.AUTHOR it@martin-walther.ch

.COMPANYNAME

.COPYRIGHT

.TAGS

.LICENSEURI

.PROJECTURI

.ICONURI

.EXTERNALMODULEDEPENDENCIES 

.REQUIREDSCRIPTS

.EXTERNALSCRIPTDEPENDENCIES

.RELEASENOTES


.PRIVATEDATA

#> 



<#

.DESCRIPTION 
Add a document in the inventory-table of the local MongoDB

.EXAMPLE
Add-MongoDBDocument -Document $Document

#> 

[CmdletBinding()]
param (
    [Parameter(
        Mandatory=$true,
        ValueFromPipeline=$true,
        ValueFromPipelineByPropertyName=$true,
        Position = 0
    )]
    [String[]] $InputString
)

begin {
    $StartTime = Get-Date
    $function = $($MyInvocation.MyCommand.Name)
    foreach($item in $PSBoundParameters.keys){
        $params = "$($params) -$($item) $($PSBoundParameters[$item])"
    }
    Write-Verbose "[Begin] $($function)$($params)"
    $ret = @()
}

process {
    $ret = foreach($item in $InputString){
        try{
            $item
        }catch{
            Write-Warning "$($function), $($item), $($_.Exception.Message)"
        }
    }
    return $ret
}

end {
    Write-Verbose "[End] $($function)"
    Write-Host "Duration: $(New-TimeSpan -Start $StartTime -End (Get-Date) | % { "{1:0}h {2:0}m {3:0}s {4:000}ms" -f $_.Days, $_.Hours, $_.Minutes, $_.Seconds, $_.Milliseconds })`n"
}
````

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]
