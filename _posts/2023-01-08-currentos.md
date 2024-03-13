---
layout: post
title:  "How to get the current OS"
author: Tinu
categories: "PowerShell-Basic"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

## Table of Contents

- [Table of Contents](#table-of-contents)
  - [PowerShell 7](#powershell-7)
  - [Windows PowerShell](#windows-powershell)
  - [Unknown Environment](#unknown-environment)
- [See also](#see-also)

### PowerShell 7

With PowerShell 7 it's easy to determine the current os:

````powershell
$IsMacOS
$IsLinux
$IsWindows
````

### Windows PowerShell

In Windows PowerShell it's easy to determine the current os:

````powershell
[Environment]::OSVersion
````

### Unknown Environment

If you don't know which PowerShell you running on which OS, you can use the following code:

````powershell
# define an enumerator for the OS-type
enum OSType {
    Linux
    Mac
    Windows
}

function Get-CurrentOS {
    # if the PSVersion is less than 6, it's Windows PowerShell
    if($PSVersionTable.PSVersion.Major -lt 6){
        return [OSType]::Windows
    }
    # if the PSVersion is greather than 6, you can use the pwsh constants
    else{
        if($IsMacOS)   {return [OSType]::Mac}
        if($IsLinux)   {return [OSType]::Linux}
        if($IsWindows) {return [OSType]::Windows} 
    }
}

switch(Get-CurrentOS){
    Mac {
        $OSVersion = "$(sw_vers -productName) $(sw_vers -productVersion).$(sw_vers -buildVersion)"
        Write-Host "Running on $($OSVersion)" -ForegroundColor Cyan
    }
    Linux {
        $OSVersion = $((Get-Content /etc/*release | Select-String -Pattern 'DISTRIB_DESCRIPTION=') -replace 'DISTRIB_DESCRIPTION=')
        Write-Host "Running on $($OSVersion)" -ForegroundColor Cyan
    }
    Windows {
        $OSVersion = "$((Get-CimInstance -ClassName Win32_OperatingSystem).Caption) ($([System.Environment]::OSVersion.Version.ToString()))"
        Write-Host "Running on $($OSVersion)" -ForegroundColor Cyan
    }
}
````

## See also

[Determine the OS version, Linux and Windows from Powershell](https://stackoverflow.com/questions/44703646/determine-the-os-version-linux-and-windows-from-powershell) on stack overflow
