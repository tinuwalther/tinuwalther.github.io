---
layout: post
title:  "Powershell Profile"
author: Tinu
categories: "PowerShell-Basic"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Create your own PowerShell Profile](#create-your-own-powershell-profile)
  - [Scope](#scope)
  - [Profile](#profile)
- [Functions in your Profile](#functions-in-your-profile)
- [See also](#see-also)

# Create your own PowerShell Profile

## Scope

You can create a profile for the following scopes:

Description | Path
- | -
Current User, Current Host | $PROFILE
Current User, Current Host | $PROFILE.CurrentUserCurrentHost
Current User, All Hosts | $PROFILE.CurrentUserAllHosts
All Users, Current Host | $PROFILE.AllUsersCurrentHost
All Users, All Hosts | $PROFILE.AllUsersAllHosts

## Profile

To create your own Profile for WindowsPowerShell start a Windows PowerShell:

````powershell
New-Item $PsHome\Profile.ps1
ise $PsHome\Profile.ps1
````

To create your own Profile for PowerShell start a PowerShell:

````powershell
New-Item $PsHome\Profile.ps1
ise $PsHome\Profile.ps1
````

````powershell
code $PROFILE.CurrentUserAllHosts
````

# Functions in your Profile

My prefered functions in my own profile.ps1:

````powershell
function Test-IsAdministrator {
    $user = [Security.Principal.WindowsIdentity]::GetCurrent();
    (New-Object Security.Principal.WindowsPrincipal $user).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
}

function prompt
{

    if (Test-IsAdministrator) {
        $color = 'Red'
    }
    else{
        $color = 'Green'
    }
    
    $history = Get-History -ErrorAction Ignore
    $Version = "$($PSVersionTable.PSVersion.Major).$($PSVersionTable.PSVersion.Minor)"
    Write-Host "[$($history.count[-1])] " -NoNewline
    Write-Host "[$($env:ComputerName)] " -ForegroundColor $color -NoNewline
    Write-Host ("I ") -nonewline
    Write-Host (([char]9829) ) -ForegroundColor $color -nonewline
    Write-Host (" PS $Version ") -nonewline
    Write-Host ("$(get-location) ") -foregroundcolor $color -nonewline
    Write-Host (">") -nonewline -foregroundcolor $color
    return " "

}
````

Output, if you start WindowsPowerShell:

````powershell
[0] I ♥ PS 5.1 C:\Users\Admin >
````

Output, if you start PowerShell:

````powershell
[0] I ♥ PS 7.1 C:\Users\Admin >
````

# See also

[About Profiles](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_profiles?view=powershell-6) on Microsoft Docs.

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]