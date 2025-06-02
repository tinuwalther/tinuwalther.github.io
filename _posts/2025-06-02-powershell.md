---
layout: post
title:  "PowerShell Settings"
author: Tinu
categories: "PowerShell-Basic"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Delay PowerShell start](#delay-powershell-start)
- [See also](#see-also)

## Delay PowerShell start

Skip Powershell startup check for new version.

- ````Off```` turns off the update notification feature
- ````Default```` is the same as not defining POWERSHELL_UPDATECHECK:
  - GA releases notify of updates to GA releases
  - Preview/RC releases notify of updates to GA and preview releases
- ````LTS```` only notifies of updates to long-term-servicing (LTS) GA releases

````powershell
[System.Environment]::SetEnvironmentVariable("POWERSHELL_UPDATECHECK", "Off", [System.EnvironmentVariableTarget]::Machine)
````

Include all other settings (for user and machine):

````powershell
$variables = [ordered]@{
   POWERSHELL_CLI_TELEMETRY_OPTOUT = "1"
   POWERSHELL_TELEMETRY_OPTOUT     = "1"
   POWERSHELL_UPDATECHECK          = "Off"
   POWERSHELL_UPDATECHECK_OPTOUT   = "1"
   DOTNET_CLI_TELEMETRY_OPTOUT     = "1"
   DOTNET_TELEMETRY_OPTOUT         = "1"
   COMPlus_EnableDiagnostics       = "0"
}

foreach ($target in "User","Machine") {
    Write-Host "Target: $target" -foregroundcolor cyan
    ($key in $variables.Keys) {
        Write-Host "  $key = $($variables.$Key)"
        [Environment]::SetEnvironmentVariable($key,$variables.$Key, $target)
    }
}
````

## See also

[About_Update_Notifications](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_update_notifications?view=powershell-7.5) on Microsoft Docs.
