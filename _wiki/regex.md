---
title: Traceroute in Object umwandeln
date: '2017-02-01T08:28:44+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- PSObject
- Regex
wordpress_id: 1881
layout: post
permalink: /wiki/regex/
render_with_liquid: false
---

Routenverfolgung zerlegen und in ein Object ausgeben. Mein Provider hat Angst vor einem "?raceroute" - ergo ?racert heisst richtig wie?

```
function Get-RouteResult
{
    param($Name)
    $routeregex = '(?<Address>(?<=Tracing route to )(.*)(?=over))'
    $TraceRouteTo  = $Name -match $routeregex
    $ipadrregex    = ‘\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b’
    $IPAddresses   = $Name | select-string -Pattern $ipadrregex -AllMatches | % {$_.Matches.Value} -ErrorAction SilentlyContinue
    if([string]::IsNullOrEmpty($IPAddresses))
    {
        $TraceRouteTo  = '{}'
        $TargetAddress = '{}'
        $FinishAddress = '{}'
    }
    else
    {
        $TargetAddress = $IPAddresses[0]
        $FinishAddress = $IPAddresses[$IPAddresses.Count-1]
    }
    $TraceResult   = if ($TargetAddress -eq $FinishAddress){$true}else{$false}

    $obj = New-Object PSObject
    $obj | Add-Member NoteProperty 'TraceRouteTo'   $TraceRouteTo
    $obj | Add-Member NoteProperty 'TargetAddress'  $TargetAddress
    $obj | Add-Member NoteProperty 'FinishAddress'  $FinishAddress
    $obj | Add-Member NoteProperty 'IPAddresses'    $IPAddresses
    $obj | Add-Member NoteProperty 'TraceResult'    $TraceResult
    return $obj
}

Get-RouteResult -Name (?racert.exe -h 15 gmx.net)
```