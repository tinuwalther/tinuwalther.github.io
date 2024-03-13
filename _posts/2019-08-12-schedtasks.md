---
layout: post
title:  "Task Scheduler"
author: Tinu
categories: "System-Engineering"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Task Scheduler](#task-scheduler)
  - [Create a Scheduled Task](#create-a-scheduled-task)
  - [Delete a Scheduled Task](#delete-a-scheduled-task)
  - [Task Actions](#task-actions)
  - [Task Information](#task-information)
- [Troubleshooting](#troubleshooting)
- [Task Scheduler Errors](#task-scheduler-errors)
- [See also](#see-also)

## Task Scheduler

### Create a Scheduled Task

````powershell
# Create the script
$ScriptFullname = 'C:\Admin\Scripts\Maintenace\RebootOnce.ps1'
if(-not(Test-Path $ScriptFullname)){$null = New-Item -Path $ScriptFullname -ItemType File -Force}

$Content = @"
Restart-Computer -Force
"@
$Content | Out-File -FilePath $ScriptFullname -Encoding utf8 -Force

# Create a new task action
$taskAction = @{
    Execute  = '%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe'
    Argument = "-NoProfile -NoLogo -NonInteractive -ExecutionPolicy Bypass -File $($ScriptFullname)"
}
$ScheduledTaskAction = New-ScheduledTaskAction @taskAction

# Create a new trigger
$taskTrigger = @{
    Once = $true
    At   = '2021/02/20 03:00:00'
}
$ScheduledTaskTrigger = New-ScheduledTaskTrigger @taskTrigger

# Create new task principal
$taskPrincipal = @{
    UserID    = 'NT AUTHORITY\SYSTEM'
    LogonType = 'ServiceAccount'
    RunLevel  = 'Highest'
}
$ScheduledTaskPrincipal = New-ScheduledTaskPrincipal @taskPrincipal

# Create new task settings
$taskSettings = @{
    ExecutionTimeLimit = (New-TimeSpan -Hours 1)
}
$ScheduledTaskSettingsSet = New-ScheduledTaskSettingsSet @taskSettings

# Register the new PowerShell scheduled task
$registerTask = @{
    TaskName    = "RestartOnce"
    Description = "Restart the computer one time"
    Action      = $ScheduledTaskAction
    Trigger     = $ScheduledTaskTrigger
    Principal   = $ScheduledTaskPrincipal
    TaskPath    = '\Maintenace'
    Settings    = $ScheduledTaskSettingsSet
}
Register-ScheduledTask @registerTask

Get-ScheduledTask -TaskName "RestartOnce" | Select *

Get-ScheduledTask "RestartOnce" | Get-ScheduledTaskInfo | Select *
````

### Delete a Scheduled Task

````powershell
# Delete the new PowerShell scheduled task
Unregister-ScheduledTask -TaskName "RestartOnce" -Confirm:$false
````

### Task Actions

Action: Start a program

Program/script: %SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe

Add arguments: -NoProfile -NoLogo -NonInteractive -ExecutionPolicy Bypass -File "C:\Temp\MyScript.ps1"

### Task Information

````powershell
Get-ScheduledTask | Where-Object TaskName -match "Verify Summary" | ForEach {

    $Task = $_
    $TaskInfo = Get-ScheduledTaskInfo -TaskName $Task.TaskName

    [PSCustomObject]@{
        TaskName           = $Task.TaskName
        TaskPath           = $Task.TaskPath
        Author             = $Task.Author
        Date               = $Task.Date
        Description        = $Task.Description
        State              = $Task.State
        LastRunTime        = $TaskInfo.LastRunTime
        NextRunTime        = $TaskInfo.NextRunTime
        LastTaskResult     = $TaskInfo.LastTaskResult
        NumberOfMissedRuns = $TaskInfo.NumberOfMissedRuns
    }

}

TaskName           : Verify Summary
TaskPath           : \
Author             : Domain\Asscount
Date               : 2019-08-12T09:04:50.0000171
Description        :
State              : Ready
LastRunTime        : 12.08.2019 09:08:08
NextRunTime        : 19.08.2019 08:04:04
LastTaskResult     : 0
NumberOfMissedRuns : 0
````

## Troubleshooting

Start the PowerShell-Script with a CMD-Script, to verify that the script can be run with the configured Account in the ScheduledTask.

````batch
@echo off
rem ---------------------------------------------------------------------------- *
rem Description: Start PS-Script
rem Author     : Martin Walther
rem ---------------------------------------------------------------------------- *

rem Path: %~dp0 Script: %~n0
set log=%~dp0%~n0.log
set script=%~dp0%~n0.ps1
echo %log%
echo %script%

echo Start %script% %date%%time% > %log%
%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe -NoProfile -NoLogo -NonInteractive -ExecutionPolicy Bypass %script% >> %log%
echo End %script% %date%%time% >> %log%
````

In the Logfile, you can find any Errors- or Output from the PowerShell-Script.

## Task Scheduler Errors

Error | Problem | Solution
-|-|-
0x1 | Path to the program does not exists | Correct the Path to the program e.g. change powershell.exe to C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
0xFFFD0000 | Path to the script does not exists | Correct the Path to the script

## See also

[Task Scheduler Error and Success Constants](https://docs.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-error-and-success-constants) on Microsoft Docs.

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]
