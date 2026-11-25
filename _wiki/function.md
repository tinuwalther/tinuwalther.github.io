---
title: Function
date: '2014-11-26T19:44:57+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Scripttemplate
wordpress_id: 123
layout: post
permalink: /wiki/function/
render_with_liquid: false
---

# Konstrukt, das einen Wert zurückliefert

 Befehlsabfolgen, welche zusammengehören sollen in Functions zusammengefasst werden. 

```
function GetSomething{
     <#
      .DESCRIPTION
           Get Something return . . .
      .EXAMPLE
           GetSomething -Param1 'Parameter 1' -Param2 'Parameter 2' -Param3 'Parameter 3'
     #>
     [CmdletBinding()]
     param(
          [Parameter(Mandatory=$true)][String] $Param1,
          [Parameter(Mandatory=$true)][String] $Param2,
          [Parameter(Mandatory=$true)][String] $Param3
     )
     $ret = 0; $function = $($MyInvocation.MyCommand.Name)
     if ($psdebug){Write-Verbose "$($function) ..." -Verbose}
     try{
          write-host $Param1, $Param2, $Param3 -ErrorAction Stop
     }
     catch [Exception]{
          $message = "$($function): $($_.Exception.GetType().FullName) - $($_.Exception.Message)"
          if($psdebug){Write-Verbose $message -Verbose}
          $error.clear()
     }
     finally{
          write-host "Finally block reached, cleanup"
     }
     return $ret
}
```

 Innerhalb einer Function sieht es zuerst genau so aus wie wir es schon von vorherigen Kapiteln kennen, Header und Parameter. Danach wird als erstes die Variable für den Return deklariert und initialisiert $ret = 0. Der Return kann wie hier ein numerischer Wert aber auch jeder andere Datentyp sein. Mit $function füllen wir den Namen der Function für das Logging ab. Danach wird eine Zeile für das Debuggen geschrieben bevor es zum Errorhandling mit try{} catch{} kommt. Der Try-Block sichert alles ab, was einen Fehler auslösen könnte und im Catch-Block werden die Ausnahmen weiterverarbeitet, hier wird der Fehler im Debugmodus an den Screen ausgegeben.