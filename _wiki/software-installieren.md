---
title: Software installieren
date: '2017-08-09T16:50:32+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Software
wordpress_id: 2324
layout: post
permalink: /wiki/software-installieren/
render_with_liquid: false
---

Software installieren/deinstallieren mit msiexec.

## Msiexec Optionen

```
msiexec /Option [Optional Parameter]
```

### Install Options

```
</package | /i>
    Installs or configures a product
/a
    Administrative install - Installs a product on the network
/j<u|m> [/t ] [/g ]
    Advertises a product - m to all users, u to current user
</uninstall | /x>
    Uninstalls the product
```

### Display Options

```
/quiet
    Quiet mode, no user interaction
/passive
    Unattended mode - progress bar only
/q[n|b|r|f]
    Sets user interface level
    n - No UI
    b - Basic UI
    r - Reduced UI
    f - Full UI (default)
/help
    Help information
```

### Restart Options

```
/norestart
    Do not restart after the installation is complete
/promptrestart
    Prompts the user for restart if necessary
/forcerestart
    Always restart the computer after installation
```

### Logging Options

```
/l[i|w|e|a|r|u|c|m|o|p|v|x|+|!|*]
    i - Status messages
    w - Nonfatal warnings
    e - All error messages
    a - Start up of actions
    r - Action-specific records
    u - User requests
    c - Initial UI parameters
    m - Out-of-memory or fatal exit information
    o - Out-of-disk-space messages
    p - Terminal properties
    v - Verbose output
    x - Extra debugging information
    + - Append to existing log file
    ! - Flush each line to the log
    * - Log all information, except for v and x options
/log
    Equivalent of /l*
```

### Update Options

```
/update [;Update2.msp]
    Applies update(s)
/uninstall [;Update2.msp] /package
    Remove update(s) for a product
```

### Repair Options

```
/f[p|e|c|m|s|o|d|a|u|v]
    Repairs a product
    p - only if file is missing
    o - if file is missing or an older version is installed (default)
    e - if file is missing or an equal or older version is installed
    d - if file is missing or a different version is installed
    c - if file is missing or checksum does not match the calculated value
    a - forces all files to be reinstalled
    u - all required user-specific registry entries (default)
    m - all required computer-specific registry entries (default)
    s - all existing shortcuts (default)
    v - runs from source and recaches local package
```

## Installation

### Msiexec

 Installation mit Msiexec durchführen und ein separates MSI-Logfile erstellen: 

```
$Inputfile   = Get-ChildItem $($ProductPath) -Filter "*.msi"
$InstallArgs = @{}
$InstallArgs.FilePath     = "msiexec.exe"
$InstallArgs.ArgumentList = @()
$InstallArgs.ArgumentList += "/i"
$InstallArgs.ArgumentList += "$($Inputfile.FullName)"
$InstallArgs.ArgumentList += "SERVER=$($var)"
$InstallArgs.ArgumentList += "/quiet"
$InstallArgs.ArgumentList += "/L*v $($ProductPath)\$($Inputfile.Name).log"
$InstallArgs.Wait         = $true
$ReturnCode = (Start-Process @InstallArgs -PassThru).ExitCode
$content = Get-Content -Path $logfile
$content | Select-String -Pattern "Error\s\d+.+\.\s" -AllMatches | Select-Object -ExpandProperty matches | Select-Object -ExpandProperty value | Select-Object -Last 1
```

### PowerShell-Script

 Installation mit einem PowerShell-Script durchführen, alle Aktionen werden mit dem Script durchgeführt und geloggt: 

```
$Inputfile   = Get-ChildItem $($ProductPath) -Filter "*.ps1"
$InstallArgs = @{}
$InstallArgs.FilePath     = "powershell.exe"
$InstallArgs.ArgumentList = @()
$InstallArgs.ArgumentList += "-ExecutionPolicy bypass -noprofile"
$InstallArgs.ArgumentList += "-file $($Inputfile.FullName)"
$InstallArgs.Wait         = $true
$ReturnCode = (Start-Process @InstallArgs -PassThru).ExitCode
```

## Deinstallation

### Product-GUID in der Registry suchen

```
function Get-ProductGuidFromRegistry{
    [cmdletbinding()]
    param(
        [string]$regpath = 'HKLM:\SOFTWARE\Classes\Installer\Products',
        [string]$product = ''
    )
    $ret = $null
    $collection = Get-ChildItem $regpath
    foreach($item in $collection){
        $result = Get-ItemProperty -Path "$($regpath)\$($item.PSChildName)" -Name ProductName
        if($($result.ProductName) -eq $product){
            $ret = $($item.PSChildName)
        }
    }
    return $ret
}
```

### Object aus WMI holen

```
function Get-MsiPackage{
    [cmdletBinding()]
    Param(
        [Parameter(Mandatory=$true,ParameterSetName="Name")][String]$Name,
        [Parameter(Mandatory=$true,ParameterSetName="guid")][String]$GUID
    )
    if ($Name){
        $Application = Get-WmiObject -Class Win32_Product -Filter "Name = '$name'"
    }
    elseif($GUID){
        $Application = Get-WmiObject -Class Win32_Product -Filter "IdentifyingNumber = '$GUID'"
    }
    if ($Application){
      write-host "Application Found $($Application.Name). Starting uninstallation process."
      Return $Application
    } 
    else{
      write-host "The Application could not be found, so it's assumed that it isn't installed."
      Return -1
    }
}
```

### Deinstallation starten

```
$msiobj = Get-MsiPackage -Name "Symantec NetBackup Client"
if($msiobj -ne -1){
    #Application found
    $ProductGuid    = Get-ProductGuidFromRegistry -regpath "HKLM:\SOFTWARE\Classes\Installer\Products" -product 'Symantec NetBackup Client'
    $LastUsedSource = (Get-ItemProperty -Path "HKLM:\SOFTWARE\Classes\Installer\Products\$($ProductGuid)\SourceList" -Name LastUsedSource).LastUsedSource
    write-output "LastUsedSource: $($LastUsedSource)"
    $logfile = 'C:\Admin\Logs\RemoveNetbackup.log'
    if(-not(Test-Path "C:\Admin\Logs")){$null = md "C:\Admin\Logs"}
    $params = @(
        "/x"
        "$($msiobj.IdentifyingNumber)"
        "/quiet"
        "/L*v $($logfile)"
    )
    $spArgs = @{
        "FilePath"     = "msiexec.exe"
        "ArgumentList" = $params
        "Wait"         = $true
    }
    $ReturnCode = (Start-Process @spArgs -PassThru).ExitCode
    $content = Get-Content -Path $logfile
    $content | Select-String -Pattern "Error\s\d+.+\.\s" -AllMatches | Select-Object -ExpandProperty matches | Select-Object -ExpandProperty value | Select-Object -Last 1
}
Write-Output $ReturnCode
```