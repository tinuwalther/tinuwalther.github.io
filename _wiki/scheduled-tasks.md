---
title: Scheduled Tasks
date: '2015-05-27T16:06:36+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Task Scheduler
wordpress_id: 1180
layout: post
permalink: /wiki/scheduled-tasks/
render_with_liquid: false
---

## Scheduled Task abfragen

```
Get-ScheduledTask -TaskName 'My Task' | Format-List *
```

Mit **schtasks.exe** können z. B. alle Tasks eines Servers abgefragt werden. Meistens möchte man aber nur das Resultat eines einzigen Tasks wissen. Das geht über PowerShell folgenderweise:

```
schtasks /query /s $server | select-string -pattern $taskname
```

Zurückgegeben wird der TaskName, Next Run Time und der Status.

## Task erstellen

```
$TaskName        = 'My Task'<br></br>$TaskDescription = 'Task created with PowerShell Commands'<br></br>$TaskToExecute   = "powershell.exe"<br></br>$TaskArguments   = "-executionpolicy bypass & {C:\Admin\Scripts\swisscom-wupdate\ALL-OPR-RunWindowsUpdate.ps1 -force}"<br></br>$SystemAccount   = "S-1-5-18"<br></br><br></br>$TaskAction      = New-ScheduledTaskAction    -Execute $TaskToExecute -Argument $TaskArguments<br></br>$TaskTrigger     = New-ScheduledTaskTrigger   -Daily -At (Get-Date "08:00")<br></br>$TaskRunAs       = New-ScheduledTaskPrincipal -UserId $SystemAccount -LogonType ServiceAccount<br></br>$TaskSettings    = New-ScheduledTaskSettingsSet<br></br>$TaskDefinition  = New-ScheduledTask -Action $TaskAction -Description $TaskDescription -Principal $TaskRunAs -Trigger $TaskTrigger -Settings $TaskSettings<br></br>Register-ScheduledTask -TaskName $TaskName -InputObject $TaskDefinition<br></br><br></br>Get-ScheduledTask     -TaskName $TaskName | Format-List *<br></br>Get-ScheduledTaskInfo -TaskName $TaskName | Format-List * 
```

## Task löschen

```
$TaskName = 'My Task'<br></br>Unregister-ScheduledTask -TaskName $TaskName
```

## PowerShell Script mit Task Scheduler starten

TaskToRun

```
powershell.exe -executionpolicy bypass & {Pfad zum Script}<br></br>powershell.exe -executionpolicy bypass -command {Get-Service -Name mpssvc}<br></br>powershell.exe -executionpolicy bypass -file install.ps1<br></br>
```