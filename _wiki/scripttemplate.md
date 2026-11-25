---
title: Scripttemplate
date: '2014-11-27T21:15:00+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Scripttemplate
wordpress_id: 223
layout: post
permalink: /wiki/scripttemplate/
render_with_liquid: false
---

## PowerShell-Scripttemplate

 Mein neustes Template. 

```
<#
    .SYNOPSIS
    Kurzbeschrieb des Scripts

    .DESCRIPTION
    Ausführliche Beschreibung was das Script macht

    .PARAMETER Inputfile
    Fullpath to the inputfile

    .PARAMETER psdebug
    Run Script in debug mode
 
    .NOTES
     Author: Martin Walther 
     Date created: 12.10.2014 

    .EXAMPLE 
    .\Script.ps1-XmlFile 'C:\scripts\config.xml' -psdebug 
#>

#region param
[CmdletBinding()]
param(
    [Parameter(Mandatory = $false, HelpMessage = 'Enter the full-filename of the inputfile.')]
    [String]$Inputfile = '',
    [Parameter(Mandatory=$false)]
    [switch]$psdebug = $false
)
#endregion

#region functions
function Get-LocalUser{
    <# Returns the given Account as an object or null #>
    param(
        [Parameter(Mandatory = $true)][String]$Name = ''
    )
    $function = $($MyInvocation.MyCommand.Name)
    Write-Verbose $function
    $ret = $null
    try{
        $ret = Get-WMIObject Win32_UserAccount -Filter "Name='$Name'"
    }
    catch [Exception]{
        if($psdebug){write-host "$(Get-Date -DisplayHint DateTime) $($function): $($_.Exception.Message)" -ForegroundColor Red}
        "$(Get-Date -DisplayHint DateTime) [   ERROR   ] $($function): $($_.Exception.Message)" | Out-File -FilePath "$($script:Scriptpath)\$($script:Logfile)" -Append -Encoding default
        $error.clear()
    }
    finally{
        #Clean up
    }
    return $ret
}
#endregion

if($PSVersionTable.PSVersion.Major -ge 4){
#region scriptglobals
$script:ScriptStart  = (get-date)
$script:Scriptpath   = Split-Path -Parent $MyInvocation.MyCommand.Path
$script:Scriptname   = $MyInvocation.MyCommand.ToString()
$script:Basename     = $script:Scriptname.Remove($script:Scriptname.Length -4)
$script:Logfile      = $($script:Scriptname).Replace('.ps1','.log')
$script:version      = '1.0.0.0000'
$script:Scriptreturn = @()
#endregion

#region script control
Set-StrictMode -Version latest
if($Error.Count -gt 0){$Error.Clear()}
if($psdebug){
    $ErrorActionPreference = 'Stop'
}
else{
    $ErrorActionPreference = 'SilentlyContinue'
}

"$(Get-Date -DisplayHint DateTime) [INFORMATION] Start $($script:Scriptname), Version $($script:version)" | Out-File -FilePath "$($script:Scriptpath)\$($script:Logfile)" -Append -Encoding default
$script:Scriptreturn += Get-LocalUser -Name Admin
if(!([String]::IsNullOrEmpty($Inputfile)) -and (Test-Path $Inputfile)){
    Get-Content $Inputfile
}
else{
    "$(Get-Date -DisplayHint DateTime) [  WARNING  ] Inputfile '$($Inputfile)' not found" | Out-File -FilePath "$($script:Scriptpath)\$($script:Logfile)" -Append -Encoding default
}

"$(Get-Date -DisplayHint DateTime) [INFORMATION] End $($script:Scriptname), Errorcount $($Error.Count)" | Out-File -FilePath "$($script:Scriptpath)\$($script:Logfile)" -Append -Encoding default

#load the current logfile
Get-Content "$($script:Scriptpath)\$($script:Logfile)" -raw

$script:Scriptreturn
#endregion
}
```

 Copyright © 2014 Martin Walther