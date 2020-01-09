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
  - [Task Actions](#task-actions)
  - [Task Information](#task-information)
- [Troubleshooting](#troubleshooting)
- [Task Scheduler Errors](#task-scheduler-errors)
- [See also](#see-also)

# Task Scheduler

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