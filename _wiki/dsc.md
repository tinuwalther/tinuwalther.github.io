---
title: Desired State Configuration (DSC)
date: '2015-03-23T11:10:56+01:00'
author: Tinu
excerpt: DSC ist eine Plattform in PowerShell, mit der Configuration as Code angewendet
  werden kann wie mit Puppet, Chef oder ähnlichen Tools in der Linux Umwelt.
categories:
- Desired State
tags:
- Desired State
- PowerShell
image: /assets/wiki/DSC_Logo_300p.png
wordpress_id: 285
layout: post
permalink: /wiki/dsc/
render_with_liquid: false
---

# Windows Configuration Management

Windows PowerShell 4.0 bzw. Windows Management Framework 4 mit .NET Framework 4.52

Mit Windows PowerShell Desired State Configuration DSC Konfigurationen nachträglich ändern oder periodisch auf deren Richtigkeit prüfen ...

Nur was bekanntgemacht wurde kann entweder hinzugefügt oder entfernt werden.

Folgende Szenarien können mit den Built-in DSC Ressourcen abgedeckt werden:

- Windows Features installieren/deinstallieren
- Registry Settings konfigurieren
- Files und Folder erstellen/löschen und Inhalte bearbeiten
- Prozesse und Services konfigurieren und starten/stoppen
- Lokale Gruppen und User Accounts konfigurieren
- Software installieren
- Environment Variablen konfigurieren
- PowerShell-Scripts ausführen
- Archive entpacken (ZIP-Files)

## Push-Mode

Standardmässig ist DSC auf jedem Windows Server 2012 R2 im Push-Mode verfügbar.

Damit eine Configuration ausgeführt werden kann, muss diese auf dem jeweiligen Node lokal vorhanden sein und DSC muss mittels manuellem Aufruf oder Scheduel Task gestartet werden (siehe Erstellen und Ausführen der Configuration).

### **Prozess**

Schreiben einer Configuration (Authoring a Configuration) → Erstellen einer Configuration (Generate Configuration MOF File) → Ausführen der Configuration (Push Desired Configuration)

## Pull-Mode

Im Pull-Mode wird ein Pull-Server aufgesetzt wo sich die Nodes (bzw. deren Local Configuration Manager) periodisch melden und ihre Configurations abrufen und ggf. wieder herstellen...

Der Pull-Server muss gut vor Attacken geschützt werden, da von diesem Server aus all seine Managed Computer angegriffen werden können.

### Voraussetzungen

- Windows Management Framework 4.0 (WMF)
- IIS server role
- DSC Service
- ideally, some means of generating a certificate, to secure credentials passed to the Local Configuration Manager on target nodes

### Prozess

Schreiben einer Configuration (Authoring a Configuration) → Erstellen einer Configuration (Generate Configuration MOF File) → Generate a checksum file to accompany the MOF → Deploy the MOF and checksum files to the pull server → Configure the target node to use the pull Server

## Local Configuration Manager

Einstellungen des Local Configuration Manager anzeigen:

```
Get-DscLocalConfigurationManager

ActionAfterReboot              : ContinueConfiguration
AgentId                        : BE7BD933-955A-11E7-B62B-B4AE2BE2FF09
AllowModuleOverWrite           : False
CertificateID                  :
ConfigurationDownloadManagers  : {}
ConfigurationID                :
ConfigurationMode              : ApplyAndMonitor
ConfigurationModeFrequencyMins : 15
Credential                     :
DebugMode                      : {NONE}
DownloadManagerCustomData      :
DownloadManagerName            :
LCMCompatibleVersions          : {1.0, 2.0}
LCMState                       : Idle
LCMStateDetail                 :
LCMVersion                     : 2.0
StatusRetentionTimeInDays      : 10
SignatureValidationPolicy      : NONE
SignatureValidations           : {}
MaximumDownloadSizeMB          : 500
PartialConfigurations          :
RebootNodeIfNeeded             : False
RefreshFrequencyMins           : 30
RefreshMode                    : PUSH
ReportManagers                 : {}
ResourceModuleManagers         : {}
PSComputerName                 :

```

