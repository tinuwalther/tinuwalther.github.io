---
title: ZIP entpacken
date: '2014-12-17T12:20:51+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- ZIP
wordpress_id: 483
layout: post
permalink: /wiki/zip-entpacken/
render_with_liquid: false
---

# Entpacken eines ZIP-FIles mit PowerShell

```csharp
function ExtractZipArchive{
    <#
    .SYNOPSIS
        Extract an archive

    .DESCRIPTION
        Extract an archive from zip file

    .PARAMETER Archive
        Local path to the archive

    .PARAMETER Path
        Local path where to extract

    .EXAMPLE
        ExtractZipArchive -Archive 'U:\tmp\archive.zip' -Path 'U:\tmp\archive'

    #>
    param(
        [Parameter(Mandatory=$true)][String] $Archive,
        [Parameter(Mandatory=$true)][String] $Path
    )
    $ret = $true
    $function = $($MyInvocation.MyCommand.Name)
    $option = 16 #Click "Yes to All" in any dialog box displayed.
    try{
        $shell = new-object -com shell.application
        if ($psdebug){write-host "$($function) Shell.Application initiated"}
            $zip = $shell.NameSpace($Archive)
            if ($psdebug){write-host "$($function) Shell.NameSpace initiated"}
            foreach($item in $zip.items()){
                $shell.Namespace($Path).copyhere($item, $option)
                if ($psdebug){write-host "$($function) Extract file"}
        }
    }
    catch [Exception]{
        write-host "$($function): Params($($Archive), $($Path)): $($_.Exception.Message)"
        $ret = $false
    }
    return $ret
}

```