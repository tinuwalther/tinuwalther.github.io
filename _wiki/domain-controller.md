---
title: Domain Controller konfigurieren
date: '2014-11-30T11:19:15+01:00'
author: Tinu
excerpt: ''
categories:
- Active Directory
tags:
- Active Directory
wordpress_id: 293
layout: post
permalink: /wiki/domain-controller/
render_with_liquid: false
---

Nachdem wir einen Windows Server 2012 R2 bereitgestellt und mit dem Post-Staging-Script konfiguriert haben, können wir den Server zu einem Domain Controller promoten und damit einen Forest/Domain erstellen.

## Features installieren

 Auf dem zukünftigen Domain Controller müssen die Features Active-Directory-Domain-Services mit den Management-Tool installiert werden. Das machen wir natürlich mit einem PowerShell-Script: 

```
function InstallADDSFeatures{
    <#
    .SYNOPSIS
        Install ADDSFeatures
    #>
    $function = $($MyInvocation.MyCommand.Name)
    if ($psdebug){LogInfo -Function $function -Message "..." -info}
	try{
		$ret = Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools
		LogInfo -Function $function -Message "$($ret.FeatureResult) $($ret.ExitCode)" -info
	}
	catch{
		LogInfo -Function $function -Message "$($_.Exception.Message)" -error -print
		$error.clear()
	}
}
```

## Forest/Domain erstellen

 Sobald die ADDS-Features installiert sind, kann ein neuer Forest/Domain erstellt werden. Dabei wird DNS gleich mit installiert. 

```
function CreateNewForest{
    <#
    .SYNOPSIS
        Create new forest
    #>
    param(
	[Parameter(Mandatory=$true)][String] $DnsName,
        [Parameter(Mandatory=$true)][String] $secpwd
    )
    $function = $($MyInvocation.MyCommand.Name)
    if ($psdebug){LogInfo -Function $function -Message "..." -info}
	try{
		$ret = Install-ADDSForest -DomainName $DnsName -DomainMode Win2012R2 -ForestMode Win2012R2 -InstallDns -Force -SafeModeAdministratorPassword $secpwd -SkipPreChecks
		LogInfo -Function $function -Message "$($ret.Message) $($ret.Status)" -info
	}
	catch{
		LogInfo -Function $function -Message "$($_.Exception.Message)" -error -print
		$error.clear()
	}
}
```

 Nach einem Reboot wird der Server als Domain Controller gestartet und man kann sich mit dem Administrator-Acount an der eben erstellten Domain als Domain Admin anmelden.