### LCM konfigurieren

Mit einer DSC Configuration kann der LCM am einfachsten konfiguriert werden.

```
#Write DSC Configuration for configure LCM
[DSCLocalConfigurationManager()]
configuration LCMConfig
{
    Node localhost
    {
        Settings
        {
            ConfigurationMode = 'ApplyAndAutoCorrect'
            RefreshMode       = 'Push'
        }
    }
}

#Generate MOF-File
LCMConfig -OutputPath "D:\Work\DSC\MOF"

#Set DSC LCMConfig
Set-DscLocalConfigurationManager -Path "D:\Work\DSC\MOF" -ComputerName localhost

#Get DSC LCMConfig
Get-DscLocalConfigurationManager
```

### Inhalt der MOF-Datei

```
/*
@TargetNode='localhost'
@GeneratedBy=Administrator
@GenerationDate=09/09/2017 15:39:45
@GenerationHost=W2K16-SRV1
*/

instance of MSFT_DSCMetaConfiguration as $MSFT_DSCMetaConfiguration1ref
{
 RefreshMode = "Push";
 ConfigurationMode = "ApplyAndAutoCorrect";

};

instance of OMI_ConfigurationDocument
{
 Version="2.0.0";
 MinimumCompatibleVersion = "1.0.0";
 CompatibleVersionAdditionalProperties= { "MSFT_DSCMetaConfiguration:StatusRetentionTimeInDays" };
 Author="Administrator";
 GenerationDate="09/09/2017 15:39:45";
 GenerationHost="W2K16-SRV1";
 Name="LCMConfig";
};
```

## Managed Computer

Sogenannte Nodes ...

## Built-in Ressourcen auflisten

```
Get-DscResource
Archive, Environment, File, Group, Log, Package, Registry, 
Script, Service, User, WindowsFeature, WindowsProcess
```

### Properties einer Ressource auflisten

```
Get-DscResource -Name WindowsFeature | Select -ExpandProperty Properties
Name, Credential, DependsOn, Ensure, IncludeAllSubFeature, LogPath, Source
```

## Schreiben einer Configuration

### WindowsFeature-Resource

```
configuration ServerConfiguration{
    Param([string]$ComputerName)
    # One can evaluate expressions to get the node list 
    # E.g: $AllNodes.Where("Role -eq Web").NodeName
    node ($ComputerName){
        WindowsFeature DhcpServer{
           Ensure = "Present"
           Name = "DHCP"
        }
        WindowsFeature DhcpServer-RSAT{
           Ensure = "Present"
           Name = "RSAT-DHCP"
        }      
    }
}
```

### File-Resource

```
configuration ServerConfiguration{
   Param(
      [string]$ComputerName,
      [string]$DscFolder
   )
   node ($ComputerName){
      File DscFolder{
         Type = 'Directory'
         DestinationPath = $DscFolder
         Ensure = 'Present'
      }
      File Now{
         Type = 'File'
         Contents = ''
         DestinationPath = "$DscFolder\$($now).txt"
         Ensure = 'Present'
         DependsOn = "[File]DscFolder"
      }
   }
}
```

### Registry-Resource

Registry Resource mit Abhängigkeiten zueinander.

```
configuration ServerConfiguration{
   Param(
      [string]$ComputerName,
      [string]$DscFolder
   )
   node ($ComputerName){
      # ValueData = String, Binary, Dword (32-bit number.), 
      # Qword (64-bit number), MultiString (Array), ExpandString
      Registry X1{
         Ensure = 'Present'
         Key = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
         ValueName = 'DSC-X1'
         ValueData = '0'
         ValueType = 'Dword'
      }
      Registry X2{
         Ensure = 'Present'
         Key = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
         ValueName = 'DSC-X2'
         ValueData = "Ein einfacher String mit Parameter: $DscFolder"
         ValueType = 'String'
         DependsOn = "[Registry]X1"
      }
      Registry X3{
         Ensure = 'Present'
         Key = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
         ValueName = 'DSC-X3'
         ValueData = @('1. Zeile','2. Zeile','3. Zeile')
         ValueType = 'MultiString'
         DependsOn = "[Registry]X2"
      }
      Registry X4{
         Ensure = 'Present'
         Key = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
         ValueName = 'DSC-X4'
         ValueData = '%PATH%'
         ValueType = 'ExpandString'
         DependsOn = "[Registry]X3"
      }
      Registry X5{
         Ensure = 'Present'
         Key = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
         ValueName = 'DSC-X5'
         ValueData = '11001001000010110100000100101'
         ValueType = 'Binary'
         DependsOn = "[Registry]X4"
      }
   }
}

```

