---
title: Windows Update
date: '2015-10-02T16:56:22+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- PSObject
- Windows Server
wordpress_id: 1377
layout: post
permalink: /wiki/windows-update/
render_with_liquid: false
---

## Installierte Hotfixes mit PowerShell auflisten

 Ab PowerShell Version 2.0 

```
function GetHotFixes{
    <# List all installed hotfies #>
    $function = $($MyInvocation.MyCommand.Name)
    $ret = @()
    try{
        get-hotfix | Selece HotFixID,Description,InstalledBy,InstalledOn | %{
            $obj = New-Object PSObject
            Add-Member -InputObject $obj -MemberType NoteProperty -Name HotFixID -Value $_.HotFixID
            Add-Member -InputObject $obj -MemberType NoteProperty -Name Description -Value $_.Description
            Add-Member -InputObject $obj -MemberType NoteProperty -Name InstalledBy -Value $_.InstalledBy
            Add-Member -InputObject $obj -MemberType NoteProperty -Name InstalledOn -Value $_.InstalledOn
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
```

## Alle installierten Updates auflisten

 Listet alle installierten Updates auf, nicht nur wie im obigen Beispiel die Hotfixes. 

```
function Get-InstalledUpdate
{
    <#
     .Synopsis
         Gets updates installed on the system
     .Description
         Gets windows and microsoft updates installed on the system
     .Example
         Get-InstalledUpdate
     .Link
         https://github.com/StartAutomating/Patchy
    #>
    param()
    
    process {
        $srch = (New-Object -ComObject "Microsoft.Update.Session").CreateUpdateSearcher()
    	$count = $srch.GetTotalHistoryCount()
        for ($i = 0; $i -lt $count; $i++) {
            $update = $($srch.QueryHistory($i, 1))
            $title     = $update.Title
            $installed = $update.Date
            $kbnumber  = $title.split(' ') | Where-Object {$_ -match 'kb\d+'} | ForEach-Object {$_.Replace('(', '').Replace(')','').Replace(",","")}
            [PSCustomObject]@{
                Installd = $installed
                KBNumber = $kbnumber
                Title    = $title
            }
        }
        #Write-Output "Found $($count) installed updates on $($env:COMPUTERNAME)"
    }
}
$Updates  = Get-InstalledUpdate
$UpdCount = $Updates.Count
$Updates

"`n$UpdCount updates found on $env:COMPUTERNAME"
```