---
title: Script Control
date: '2014-11-26T19:47:48+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Scripting
wordpress_id: 127
layout: post
permalink: /wiki/script-control/
render_with_liquid: false
---

# Script Steuerung

 Am Ende des Scriptfiles (der Prozedur) wird die ganze Ablaufsteuerung vorgenommen. 

```
#region script control
if($PSVersionTable.PSVersion.Major -ge 4){
Set-StrictMode -Version latest
if($Error.Count -gt 0){$Error.Clear()}
if($psdebug){
    $ErrorActionPreference = 'Stop'
}
else{
    $ErrorActionPreference = 'SilentlyContinue'
}

"$(Get-Date -DisplayHint DateTime) [INFORMATION] Start $($script:Scriptname), Version $($script:version)" | Out-File -FilePath "$($script:Scriptpath)\$($script:Logfile)" -Append -Encoding default
$script:Scriptreturn += Get-LocalUser -Name Admin
if(!([String]::IsNullOrEmpty($Inputfile)) -and (Test-Path $Inputfile)){
    Get-Content $Inputfile
}
else{
    "$(Get-Date -DisplayHint DateTime) [  WARNING  ] Inputfile '$($Inputfile)' not found" | Out-File -FilePath "$($script:Scriptpath)\$($script:Logfile)" -Append -Encoding default
}
$duration = $([math]::round(((New-TimeSpan $($Global:ScriptStart) $(get-date)).TotalMinutes),2))
"$(Get-Date -DisplayHint DateTime) [INFORMATION] End $($script:Scriptname), Duration $($duration) Minutes, Errorcount $($Error.Count)" | Out-File -FilePath "$($script:Scriptpath)\$($script:Logfile)" -Append -Encoding default
#Calculate the duration of this script
#load the current logfile
Get-Content "$($script:Scriptpath)\$($script:Logfile)" -raw

$script:Scriptreturn
#endregion
}
```

 Ich glaube dieser Code ist selbsterklärend, falls nicht bitte via Kontaktformular melden.