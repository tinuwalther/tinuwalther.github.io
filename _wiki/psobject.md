---
title: PSObject
date: '2015-10-08T20:42:55+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- PSObject
- Scripting
wordpress_id: 1404
layout: post
permalink: /wiki/psobject/
render_with_liquid: false
---

PSObject versus PSCustomObject

## PowerShell Version 1.0

 Spalten werden gemäss der Anordnung innerhalb der Schleife dargestellt. 

```
function GetInstaledSoftware{
    <#
        Get installed Software
    #>
    $function = $($MyInvocation.MyCommand.Name)
    $ret = @()
    try{
        if($psdebug){write-verbose "Running $($function) ..." -verbose}
        Get-WmiObject -Class Win32_Product | %{
            $obj = New-Object PSObject
            $obj | Add-Member NoteProperty Name        $_.Name
            $obj | Add-Member NoteProperty Version     $_.Version
            $obj | Add-Member NoteProperty Description $_.Description
            $obj | Add-Member NoteProperty InstallDate $_.InstallDate
            $obj | Add-Member NoteProperty PackageName $_.PackageName
            $obj | Add-Member NoteProperty Vendor      $_.Vendor
            $ret += $obj
       }
    }
    catch [Exception]{
          write-host "$($function): $($_.Exception.Message)" -ForegroundColor Red
          $error.clear()
          $ret += $obj
    }
    return $ret
}
GetInstaledSoftware | sort vendor | ft -AutoSiz
```

## PowerShell Version 2.0

 Spalten werden willkürlich angeordnet dargestellt. 

```
function GetInstaledSoftware{
    <# Get installed Software #>
    $function = $($MyInvocation.MyCommand.Name)
    $ret = @()
    try{
        if($psdebug){write-verbose "Running $($function) ..." -verbose}
        Get-WmiObject -Class Win32_Product | %{
            $obj = New-Object PSObject -Property @{ 
                Name        = $_.Name
                Version     = $_.Version
                Description = $_.Description
                InstallDate = $_.InstallDate
                PackageName = $_.PackageName
                Vendor      = $_.Vendor
            }
            $ret += $obj
       }
    }
    catch [Exception]{
          write-host "$($function): $($_.Exception.Message)" -ForegroundColor Red
          $error.clear()
          $ret += $obj
    }
    return $ret
}
GetInstaledSoftware | sort vendor | ft -AutoSiz
```

## PowerShell Version 3.0

 Spalten werden gemäss der Anordnung innerhalb der Schleife dargestellt. 

```
function GetInstaledSoftware{
    <# Get installed Software #>
    $function = $($MyInvocation.MyCommand.Name)
    $ret = @()
    try{
        if($psdebug){write-verbose "Running $($function) ..." -verbose}
        Get-WmiObject -Class Win32_Product | %{
            $obj = [PSCustomObject]@{
                InstallDate = $_.InstallDate
                Vendor      = $_.Vendor
                Name        = $_.Name
                PackageName = $_.PackageName
                Description = $_.Description
                Version     = $_.Version
            }
            $ret += $obj
        }
    }
    catch [Exception]{
          write-host "$($function): $($_.Exception.Message)" -ForegroundColor Red
          $error.clear()
          $ret += $obj
    }
    return $ret
}
GetInstaledSoftware | sort vendor | ft -AutoSize

```