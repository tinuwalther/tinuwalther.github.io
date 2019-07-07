---
layout: post
title:  "Powershell Profile"
author: Tinu
categories: "PowerShell-Basic"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

# Table of Contents

- [Table of Contents](#Table-of-Contents)
- [Create your own PowerShell Profile](#Create-your-own-PowerShell-Profile)
- [Functions in your Profile](#Functions-in-your-Profile)
- [See also](#See-also)

# Create your own PowerShell Profile

To create your own Profile for WindowsPowerShell:

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
    Write-Host "[$($history.count[-1])] " -NoNewline
    Write-Host ("I ") -nonewline
    Write-Host (([char]9829) ) -ForegroundColor $color -nonewline
    Write-Host (" PS ") -nonewline
    Write-Host ("$(get-location) ") -foregroundcolor $color -nonewline
    Write-Host (">") -nonewline -foregroundcolor $color
    return " "

}
````

Output, if you start PowerShell:

````powershell
[0] I ♥ PS C:\Users\Admin > Get-History -Count 1
[1] I ♥ PS C:\Users\Admin > Invoke-History 1
Get-History -Count 1

  Id CommandLine
  -- -----------
   1 Get-History -Count 1
````

# See also

[About Profiles](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_profiles?view=powershell-6) on Microsoft Docs.

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]