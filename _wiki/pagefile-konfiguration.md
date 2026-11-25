---
title: Pagefile Konfiguration
date: '2017-07-05T21:41:34+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Memorydump
- Pagefile
- Windows Server
wordpress_id: 2241
layout: post
permalink: /wiki/pagefile-konfiguration/
render_with_liquid: false
---

Bei einer Default-Installation eines Windows OS ist das Pagefile immer auf AutomaticManagedPagefile eingestellt. Diese Konfiguration führt früher oder später zu einem Diskspace Problem auf der System Disk, da das Pagefile sich so viel Platz nimmt wie es kann. Mit folgendem Script kann die Pagefile Konfiguration, den letzten Memorydump, die Eventlogeinträge von den letzten paar System Crashes sowie der Diskspace aller Disks ausgelesen werden. P.S.: Ein System Crash kann den Memorydump nicht auf eine Dynamic Disk schreiben!

```
<#
 Analyze Pagefiles and MemoryDump Settings
 https://blogs.msdn.microsoft.com/ntdebugging/2010/04/02/how-to-use-the-dedicateddumpfile-registry-value-to-overcome-space-limitations-on-the-system-drive-when-capturing-a-system-memory-dump/ 
#>

function CheckPagefileSettings{
    <# Check PageFileManagement #>
    [cmdletbinding()]
    Param()
    $function = $($MyInvocation.MyCommand.Name)
    write-verbose "Running $($function) ..."
    try{
        $PagefileOnCDrive  = $false
        $Hash              = [ordered]@{}
        $Hash.OverAllState = $true
        $Hash.ComputerName = $($env:COMPUTERNAME)

        #Automatically manage pagefile
        $SystemInfo = Get-WmiObject -Class Win32_ComputerSystem -EnableAllPrivileges
        $Hash.AutomaticManagedPagefile = $SystemInfo.AutomaticManagedPagefile
        if($Hash.AutomaticManagedPagefile)
        {
            $Hash.OverAllState = $false
        }

        #PagefileSettings
        $PagefileSettings  = Get-CimInstance -ClassName Win32_PageFileSetting
        $Hash.PageFilePath = $($PagefileSettings.Name)
        foreach($item in $Hash.PageFilePath)
        {
            if($item -match 'c:')
            {
                $PagefileOnCDrive = $true
            }
        }
        if([String]::IsNullOrEmpty($PagefileSettings))
        {
            $Hash.OverAllState = $false
            $Hash.PageFileInitialSize = 'None'
            $Hash.PageFileMaximumSize = 'None'
        }
        else
        {
            $Hash.PageFileInitialSize = $($PagefileSettings.InitialSize)
            $Hash.PageFileMaximumSize = $($PagefileSettings.MaximumSize)
        }

        #DedicatedDumpFile
        $DedicatedDumpFile = Get-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\CrashControl' -ErrorAction SilentlyContinue
        $Hash.DefaultDumpFilePath   = $($DedicatedDumpFile.DumpFile)
        $Hash.DedicatedDumpFilePath = $($DedicatedDumpFile.DedicatedDumpFile)
        $Hash.DedicatedDumpFileSize = $($DedicatedDumpFile.DumpFileSize)

        #MemoryDumpSettings
        $DebugFilePath = Get-WmiObject Win32_OSRecoveryConfiguration -EnableAllPrivileges
        #$Hash.DebugFilePath              = $($DebugFilePath.DebugFilePath)
        $Hash.ExpandedDebugFilePath      = $($DebugFilePath.ExpandedDebugFilePath)
        if(Test-Path $Hash.ExpandedDebugFilePath)
        {
            $Hash.DumpLastWriteTime = (Get-Item $($Hash.ExpandedDebugFilePath)).LastWriteTime
        }
        else
        {
            $Hash.DumpLastWriteTime = 'None'
        }
        #$Hash.MiniDumpDirectory          = $($DebugFilePath.MiniDumpDirectory)
        $Hash.ExpandedMiniDumpDirectory  = $($DebugFilePath.ExpandedMiniDumpDirectory)
        $Hash.OverwriteExistingDebugFile = $($DebugFilePath.OverwriteExistingDebugFile)
        $Hash.KernelDumpOnly             = $($DebugFilePath.KernelDumpOnly)
        $Hash.SendAdminAlert             = $($DebugFilePath.SendAdminAlert)
        $Hash.WriteDebugInfo             = $($DebugFilePath.WriteDebugInfo)
        $Hash.WriteToSystemLog           = $($DebugFilePath.WriteToSystemLog)
        $Hash.AutoReboot                 = $($DebugFilePath.AutoReboot)
        
        #DiskInfos
        $DiskTypes = Get-WmiObject Win32_DiskPartition -filter "Type='Logical Disk Manager'"
        foreach($Disk in $DiskTypes)
        {
            if($PagefileOnCDrive -eq $false)
            {
                $Hash.OverAllState  = $false
                $Hash.DynamicDiskAt = "$($DiskTypes.GetRelated('Win32_LogicalDisk').DeviceID), $($Disk.Name)"
            }
        }
        $Obj = New-Object psobject -Property $Hash
        return $Obj
    }
    catch [Exception]{
          "ERROR: $($_.Exception.Message)" | out-string
          $error.clear()
    }
}

function GetDiskSpace{
    [cmdletbinding()]
    Param()
    $function = $($MyInvocation.MyCommand.Name)
    write-verbose "Running $($function) ..."
    # DeviceID, MediaType, TotalSize, FreeSize, Percent
    try{
	    $ret  = @()
        $Hash = [ordered]@{}
	    Get-WmiObject Win32_logicaldisk | where {$_.MediaType -eq 12} | %{
		    $size = $([math]::round($_.size/1gb))
		    $free = $([math]::round($_.freespace/1gb))
		    $percent = $([math]::round(($free*100) / ($size)))

		    $Hash.DeviceID         = $_.DeviceID
		    $Hash.TotalSizeGB      = $size
		    $Hash.FreeSpaceGB      = $free
		    $Hash.'FreeSpace%' = $percent

            $obj = New-Object psobject -Property $Hash
		    $ret += $obj
	    }
        return $ret
    }
    catch [Exception]{
          "ERROR: $($_.Exception.Message)" | out-string
          $error.clear()
    }
}

cls
CheckPagefileSettings
GetDiskSpace | Format-Table -AutoSize
Get-WinEvent -FilterHashtable @{Logname='System';Id=46} -MaxEvents 2 -ErrorAction SilentlyContinue | Select TimeCreated,Message | Format-Table -AutoSize
Get-WinEvent -FilterHashtable @{Logname='System';Id=6008} -MaxEvents 4 -ErrorAction SilentlyContinue | Select TimeCreated,Message | Format-Table -AutoSize
```

 Als Resultat wird ein Report ausgegeben: 

