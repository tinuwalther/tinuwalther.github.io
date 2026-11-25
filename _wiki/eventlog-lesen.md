---
title: Eventlog lesen
date: '2015-07-08T09:28:48+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Eventlog
- Hashtable
- PSObject
wordpress_id: 1287
layout: post
permalink: /wiki/eventlog-lesen/
render_with_liquid: false
---

## Eventlogs mit PowerShell 5.0 auslesen

### Eventlog Einträge zwischen zwei Datums-/Zeitangaben auslesen

 Mit folgendem Command kann nach Events innerhalb einer definierten Zeitspanne in den Eventlogs Application und System gesucht werden: 

```
$LogName             = 'Application', 'System'
[DateTime]$StartTime = '07.02.2015 14:30:00'
[DateTime]$EndTime   = '07.02.2015 15:05:00'
Get-WinEvent -FilterHashtable @{
   Logname=$LogName
   StartTime=$StartTime
   EndTime=$EndTime
} | ft -Property LogName,TimeCreated,Id,LevelDisplayName,Message -Auto
```

### Unexpected Shutdown Einträge suchen

 Die letzten 20 unecpected Shutdown Einträge auflisten: 

```
$ID      = 6008
$LogName = 'System'
Get-WinEvent -FilterHashtable @{
   Logname=$LogName
   Id=$ID
} -MaxEvents 20 | ft -Property LogName,TimeCreated,Id,LevelDisplayName,Message -Auto
```

### Application Error und -Popup Einträge suchen

 Aus den letzten 20 Events die Application Error- und Application Popup Einträge auflisten: 

```
$LogName      = 'Application','System'
$ProviderName = 'Application Error','Application Popup'
Get-WinEvent -FilterHashtable @{
   Logname=$LogName
   ProviderName=$ProviderName
} -MaxEvents 20 | ft -Property LogName,TimeCreated,Id,LevelDisplayName,Message -Auto
```

### Einträge nach Level (Critical, Error, Warning) suchen

 Die letzten 20 Einträge mit bestimmtem Level auflisten: 

```
$LogName = 'Application', 'System'
$Level = 1,2,3
# 0 - LogAlways
# 1 - Critical
# 2 - Error
# 3 - Warning
# 4 - Informational
# 5 - Verbose
Get-WinEvent -FilterHashtable @{
   Logname=$LogName
   Level=$Level
} -MaxEvents 20 | ft -Property LogName,TimeCreated,Id,LevelDisplayName,Message -Auto
```

### Einträge vor dem letzten unexpected shutdown suchen

```
cls
$ID      = 6008
$LogName = 'System'
$event   = Get-WinEvent -FilterHashtable @{Logname=$LogName;Id=$ID} -MaxEvents 1
Write-Host "$($event.TimeCreated) $($event.Message)"
$Level = 1,2,3,4
[DateTime]$StartTime = ($event.TimeCreated).AddMinutes(-60)
[DateTime]$EndTime = ($event.TimeCreated).AddMinutes(10)
Get-WinEvent -FilterHashtable @{
 Logname=$LogName
 Level=$Level
 StartTime=$StartTime
 EndTime=$EndTime
} | ft -Property LogName,TimeCreated,Id,LevelDisplayName,Message -Auto
```

## Eventlogs mit PowerShell 2.0/3.0 auslesen

### Eventlog Einträge zwischen zwei Datums-/Zeitangaben auslesen

```
[DateTime]$after  = '07.02.2015 14:50:00'
[DateTime]$before = '07.02.2015 15:05:00'
$Logname          = 'Application'
Get-EventLog $Logname -After $after -Before $before | `
Select TimeGenerated,EventID,EntryType,Message | ft -auto
```

### Unexpected Shutdown Einträge suchen

```
$EventId          = 6008
$Logname          = 'System'
[DateTime]$after  = '07.02.2015 14:00:00'
[DateTime]$before = '07.02.2015 15:05:00'
Get-EventLog $Logname -After $after -Before $before | where {$_.eventID -eq 6008} | `
Select TimeGenerated,EventID,EntryType,Message | ft -auto
```

### Shutdown History erstellen

 Shutdown- bzw. Restart History innerhalb des letzten Monats erstellen: 

```
cls
$ret = @()
$Logname          = 'System'
[DateTime]$now    = Get-Date
[DateTime]$after  = $now.AddMonths(-1)
[DateTime]$before = $now
"Systemrestarts between $($after) and $($before):"
Get-EventLog $Logname -After $after -Before $before | where {
    $_.eventID -eq 1074 -or # Explorer.EXE has initiated the restart of computer
    $_.eventID -eq 6009 -or # The user restarted or shut down the computer by clicking Start or pressing CTRL+ALT+DELETE
    $_.eventID -eq 6008     # The previous system shutdown at <time> on <date> was unexpected.
} | % {
    $obj = New-Object PSObject
    Add-Member -InputObject $obj -MemberType NoteProperty -Name TimeGenerated -Value $_.TimeGenerated
    Add-Member -InputObject $obj -MemberType NoteProperty -Name EventID -Value $_.EventID
    if($_.EventID -eq 6009){
        $message = "Restart of the the computer..."
    }
    else{
        $i = $($_.Message).Split(":").getupperbound(0) -1
        $message = "$($($_.Message).Split(":")[$i].Trim())"
    }
    Add-Member -InputObject $obj -MemberType NoteProperty -Name Message -Value $message
    $ret += $obj
}
$ret | sort TimeGenerated -Descending | ft -AutoSize
```

### Application Error Einträge suchen

```
$Source  = 'Application Error'
$Logname = 'Application'
$EventId = 1000
Get-EventLog $Logname  | where {$_.eventID -eq $EventId} | `
Select TimeGenerated,EventID,EntryType,Message | ft -auto
```

### Securitylog

 Logon und Logoff Sessions in einem gewissen Zeitraum auflisten. 

```
$Logname          = 'Security'
[DateTime]$now    = Get-Date
[DateTime]$after  = $now.AddMonths(-1)
[DateTime]$before = $now
$events = Get-EventLog -LogName $Logname -InstanceId 4624,4625,4634 -After $after -Before $before | `
Select TimeGenerated,EventID,EntryType,Message
```