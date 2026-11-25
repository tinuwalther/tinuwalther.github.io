---
title: IP4 RouteTable Class
date: '2018-02-26T21:32:31+01:00'
author: Tinu
excerpt: IP4 Route Table exportieren, löschen und importieren mit einer PowerShell
  Class.
categories:
- PowerShell
tags:
- Class
image: /assets/wiki/powershell-1.png
wordpress_id: 2456
layout: post
permalink: /wiki/ip4-routetable-class/
render_with_liquid: false
---

## Routing Tabelle

IP4 Route Table exportieren, löschen und importieren mit einer PowerShell Class. 

```
<#
 .SYNOPSIS
  IP4 Route Table

 .DESCRIPTION
  List | Export | Import | Delete IP4 Route Table entries

 .PARAMETER
  Inputfile Fullpath to the inputfile

 .NOTES
  Author: Martin Walther
  Date created: 26.02.2018
  Version: 1.0.0.00000

 .EXAMPLE
  (New-Object PSIpRouteTable).RoutingEntries
  [PSIpRouteTable]::new().RoutingEntries

  IPv4 Active Routes:
  [PSIpRouteTable]::GetIP4RouteTable() 
  [PSIpRouteTable]::ExportIP4RouteTable('C:\Admin\logs\IP4RouteTable.json') 
  [PSIpRouteTable]::ImportIP4RouteTable('C:\Admin\logs\IP4RouteTable.json')

  IPv4 Persistent Routes: 
  [PSIpRouteTable]::GetIP4PersistedRouteTable() 
  [PSIpRouteTable]::ExportIP4PersistedRouteTable('C:\Admin\logs\IP4PersistedRouteTable.json') 
  [PSIpRouteTable]::ImportIP4PersistedRouteTable('C:\Admin\logs\IP4PersistedRouteTable.json') 

  [PSIpRouteTable]::DeleteIP4RouteTable('C:\Admin\logs\IP4PersistedRouteTable.json') 
#>

Class PSIpRouteTable {

    [object]$RoutingEntries         = $null

    PSIpRouteTable(){
        $this.RoutingEntries        += [PSIpRouteTable]::GetIP4RouteTable()
        $this.RoutingEntries        += [PSIpRouteTable]::GetIP4PersistedRouteTable()
    }

    #region IPv4 Active Routes
    [object]static GetIP4RouteTable(){
        $retarray = @()
        $objWin32 = Get-WmiObject Win32_IP4RouteTable
        foreach($item in $objWin32){
            $rethash  = @{}
            #$rethash.Caption      = $item.Caption
            #$rethash.Description  = $item.Description
            $rethash.Destination  = $item.Destination
            $rethash.Mask         = $item.Mask
            $rethash.Metric1      = $item.Metric1
            $rethash.Name         = $item.Name
            $rethash.NextHop      = $item.NextHop
            $rethash.Type         = 'Active'
            $rethash.IPVersion    = 4
            $retarray += $rethash
        }
        return $retarray
    }

    [object]static ExportIP4RouteTable($ToJsonFile){
        $retarray = @()
        $objWin32 = Get-WmiObject Win32_IP4RouteTable
        foreach($item in $objWin32){
            $rethash  = @{}
            #$rethash.Caption      = $item.Caption
            #$rethash.Description  = $item.Description
            $rethash.Destination  = $item.Destination
            $rethash.Mask         = $item.Mask
            $rethash.Metric1      = $item.Metric1
            $rethash.Name         = $item.Name
            $rethash.NextHop      = $item.NextHop
            $retarray += $rethash
        }
        $retarray | ConvertTo-Json -Compress | Out-File $ToJsonFile -Force
        if(Test-Path -Path $ToJsonFile){
            return Get-Item $ToJsonFile
        }
        else{
            return $null
        }
    }
    [object]static ImportIP4RouteTable($ToJsonFile){
        $routeret = $null
        $ret = $false
        if(Test-Path -Path $ToJsonFile){
            $objjson = Get-Content -Path $ToJsonFile -Raw | ConvertFrom-Json
            foreach($item in $objjson){
                if($item.Name -ne '0.0.0.0'){
                    $routeret = route.exe ADD -p $($item.Name) MASK $($item.Mask) $($item.NextHop) METRIC $($item.Metric1)
                    Write-Host "route ADD $($item.Name) MASK $($item.Mask) $($item.NextHop) METRIC $($item.Metric1) -- Status $($routeret)"
                    if($routeret.trim() -eq 'OK!'){
                        $ret = $true
                    }
                }
            }
        }
        return $ret
    }
    #endregion

    #region IPv4 Persistent Routes
    [object]static GetIP4PersistedRouteTable(){
        $retarray = @()
        $objWin32 = Get-WmiObject Win32_IP4PersistedRouteTable
        foreach($item in $objWin32){
            $rethash  = @{}
            #$rethash.Caption      = $item.Caption
            #$rethash.Description  = $item.Description
            $rethash.Destination  = $item.Destination
            $rethash.Mask         = $item.Mask
            $rethash.Metric1      = $item.Metric1
            $rethash.Name         = $item.Name
            $rethash.NextHop      = $item.NextHop
            $rethash.Type         = 'Persistent'
            $rethash.IPVersion    = 4
            $retarray += $rethash
        }
        return $retarray
    }

    [object]static ExportIP4PersistedRouteTable($ToJsonFile){
        $retarray = @()
        $objWin32 = Get-WmiObject Win32_IP4PersistedRouteTable
        foreach($item in $objWin32){
            $rethash  = @{}
            #$rethash.Caption      = $item.Caption
            #$rethash.Description  = $item.Description
            $rethash.Destination  = $item.Destination
            $rethash.Mask         = $item.Mask
            $rethash.Metric1      = $item.Metric1
            $rethash.Name         = $item.Name
            $rethash.NextHop      = $item.NextHop
            $retarray += $rethash
        }
        $retarray | ConvertTo-Json -Compress | Out-File $ToJsonFile -Force
        if(Test-Path -Path $ToJsonFile){
            return Get-Item $ToJsonFile
        }
        else{
            return $null
        }
    }

    [object]static ImportIP4PersistedRouteTable($ToJsonFile){
        $routeret = $null
        $ret = $false
        if(Test-Path -Path $ToJsonFile){
            $objjson = Get-Content -Path $ToJsonFile -Raw | ConvertFrom-Json
            foreach($item in $objjson){
                if($item.Name -ne '0.0.0.0'){
                    $routeret = route.exe ADD -p $($item.Name) MASK $($item.Mask) $($item.NextHop) METRIC $($item.Metric1)
                    Write-Host "route ADD -p $($item.Name) MASK $($item.Mask) $($item.NextHop) METRIC $($item.Metric1) -- Status $($routeret)"
                    if($routeret.trim() -eq 'OK!'){
                        $ret = $true
                    }
                }
            }
        }
        return $ret
    }
    #endregion

    #region Global
    [object]static DeleteIP4RouteTable($ToJsonFile){
        $routeret = $null
        $ret = $false
        if(Test-Path -Path $ToJsonFile){
            $objjson = Get-Content -Path $ToJsonFile -Raw | ConvertFrom-Json
            foreach($item in $objjson){
                if($item.Name -ne '0.0.0.0'){
                    $routeret = route.exe DELETE $($item.Name)
                    Write-Host "route DELETE $($item.Name) -- Status $($routeret)"
                    if($routeret.trim() -eq 'OK!'){
                        $ret = $true
                    }
                }
            }
        }
        return $ret
    }
    #endregion
}
```