```
OverAllState               : False
ComputerName               : WIN-U6TO22C231T
AutomaticManagedPagefile   : False
PageFilePath               : d:\pagefile.sys
PageFileInitialSize        : 2048
PageFileMaximumSize        : 2048
DefaultDumpFilePath        : C:\Windows\MEMORY.DMP
DedicatedDumpFilePath      : 
DedicatedDumpFileSize      : 
ExpandedDebugFilePath      : C:\Windows\MEMORY.DMP
DumpLastWriteTime          : None
ExpandedMiniDumpDirectory  : C:\Windows\Minidump
OverwriteExistingDebugFile : True
KernelDumpOnly             : False
SendAdminAlert             : False
WriteDebugInfo             : True
WriteToSystemLog           : True
AutoReboot                 : True
DynamicDiskAt              : D:, Disk #1, Partition #0

DeviceID TotalSizeGB FreeSpaceGB FreeSpace%
-------- ----------- ----------- ----------
C:                25          17         68
E:                 5           4         80

TimeCreated         Message                          
-----------         -------                          
03.07.2017 22:39:14 Crash dump initialization failed!
03.07.2017 22:39:14 Crash dump initialization failed!

TimeCreated         Message                                                             
-----------         -------                                                             
05.07.2017 20:56:27 The previous system shutdown at 20:54:39 on ‎05.‎07.‎2017 was une...
03.07.2017 22:43:13 The previous system shutdown at 22:42:27 on ‎03.‎07.‎2017 was une...
03.07.2017 22:39:26 The previous system shutdown at 22:38:39 on ‎03.‎07.‎2017 was une...
03.07.2017 22:35:39 The previous system shutdown at 22:34:17 on ‎03.‎07.‎2017 was une...
```