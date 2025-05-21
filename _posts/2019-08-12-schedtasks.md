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
  - [Create a PowerShell Script](#create-a-powershell-script)
  - [Create a new task action](#create-a-new-task-action)
  - [Create a new trigger](#create-a-new-trigger)
  - [Create new task principal](#create-new-task-principal)
  - [Create new task settings](#create-new-task-settings)
  - [Register the Scheduled Task](#register-the-scheduled-task)
  - [Register a Scheduled Task as User](#register-a-scheduled-task-as-user)
  - [Delete a Scheduled Task](#delete-a-scheduled-task)
  - [Task Actions](#task-actions)
  - [Task Information](#task-information)
- [Troubleshooting](#troubleshooting)
- [Task Scheduler Errors](#task-scheduler-errors)
- [See also](#see-also)

## Task Scheduler

### Create a PowerShell Script

````powershell
# Create the script
$ScriptFullname = 'C:\Temp\Maintenace\RebootOnce.ps1'
if(-not(Test-Path $ScriptFullname)){$null = New-Item -Path $ScriptFullname -ItemType File -Force}

$Content = @"
Restart-Computer -WhatIf | Set-Content 'C:\Temp\Maintenace\RebootOnce.log'
"@
$Content | Out-File -FilePath $ScriptFullname -Encoding utf8 -Force
````

### Create a new task action

The Task Action is the action or program, that schould be executed.

````powershell
$taskAction = @{
    Execute  = '%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe'
    Argument = "-NoProfile -NoLogo -NonInteractive -ExecutionPolicy Bypass -File $($ScriptFullname)"
}
$ScheduledTaskAction = New-ScheduledTaskAction @taskAction
````

### Create a new trigger

The Trigger define the runtime of the action.

Parameters:

- AtLogOn – Runs the task when a user logs on
- AtStartup – When the system is started
- At – Used with Once, Daily, or Weekly. Defines the specific time to run the task
- Daily – Runs every day. Define the days with DaysOfWeek
- DaysInterval – Run every x days
- DaysOfWeek – This can be used with Daily or Weekly. Defines which days to run the task
- Weekly – Runs the tasks every week
- WeeklyInterval – Determines the interval between the weeks.

````powershell
$taskTrigger = @{
    Once = $true
    At   = '2021/02/20 03:00:00'
}
$ScheduledTaskTrigger = New-ScheduledTaskTrigger @taskTrigger
````

### Create new task principal

Specifies the security context in which a task runs.

Parameter LogonType:

Specifies the security logon method that Task Scheduler uses to run the tasks that are associated with the principal.

The acceptable values for this parameter are:

- None
- Password
- S4U
- Interactive
- Group
- ServiceAccount
- InteractiveOrPassword

For more information about LogonType values, see [Principal.LogonType](https://learn.microsoft.com/en-us/windows/win32/taskschd/principal-logontype#property-value)

````powershell
$taskPrincipal = @{
    UserID    = 'NT AUTHORITY\SYSTEM'
    LogonType = 'ServiceAccount'
    RunLevel  = 'Highest'
}
$ScheduledTaskPrincipal = New-ScheduledTaskPrincipal @taskPrincipal
````

### Create new task settings

Settings for teh Task ...

````powershell
$taskSettings = @{
    ExecutionTimeLimit = (New-TimeSpan -Hours 1)
}
$ScheduledTaskSettingsSet = New-ScheduledTaskSettingsSet @taskSettings
````

### Register the Scheduled Task

````powershell
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
````

````powershell
Get-ScheduledTask -TaskName "RestartOnce" | Select *

Get-ScheduledTask "RestartOnce" | Get-ScheduledTaskInfo | Select *
````

### Register a Scheduled Task as User

Running the Task with Different Privileges. (Have to test the differences between this and New-ScheduledTaskPrincipal)

````powershell
$Credentials = Get-Credential

$registerTask = @{
    TaskName    = "PowerShell Task"
    Description = "Run a PowerShell Script"
    Action      = $ScheduledTaskAction
    Trigger     = $ScheduledTaskTrigger
    TaskPath    = 'PSTasks'
    User        = $Credentials.UserName
    Password    = $Credentials.GetNetworkCredential().Password
    RunLevel    = 'Highest'
}

Register-ScheduledTask @registerTask
````

### Delete a Scheduled Task

````powershell
# Delete the new PowerShell scheduled task
Unregister-ScheduledTask -TaskName "RestartOnce" -Confirm:$false
````

### Task Actions

Action: Start a program

Program/script: ````%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe````

Add arguments: ````-NoProfile -NoLogo -NonInteractive -ExecutionPolicy Bypass -File "C:\Temp\MyScript.ps1"````

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
````

````powershell
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
