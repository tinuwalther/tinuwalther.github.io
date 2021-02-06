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

You can create a profile for the following scope:

Description | Path
- | -
All Users, All Hosts | $PSHOME\Profile.ps1
All Users, Current Host | $PSHOME\Microsoft.PowerShell_profile.ps1
Current User, All Hosts | $Home\[My ]Documents\PowerShell\Profile.ps1
Current user, Current Host | $Home\[My ]Documents\PowerShell\Microsoft.PowerShell_profile.ps1

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