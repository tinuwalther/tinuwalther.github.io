---
title: Pagefile
date: '2015-07-09T13:28:20+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Memory
- Pagefile
wordpress_id: 1300
layout: post
permalink: /wiki/pagefile/
render_with_liquid: false
---

## Virtual Memory abfragen

 Die Grössenangaben sind alle in Megabytes zu verstehen. 

```
Get-WmiObject -Class Win32_PageFileUsage | `
Select Name,AllocatedBaseSize,CurrentUsage,Peakusage,TempPageFile | Format-List
```

 Oder formatiert: 

```
Get-WmiObject -Class Win32_PageFileUsage | `
Select @{Name="Pagefile";Expression="Name"},`
@{Name="Allocated(MB)";Expression="AllocatedBaseSize"},`
@{Name="Current(MB)";Expression="CurrentUsage"},`
@{Name="Peak(MB)";Expression="Peakusage"},TempPageFile | ft -AutoSize
```

## Virtual Memory verwalten

 If you have **more than one physical disk**, moving the page file to a fast drive that doesn’t contain your Windows system files is a good idea. If you are **short of hard disk space**, you might consider setting a **smaller initial page file size**. Monitor **peak usage** levels over time; if the peak is well **below the current page file size**, you can consider **reducing the initial size** to save disk space. 

### Virtual Memory GUI starten

 Start, Run, systempropertiesadvanced, Enter 

## Automatically Manage Paging File Size

 Windows might **increase** or even **decrease** the size of the page file. All this happens without you’re knowing as long as you leave the **Automatically Manage Paging File Size For All Drives** option selected. To **decrease** the size of the page file, a reboot of the computer is required. 

### Manually Manage Paging File Size with PowerShell

 The **minimum size** on a Windows 8 or Windows Server 2012 system is equal to the amount of physical RAM plus 300 MB (for crash dump). The default **maximum size** is three times the amount of RAM or 4 GB, whichever is larger. 

```
$SystemInfo = gwmi -Class Win32_ComputerSystem -EnableAllPrivileges
$SystemInfo.AutomaticManagedPageFile = $false
$SystemInfo.Put() | Out-Null

gwmi -Class Win32_PageFileUsage | `
Select Name,AllocatedBaseSize,CurrentUsage,Peakusage

[int]$memory = gcim -class "cim_physicalmemory" | % {($_.Capacity)/1mb}
Write-Host "Physical Memory is $($memory) MB"
$currentpagefile = gwmi -Class Win32_PageFileSetting
if(($currentpagefile.InitialSize) -lt $memory){
   $pagefilepath = (gwmi -Class Win32_PageFileSetting).name
   $pagefile = gwmi -Query "Select * From Win32_PageFileSetting"
   $pagefile.InitialSize = (($memory)+300)
   $pagefile.MaximumSize = (($memory)*1.5)
   $pagefile.Put() | Out-Null
   gwmi -Class Win32_PageFileSetting | select Name,InitialSize,MaximumSize | fl
   Start-Sleep -Seconds 20
   Restart-Computer
}
```

 Falls ein Error auftritt, Server booten und Script erneut durchführen. Die englischen Abschnitte stammen aus den [Best Practices for Optimizing the Virtual Memory Configuration](https://technet.microsoft.com/en-us/magazine/ff382717.aspx) aus dem TechNet Magazine. Weitere Information zum Thema Virtual Memory siehe [Microsoft Support KB 2860880](https://support.microsoft.com/en-us/kb/2860880).