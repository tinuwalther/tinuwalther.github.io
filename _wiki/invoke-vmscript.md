---
title: Invoke-VMScript
date: '2021-10-13T10:16:00+02:00'
author: Tinu
excerpt: Mit PowerCLI Invoke-VMScript kann ein Command oder ein Script auf einer VM
  ausgeführt und das Resultat zurück gegeben werden.
categories:
- Virtualisierung
tags:
- PowerCLI
- VMware
image: /assets/wiki/vmware-e1620821111224.png
wordpress_id: 3471
layout: post
permalink: /wiki/invoke-vmscript/
render_with_liquid: false
---

Mit PowerCLI Invoke-VMScript kann ein Command oder ein Script auf einer VM ausgeführt und das Resultat zurück gegeben werden.

## Requirements

- PowerCLI 12.3.x auf dem ausführenden Computer
- TCP Port (manchmal liest man auch vom UDP Port) 902 vom ausführenden Computer auf den ESXi Host, welcher die Guest VM hostet
- Guest VM muss eingeschaltet sein
- Administrator Rechte auf der Guest VM
- VMware tools sind auf der Guest VM installiert

## Command ausführen

```
#region Guest-VM
$guestvm       = 'test123'
$guestaccount  = 'localadmin'
$guestpassword = Read-Host -AsSecureString -Prompt "Enter the password for $($guestaccount)"
$guestcred     = New-Object System.Management.Automation.PSCredential ($guestpassword, $guestpassword)
#endregion

$command = 'Get-ChildItem C:\Temp' 

if(Get-VM -Name $guestvm) {
    $VMScriptRet = Invoke-VMScript -VM $guestvm - Credential $guesrcred -ScriptText $command
    $VMScriptRet
} 
```

## Scriptblock ausführen

Ein Script wird als String (Text) auf die Guest VM übertragen und dort ausgeführt. Das Resultat kommt ebenfalls als String (Text) zurück. Will man ein Object zurückgeben, so kann man dieses in einen JSON-String und dann wieder in ein Object zurück konvertieren.

```
#region Guest-VM
$guestvm       = 'test123'
$guestaccount  = 'localadmin'
$guestpassword = Read-Host -AsSecureString -Prompt "Enter the password for $($guestaccount)"
$guestcred     = New-Object System.Management.Automation.PSCredential ($guestpassword, $guestpassword)
#endregion

$Scriptblock = @'
    Get-Process | ConvertTo-Json -Depth 1 -WarningAction SilentlyContinue
'@

if(Get-VM -Name $guestvm) {
    $VMScriptRet = Invoke-VMScript -VM $guestvm - Credential $guesrcred -ScriptText $Scriptblock -ScriptType PowerShell
    if($VMScriptRet){
        $VMScriptRet.Output | ConvertFrom-Json
    }
} 
```

## Script kopieren

Script auf Guest VM kopieren.

```
#region Guest-VM
$guestvm       = 'test123'
$guestaccount  = 'localadmin'
$guestpassword = Read-Host -AsSecureString -Prompt "Enter the password for $($guestaccount)"
$guestcred     = New-Object System.Management.Automation.PSCredential ($guestpassword, $guestpassword)
#endregion

$SourceScript = 'D:\Scripts\Get-AllProcess.ps1'
$TargetPath   = 'C:\Temp\'

if(Get-VM -Name $guestvm) {
    Copy-VMGuestFile -Source $SourceScript -Destination $TargetPath -VM $guestvm -LocalToGuest -Credential $guesrcred
} 
```

## Script ausführen

Ein Script kann ebenfalls mit Invoke-VMScript ausgeführt werden, dazu wird dem Parameter ScriptText anstelle eines Commands oder ScriptBlocks der Pfad zu dem (lokal vorhandenen) Script mitgegeben.

```
#region Guest-VM
$guestvm       = 'test123
$guestaccount  = 'localadmin'
$guestpassword = Read-Host -AsSecureString -Prompt "Enter the password for $($guestaccount)"
$guestcred     = New-Object System.Management.Automation.PSCredential ($guestpassword, $guestpassword)
#endregion

$ScriptFullName = 'C:\Temp\Get-AllProcess.ps1' 

if(Get-VM -Name $guestvm) {
    $VMScriptRet = Invoke-VMScript -VM $guestvm -Credential $guesrcred -ScriptText $ScriptFullName -ScriptType PowerShell
    if($VMScriptRet){
        $VMScriptRet.Output | ConvertFrom-Json
    }
} 
```

## UAC Problematik

<https://communities.vmware.com/t5/VMware-PowerCLI-Discussions/Invoke-VMScript-to-run-ps-commands-as-an-administrator/td-p/2196652>

```
#region Guest-VM
$guestvm       = 'test123
$guestaccount  = 'localadmin'
$guestpassword = Read-Host -AsSecureString -Prompt "Enter the password for $($guestaccount)"
$guestcred     = New-Object System.Management.Automation.PSCredential ($guestpassword, $guestpassword)
#endregion

$ScriptText = "Start-Process powershell -Credential $guestcred -ArgumentList '-noprofile -noninteractive -command get-service'" 

if(Get-VM -Name $guestvm) {
    $VMScriptRet = Invoke-VMScript -VM $guestvm - Credential $guesrcred -ScriptText $ScriptText -ScriptType PowerShell
    if($VMScriptRet){
        $VMScriptRet.Output
    }
} 
```

## Reference