---
title: Remoting mit PSExec
date: '2016-10-25T07:22:40+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Remote Commands
wordpress_id: 1668
layout: post
permalink: /wiki/remoting-mit-psexec/
render_with_liquid: false
---

PsExec v2.11 von [sysinternals](https://technet.microsoft.com/en-us/sysinternals/pxexec.aspx)

## Verwendung

```
Psexec [\\Computer[,Computer2[,...] | @Datei]
[-u Benutzer [-p Kennwort]]
[-n s]
[-l]
[-s|-e]
[-x]
[-i [Sitzung]]
[-c [-f|-v]]
[-w Verzeichnis]
[-d]
[-<Priorität>]
[-a n,n,... ] 
[-accepteula]
cmd [Argumente]
```

 Computer Weist PsExec an, die Anwendung auf den angegebenen Computern auszuführen. @Datei Weist PsExec an, den Befehl auf allen Computern auszuführen, die in der angegebenen Textdatei aufgeführt sind. -c Kopiert das angegebene Programm zur Ausführung auf das Remotesystem. Wenn Sie diese Option nicht angeben, muss sich die Anwendung auf dem Remotesystem im Systempfad befinden. -d Beenden der Anwendung nicht abwarten. Verwenden Sie diese Option nur für nichtinteraktive Anwendungen. -e Lädt nicht das Profil des angegebenen Kontos. -f Kopiert das angegebene Programm selbst dann auf das Remotesystem, wenn die Datei bereits auf dem Remotesystem vorhanden ist. -i Führt das Programm so aus, dass es mit dem Desktop für die angegebene Sitzung auf dem Remotesystem interagiert. Wenn Sie keine Sitzung angeben, wird der Prozess in der Konsolensitzung ausgeführt. -l Führt den Prozess als Benutzer mit eingeschränkten Rechten aus. (Die Administratorengruppe wird entfernt, und es werden nur solche Berechtigungen zugelassen, die der Benutzergruppe zugewiesen wurden.) Unter Windows Vista wird der Prozess mit niedriger Integrität ausgeführt. -n Gibt das Timeout in Sekunden für die Verbindung mit Remotecomputern an. -p Gibt das optionale Kennwort für den Benutzernamen an. Wenn Sie diese Option nicht verwenden, werden Sie aufgefordert, ein Kennwort einzugeben, wobei dieses Kennwort bei der Eingabe nicht angezeigt wird. -s Führt den Remoteprozess im Systemkonto aus. -u Gibt den optionalen Benutzernamen für die Anmeldung beim Remotecomputer an. -v Kopiert die angegebene Datei nur dann, wenn sie eine höhere Versionsnummer besitzt oder neuer ist als die Datei auf dem Remotesystem. -w Gibt das Arbeitsverzeichnis für den Prozess an (relativ zum Remotecomputer). -x Zeigt die grafische Benutzeroberfläche auf dem Winlogon-Desktop an (nur lokales System). -Priorität Führt den Prozess in der angegebenen Priorität aus. Zulässige Optionen: -low, -belownormal, -abovenormal, -high, -realtime. Programm Name des auszuführenden Programms. Argumente Die zu übergebenden Argumente. (Die Dateipfade müssen dabei absolute Pfade auf dem Zielsystem sein.) 

## Commands

- psexec \\\\hostname cmd &gt;&gt; c:\\temp\\ausgabe.txt
- psexec \\\\hostname reg add \\\\COMPUTERNAME\\HKLM\\System\\CurrentControlSet\\Services\\LanmanServer\\Parameters /t REG\_DWORD /v autosharewks /d 1 /f
 

### Command Prompt

```
psexec "\\$($server)" -u "$($server)\$($user)" -p $cpwd -d -h cmd \c 'echo . | tasklist'
```

### PowerShell

```
psexec "\\$($server)" -u "$($server)\$($user)" -p $cpwd -d -h powershell -command '&'C:\Admin\Scripts\Wsus\WSUSInstallUpdates.ps1 -Force"" 2>&1
```

## Voraussetzungen

 Benutzt SMB 445 auf Admin-Share C$ oder IPC$ 

### UAC ausschalten

 **Pfad:** Local Computer Policy, Computer Configuration, Windows Settings,Security Settings, Local Policies, Security Options, User Account Control Sicherstellen, dass User Account Control: **Use Admin Approval Mode for the built-in Administrator account** disabled ist. Sicherstellen, dass User Account Control: **Behavior of the elevation prompt for administrators in Admin Approval Mode auf Elevate without prompting** eingestellt ist 

### PowerShell Execution Policy

 **Pfad:** Local Computer Policy, Computer Configuration, Administrativ Templates,Windows Components, Windows PowerShell, **Turn on Script Execution Policy** Sicherstellen, dass Turn on Script Execution Policy auf **Allow local scripts and remote signed scripts** eingestellt ist. 

### Windows Firewall

 Print and Share...SMB 445 incomming 

### LocalAccountTokenFilterPolicy

 Set-ItemProperty HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System -Name LocalAccountTokenFilterPolicy -Value 1 DWORD-Wert (32bit)