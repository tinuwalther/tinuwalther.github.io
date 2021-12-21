---
layout: post
title:  "Low Memory Condition"
author: Tinu
categories: "PowerShell-Eventlog"
tags:   PowerShell News
permalink: /posts/:title:output_ext
---

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Low Memory Condition](#low-memory-condition)
  - [Identify the programs that trigger Low Memory Condition](#identify-the-programs-that-trigger-low-memory-condition)
  - [Configure Virtual Memory manually](#configure-virtual-memory-(pagefile)-manually)
  - [Check for corruption of your files](#check-for-corruption-of-your-files)
  - [Check for disk errors](#check-for-disk-errors)
- [See also](#see-also)

# Low Memory Condition

Low memory occurs when the device you are working runs **out of RAM** and also is **low on virtual memory**. This can happen in a situation where you burden your device with programs that cannot be supported by its RAM. Another instance when low memory error can occur is **when the programs do not free the memory** they have been using after their completion. We call this process memory overuse or **memory leak**.

## Identify the programs that trigger Low Memory Condition

This function can be used to identify the programs that trigger Low Memory Condition of a Windows Server.

````powershell
function Get-LowMemoryCondition{

    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$false)]
        [Int]$LastMonth = 1,

        [Parameter(Mandatory=$false)]
        [Int32]$EventId = 2004
    )
    $function = $($MyInvocation.MyCommand.Name)
    Write-Verbose "Running $function"
    
    $RegExApplication = '(?<=\s)(\w+)(?=\.\w{3})'
    $RegExBytes       = '(?<=consumed\s)(\d+)(?=\sbytes)'
    $RegExPID         = '(?<=\s\()(\d+)(?=\)\s)'

    $Application = $null; $bytes = $null; $ID = $null

    $EventParameter = @{
        ProviderName = 'Microsoft-Windows-Resource-Exhaustion-Detector'
        StartTime    = (Get-Date).AddMonths(-$LastMonth)
    }

    $EventProperties = @(
        'TimeCreated','LogName','ProviderName','Id','LevelDisplayName','Message','MachineName'
    )

    try{
        $WinEvent = (Get-WinEvent -FilterHashtable $EventParameter -ErrorAction Stop).({Where $_.Id -eq $EventId}) | Select-Object $EventProperties 
        foreach($Message in $WinEvent){
            foreach($item in $Message.Message){
                $line = ($item -split '\:')[1]
                ($line -split '\,') | ForEach-Object {
                    if($_ -match $RegExApplication){$Application = $Matches[0]}
                    if($_ -match $RegExBytes){$bytes = $Matches[0] }
                    if($_ -match $RegExPID){$ID = $Matches[0]}
                    [PSCustomObject]@{
                        TimeCreated = $Message.TimeCreated
                        FullItem    = $_.Trim()
                        Application = $Application
                        Id          = $ID
                        UsedMB      = '{0:N0}' -f ($bytes/1mb)
                    }
                }
            }
        }
    }catch{
        [PSCustomObject]@{
            Succeeded  = $false
            Function   = $function
            TimeStamp  = (Get-Date)
            Scriptname = $($_.InvocationInfo.ScriptName)
            LineNumber = $($_.InvocationInfo.ScriptLineNumber)
            Activity   = $($_.CategoryInfo).Activity
            Message    = $($_.Exception.Message)
            Category   = $($_.CategoryInfo).Category
            Exception  = $($_.Exception.GetType().FullName)
            TargetName = $($_.CategoryInfo).TargetName
        } 
        $error.Clear()
    }
}

Get-LowMemoryCondition -LastMonth 1
````

## Configure Virtual Memory (Pagefile) manually

Disable automatic-managed PageFile, set the initial- and maximum-size manually and rebbot the computer:

````powershell
$InitialSizeMB = 4096
$MaximumSizeMB = 4096

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
   $pagefile.InitialSize = $InitialSizeMB
   $pagefile.MaximumSize = $MaximumSizeMB
   $pagefile.Put() | Out-Null
   gwmi -Class Win32_PageFileSetting | select Name,InitialSize,MaximumSize | fl
   Start-Sleep -Seconds 20
   Restart-Computer
}
````

## Check for corruption of your files

Start the prompt as the administrator and type in these letters

````
sfc /scannow
````

## Check for disk errors

Start the prompt as the administrator and type in these letters

````
chkdsk C:/f
````

or scan with no reboot and no fixing

````
chkdsk C: /scan
````

# See also

[How to Use PowerShell to Write to Event Logs](https://devblogs.microsoft.com/scripting/how-to-use-powershell-to-write-to-event-logs/) on devblogs.microsoft.com

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]