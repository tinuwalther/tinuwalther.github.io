---
title: Securitylog auswerten
date: '2017-06-22T10:14:32+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Eventlog
- PSObject
- Regex
- Security
wordpress_id: 2216
layout: post
permalink: /wiki/securitylog-auswerten/
render_with_liquid: false
---

## Securitylog mit Regex auswerten

### Logon Events

```
function CheckLogons{
    [cmdletbinding()]
    Param($days)
    $ret = @()
    $Logname          = 'Security'
    [DateTime]$now    = Get-Date
    [DateTime]$after  = $now.AddDays(-$days)
    [DateTime]$before = $now
    $events = Get-EventLog -LogName $Logname -InstanceId 4624,4625,4634 -After $after -Before $before
    foreach($event in $events)
    {
        $content  = $event.message | Find-Matches -Pattern 'account name:\s+\w+'
        if($content.Count -eq 2){
            $account = $content[1]
        }
        else{
            $account =  $content 
        }

        $account  = (($account -split ':')[1]) -replace '\s+',''
        $notmatch = "DWM|SYSTEM|IUSR|LOCAL|NETWORK|$($env:ComputerName)" 
        if($account -notmatch $notmatch) {

            #region EventType
            switch ($event.EventID){
                4624 {$EventType = 'An account was successfully logged on'}
                4625 {$EventType = 'An account failed to log on'}
                4634 {$EventType = 'An account was logged off'}
            }
            #endregion

            #region LogonType
            if($event.Message | Select-String -Pattern 'Logon Type:\s+[2]') {
                $LogonType = 'Interactive' 
            }
            if($event.Message | Select-String -Pattern 'Logon Type:\s+[3]') {
                $LogonType = 'Network' 
            }
            if($event.Message | Select-String -Pattern 'Logon Type:\s+[4]') {
                $LogonType = 'Batch' 
            }                        
            if($event.Message | Select-String -Pattern 'Logon Type:\s+[5]') {
                $LogonType = 'Service' 
            }                        
            if($event.Message | Select-String -Pattern 'Logon Type:\s+[7]') {
                $LogonType = 'Computer Unlocked' 
            }                        
            if($event.Message | Select-String -Pattern 'Logon Type:\s+[9]') {
                $LogonType = 'RunAs' 
            }                        
            if($event.Message | Select-String -Pattern 'Logon Type:\s+[10]') {
                $LogonType = 'Remote Interactive' 
            }
            if($event.Message | Select-String -Pattern 'Logon Type:\s+[11]') {
                $LogonType = 'Cached Logon' 
            }
            #endregion

            #region Workstation
            $content = $event.message | Find-Matches -Pattern 'Workstation Name:\s+\w+'
            if($Workstation.Count -eq 2){
                $Workstation = $content[1]
            }
            else{
                $Workstation =  $content 
            }
            $Workstation  = (($Workstation -split ':')[1]) -replace '\s+',''
            #endregion

            $obj = New-Object PSObject
            $obj | Add-Member NoteProperty TimeGenerated $event.TimeGenerated
            $obj | Add-Member NoteProperty EventID       $event.EventID
            $obj | Add-Member NoteProperty EntryType     $event.EntryType
            $obj | Add-Member NoteProperty EventType     $EventType
            $obj | Add-Member NoteProperty Account       $account
            $obj | Add-Member NoteProperty Workstation   $Workstation
            $obj | Add-Member NoteProperty LogonType     $LogonType
            $ret += $obj
       }
    }
    return $ret
}

Function Find-Matches 
{
    Param($Pattern)
    Process {
        $_ | Select-String -pattern $Pattern -AllMatches |
        Select-Object -ExpandProperty matches |
        Select-Object -ExpandProperty value
    }
}
```

### Andere Events

 Event ID 4663, **An attempt was made to access an object**, which is logged for any kind of audited file access like read, write, delete, etc. Event ID 4670, **Permissions on an object were changed**, provides the before and after permissions of the object under Permissions Change. Damit diese Events überhaupt aufgezeichnet werden, muss per Policy unter **Computer Configuration\\Windows Settings\\Security Settings** folgendes eingestellt werden: 

- Advanced Audit Policy Configuration\\System Audit Policies\\Object Access = Enable File System for success
- Local Policies\\Security Options = Enable Audit: Force audit policy subcategory settings to override audit policy category settings
 

```
function Find-Matches 
{
    Param($Pattern)
    Process {
        $_ | Select-String -pattern $Pattern -AllMatches |
        Select-Object -ExpandProperty matches |
        Select-Object -ExpandProperty value
    }
}            

function Get-MessageContent{
    [cmdletbinding()]
    param(
        $message,
        $pattern
    )
    $content  = $message | Find-Matches -Pattern $pattern
    if($content.Count -eq 2){
        $ret = $content[1]
    }
    else{
        $ret =  $content 
    }
    return $ret
}
$Logname          = 'Security'
[DateTime]$now    = Get-Date
[DateTime]$after  = $now.AddHours(-24)
[DateTime]$before = $now
$events = Get-EventLog -LogName $Logname -InstanceId 4670,4663 -After $after -Before $before
$ret = @()
foreach($event in $events)
{
    $ret1 = ((Get-MessageContent -message $event.Message -pattern 'Security ID:\s+.+')    -split ':')    -replace '\s+',''
    $ret2 = ((Get-MessageContent -message $event.Message -pattern 'Account Name:\s+\w+')  -split ':')    -replace '\s+',''
    $ret3 = ((Get-MessageContent -message $event.Message -pattern 'Account Domain:\s+.+') -split ':')    -replace '\s+',''
    $ret4 = ((Get-MessageContent -message $event.Message -pattern 'Object Name:\s+.+')    -split ':')    -replace '\s+',''
    $ret5 = ((Get-MessageContent -message $event.Message -pattern 'Process Name:\s+.+')   -split ':\s+') -replace '\s+',''
    $ret6 = ((Get-MessageContent -message $event.Message -pattern 'Access Mask:\s+.+')    -split ':')    -replace '\s+',''
    
    $obj = New-Object PSObject -Property @{ 
        TimeGenerated = $event.TimeGenerated
        InstanceId    = $event.InstanceId
        $ret1[0] = $ret1[1]
        $ret2[0] = $ret2[1]
        $ret3[0] = $ret3[1]
        $ret4[0] = $ret4[1]
        $ret5[0] = $ret5[1]
        $ret6[0] = $ret6[1]
    }
    $ret += $obj
} 
$ret | sort TimeGenerated | ft
```