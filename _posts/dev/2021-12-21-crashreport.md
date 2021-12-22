---
layout: post
title:  "Reboot and Crash-Report"
author: Tinu
categories: "PowerShell-Eventlog"
tags:   PowerShell News
permalink: /posts/:title:output_ext
---

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Restart History](#restart-history)
- [Restart or Crash-Report](#restart-or-crash-report)
- [See also](#see-also)

# Restart History

Create a restart history

````powershell
$LastBootupTime      = (Get-CimInstance Win32_OperatingSystem).LastBootupTime
[DateTime]$StartTime = $LastBootupTime.AddHours(-1)
[DateTime]$EndTime   = $LastBootupTime.AddHours(1)

Write-Host "LastBooupTime $(Get-Date $LastBootupTime -f 'yyyy-MM-dd HH:mm:ss')"
````

EventLog Service messages:

````powershell
Get-WinEvent -FilterHashtable @{
   Logname   = 'System'
   StartTime = $StartTime
   EndTime   = $EndTime
} | Where Id -match '600\d' | Select TimeCreated,Id,Message,ProviderName | Format-Table
````

Application.exe has initiated the restart of computer:

````powershell
$RestartyApplication = Get-WinEvent -FilterHashtable @{
   Logname   = 'System'
   StartTime = $StartTime
   EndTime   = $EndTime
} | Where Id -match '1074' | Select TimeCreated,Id,Message,ProviderName

foreach($item in $RestartyApplication){
   if($_.Message -match 'CCM\\TSManager\.exe'){
      $message = "Restarted by System Center Configuration Manager"
   }elseif($_.Message -match 'VMware Tools\\vmtoolsd.exe'){
      $message = "Restarted by VMware Tools (API)"
   }else{
      $message = $_.Message
   }
   [PSCustomObject]@{
      TimeCreated  = $item.TimeCreated
      EventId      = $item.Id
      Message      = $message
      ProviderName = $item.ProviderName
   }
}
````

# Restart or Crash-Report

````powershell
$params = @{
    LogName   = 'System'
    Id = 2004,6008,1074,41,1001,46
    StartTime = (Get-Date).AddDays(-2)
    EndTime   = (Get-Date)
 }
Get-WinEvent -FilterHashtable $params | Select-Object TimeCreated,Id,Message
````

````
TimeCreated : 21.12.2021 12:29:14
Id          : 1001
Message     : The computer has rebooted from a bugcheck. 
              The bugcheck was: 0x0000009f (0x0000000000000005, 0xffff950d5f4cc060, 0xffff950d7c5f0920, 0x0000000000000000). 
              A dump was saved in: C:\WINDOWS\MEMORY.DMP. 
              Report Id: cdc03408-1c74-42d1-ad9c-caae62d7edc3.

TimeCreated : 21.12.2021 12:29:01
Id          : 41
Message     : The system has rebooted without cleanly shutting down first.
              This error could be caused if the system stopped responding, crashed, or lost power unexpectedly.

TimeCreated : 21.12.2021 12:29:09
Id          : 6008
Message     : The previous system shutdown at 11:59:15 on 21.12.2021 was unexpected.

TimeCreated : 20.12.2021 18:56:59
Id          : 1074
Message     : The process C:\Windows\System32\RuntimeBroker.exe (Computer1) has initiated the power off of computer Computer1 on behalf of
              user Computer1\Admin for the following reason: Other (Unplanned)
               Reason Code: 0x0
               Shut-down Type: power off
               Comment:

TimeCreated : 20.12.2021 16:51:52
Id          : 1074
Message     : The process C:\WINDOWS\system32\winlogon.exe (Computer1) has initiated the restart of computer Computer1 on behalf of
              user NT AUTHORITY\SYSTEM for the following reason: No title for this reason could be found
               Reason Code: 0x500ff
               Shut-down Type: restart
               Comment:

TimeCreated : 20.12.2021 16:51:50
Id          : 1074
Message     : The process rundll32.exe has initiated the restart of computer Computer1 on behalf of user Computer1\Admin for the 
              following reason: Other (Unplanned)
               Reason Code: 0x0
               Shut-down Type: restart
               Comment:
````

# See also

[How to Use PowerShell to Write to Event Logs](https://devblogs.microsoft.com/scripting/how-to-use-powershell-to-write-to-event-logs/) on devblogs.microsoft.com

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]