### Script-Resource

TestScript wird immer als erstes durchgeführt. Nur wenn die TestScript $false zurückgibt, wird SetScript durchgeführt.

```
configuration ServerConfiguration{
   Param(
      [string]$ComputerName,
      [string]$DscFolder
   )
   node ($ComputerName){
      $now = Get-Date -Format 'yyyyMMdd-hhmmss'
      Script ScriptExample{
         TestScript = {
            Write-Verbose -Message 'Executing TestScript'
            Test-Path "$($using:DscFolder)\$($using:now).txt"
            Write-Verbose -Message 'Finished running TestScript'
         }
         SetScript = { 
           Write-Verbose -Message 'Executing SetScript'
           Get-Service | Where-Object {$_.Status -like 'Stopped'} | `
           Out-File "$($using:DscFolder)\$($using:now).txt"
           Write-Verbose -Message 'Finished running SetScript'
         }
         GetScript = {
            <# This must return a hash table @{'Key'='Item'}#>
            Write-Verbose -Message 'Executing GetScript'
            $Result = @{ 
               Result = $false
               GetScript = $GetScript
               SetScript = $SetScript
               TestScript = $TestScript
            }
            return $Result
            Write-Verbose -Message 'Finished running GetScript'
         } 
      }       
   }
}
```

[Erklärungen](http://trevorsullivan.net/2014/08/19/use-powershell-dsc-to-enable-screencast-recording-on-azure-vms/)

## Erstellen der Configuration (MOF-Datei)

```
$computer = (read-host 'Enter Computer name')
ServerConfiguration -OutputPath 'C:\DSC' -ComputerName $computer
```

## Ausführen der Configuration (MOF-Datei)

Die Configuration kann entweder auf dem lokalen Computer oder auch auf remote Computern ausgeführt werden. Bedingt, dass die Configuration im angegebenen Pfad auf jedem angesprochenen Computer abgespeichert ist.

```
$computer = (read-host 'Enter Computer name')
Start-DscConfiguration -Path 'C:\DSC' -ComputerName $computer -Verbose -Wait
```

## Prüfen der Configuration

```
Get-DscConfiguration -Verbose
Test-DscConfiguration -Verbose
```

Das [DSC Resource Kit](https://gallery.technet.microsoft.com/scriptcenter/DSC-Resource-Kit-All-c449312d "DSC Resource Kit") bietet zusätzliche Features an.

## Entfernen einer Configuration

DSC Configuration Document entfernen und LCM auf ApplyAndMonitor zurücksetzen.

```
[DSCLocalConfigurationManager()]

configuration LCMConfig{
    Node localhost{
        Settings{
            ConfigurationMode = 'ApplyAndMonitor'
            RefreshMode       = 'Push'
            ConfigurationModeFrequencyMins = 15
        }
    }
}

LCMConfig -OutputPath "C:\Admin\DSC\MOF"
Set-DscLocalConfigurationManager -Path "C:\Admin\DSC\MOF"

Remove-DscConfigurationDocument -Stage Current
Remove-Item "C:\Admin\DSC\MOF"
```

## References

[Windows PowerShell Desired State Configuration Overview](https://docs.microsoft.com/en-us/powershell/scripting/dsc/overview/overview?view=powershell-7.1), [DSC Community](https://github.com/dsccommunity), [octopus.com: Getting started with PowerShell Desired State Configuration (DSC)](https://octopus.com/blog/getting-started-with-powershell-dsc)

