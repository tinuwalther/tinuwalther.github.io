---
layout: post
title:  "Powershell Profile"
author: Tinu
categories: "PowerShell-Basic"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Create your own PowerShell Profile](#create-your-own-powershell-profile)
  - [Scope](#scope)
  - [Profile](#profile)
- [Functions in your Profile](#functions-in-your-profile)
  - [Windows](#windows)
  - [Mac OS](#mac-os)
- [See also](#see-also)

## Create your own PowerShell Profile

### Scope

You can create a profile for the following scopes:

Description | Path
-|-
Current User, Current Host | $PROFILE
Current User, Current Host | $PROFILE.CurrentUserCurrentHost
Current User, All Hosts | $PROFILE.CurrentUserAllHosts
All Users, Current Host | $PROFILE.AllUsersCurrentHost
All Users, All Hosts | $PROFILE.AllUsersAllHosts

### Profile

To create your own Profile for WindowsPowerShell start Visual Studio Code and edit each of the following profile.ps1:

- Microsoft.PowerShell_profile.ps1
- Microsoft.VSCode_profile.ps1
- profile.ps1

````powershell
code $PROFILE

code $PROFILE.CurrentUserCurrentHost

code $PROFILE.CurrentUserAllHosts
````

## Functions in your Profile

My prefered functions in my own profile.ps1 on Windows, Mac and Linux:

````powershell
function Test-IsElevated {
    if($PSVersionTable.PSVersion.Major -lt 6){
        # Windows only
        $user = [Security.Principal.WindowsIdentity]::GetCurrent()
        $ret  = (New-Object Security.Principal.WindowsPrincipal $user).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
    }else{
        if($IsWindows){
            $user = [Security.Principal.WindowsIdentity]::GetCurrent()
            $ret  = (New-Object Security.Principal.WindowsPrincipal $user).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
        }
        if($IsLinux -or $IsMacOS){
            $ret  = (id -u) -eq 0
        }
    }
    $ret
}

function prompt
{
    if (Test-IsElevated) {
        $color = 'Red'
    }
    else{
        $color = 'Green'
    }
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Import-Module -Name CompletionPredictor
    Set-PSReadLineOption -PredictionViewStyle ListView
    $history = Get-History -ErrorAction Ignore

    $Version = "$($PSVersionTable.PSVersion.Major).$($PSVersionTable.PSVersion.Minor).$($PSVersionTable.PSVersion.Patch)"

    Write-Host "[$($history.count[-1])] " -NoNewline
    Write-Host "[$([Environment]::UserName)@$([Environment]::MachineName)] " -ForegroundColor $color -NoNewline
    Write-Host ("I ") -nonewline
    Write-Host (([char]9829) ) -ForegroundColor $color -nonewline
    Write-Host ("  PS $Version ") -nonewline

    Write-Host ("$(get-location)") -foregroundcolor $color -nonewline
    Write-Host (" >") -nonewline
    return " "

}
````

Output, if you start WindowsPowerShell:

````powershell
[0] [user@computer] I ♥ PS 5.1.1 C:\Users\Admin >
````

Output, if you start PowerShell:

````powershell
[0] [user@computer] I ♥ PS 7.1.4 C:\Users\Admin >
````

## See also

[About Profiles](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_profiles?view=powershell-6) on Microsoft Docs.
