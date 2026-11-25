---
title: Collection to String
date: '2016-08-02T17:07:18+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- String
wordpress_id: 1526
layout: post
permalink: /wiki/collection-to-string/
render_with_liquid: false
---

Immer wenn eine Collection in einen String umgewandelt werden soll...

```
function Convert-CollectionToString
{
    <# Convert System.Collections.Specialized.StringCollection to String #>
    param(
        [Parameter(Mandatory = $true)] $col
    )
    $function = $($MyInvocation.MyCommand.Name)
    [String] $ret = $null
    try
    {
        if($psdebug)
        {
            Write-Verbose -Message "Running $($function) ..." -Verbose
        }
        if($col -is [System.Collections.Specialized.StringCollection])
        {
            foreach($item in $col)
            {
                $ret = "$($ret) $($item)"
            }
        }
        else
        {
            $ret = $col
        }
    }
    catch [Exception]
    {
        if($psdebug)
        {
            Write-Error -Message "$($function): $($_.Exception.Message)" ...
        }
        else
        {
           "$(get-date -f 'yyyy-MM-dd HH:mm:ss') - [   ERROR   ] $($function): $($_.Exception.Message)" | Out-File "$($Global:Logfile)" -Encoding ascii -Append

        }
        $error.clear()
    }
    if($psdebug)
    {
        Write-Verbose -Message "$($function): Return $($ret)" -Verbose
    }
    return $ret
}
```