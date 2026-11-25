---
title: CD-Rom ändern
date: '2016-06-27T18:50:02+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Devices
wordpress_id: 1494
layout: post
permalink: /wiki/cd-rom-aendern/
render_with_liquid: false
---

CD-Rom auf anderen Laufwerksbuchstaben ändern.

```
function Get-CDRomLetter{
    $function = $($MyInvocation.MyCommand.Name)
    $ret = $null
    try
    {
        $ret = (gwmi Win32_cdromdrive).drive
    }
    catch [Exception]
    {
        write-host "$($function): $($_.Exception.Message)" -ForegroundColor Red
        $error.clear()
    }
    return $ret
}

function Set-CDRomLetter{
    param(
        [Parameter(Mandatory=$true)][String]$newdrive=''
    )
    $function = $($MyInvocation.MyCommand.Name)
    $ret = $null
    try
    {
        (gwmi Win32_cdromdrive).drive | %{
            #Lists the mounted volume name for the specified directory.
            $currentdrive = mountvol $_ /l
            #Removes the volume mount point from the specified directory.
            mountvol $_ /d
            $currentdrive = $currentdrive.Trim()
            mountvol $newdrive $currentdrive
        }
    }
    catch [Exception]
    {
        write-host "$($function): $($_.Exception.Message)" -ForegroundColor Red
        $error.clear()
    }
}

if (Get-CDRomLetter -notlike 'Z:')
{
    Set-CDRomLetter -newdrive 'Z:'
}
```