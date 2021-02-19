---
layout: post
title:  "Task Scheduler"
author: Tinu
categories: "System-Engineering"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Task Scheduler](#task-scheduler)
  - [Create a Scheduled Task](#create-a-scheduled-task)
- [Create the script](#create-the-script)
- [Create a new task action](#create-a-new-task-action)
- [Create a new trigger (Daily at 3 AM -> 02:00 local time)](#create-a-new-trigger-daily-at-3-am---0200-local-time)
- [Register the new PowerShell scheduled task](#register-the-new-powershell-scheduled-task)
- [Register the scheduled task](#register-the-scheduled-task)
  - [Task Actions](#task-actions)
  - [Task Information](#task-information)
- [Troubleshooting](#troubleshooting)
- [Task Scheduler Errors](#task-scheduler-errors)
- [See also](#see-also)

# Task Scheduler

## Create a Scheduled Task

````powershell
# Create the script
$Content = @"
Restart-Computer -WhatIf
"@
Set-Content -Path 'D:\Temp\Restart.ps1' -Value $Content

# Create a new task action
$taskAction = @{
    Execute  = '%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe'
    Argument = '-NoProfile -NoLogo -NonInteractive -ExecutionPolicy Bypass -File "D:\Temp\Restart.ps1"'
}
$ScheduledTaskAction = New-ScheduledTaskAction @taskAction

# Create a new trigger (Daily at 3 AM -> 02:00 local time)
$taskTrigger = @{
    Daily = $true
    At    = '3AM'
}
$ScheduledTaskTrigger = New-ScheduledTaskTrigger @taskTrigger

# Register the new PowerShell scheduled task
$ScheduledTask = @{
    TaskName    = "Restart computer"
    Description = "Restart the computer daily"
    Action      = $ScheduledTaskAction
    Trigger     = $ScheduledTaskTrigger
    User        = 'SYSTEM'
}

# Register the scheduled task
Register-ScheduledTask @ScheduledTask

Get-ScheduledTaskInfo -TaskName "Restart computer"
````

## Task Actions

Action: Start a program

Program/script: %SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe

Add arguments: -NoProfile -NoLogo -NonInteractive -ExecutionPolicy Bypass -File "C:\Temp\MyScript.ps1"

## Task Information

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

# Troubleshooting

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
%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass %script% >> %log%
echo End %script% %date%%time% >> %log%
````

In the Logfile, you can find any Errors- or Output from the PowerShell-Script.

# Task Scheduler Errors

Error | Problem | Solution
-|-|-
0xFFFD0000 | Path to the script does not exists | Correct the Path to the script

# See also

[Task Scheduler Error and Success Constants](https://docs.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-error-and-success-constants) on Microsoft Docs.

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]