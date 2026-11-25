---
title: SQLiteDB
date: '2023-05-09T20:00:15+02:00'
author: Tinu
excerpt: SQLite ist eine Datenbank-Management-Lösung in einer C-Programmierbibliothek.
  Jeff Hicks hat dazu ein PowerShell-Module auf der PowerShell Gallery veröffentlicht
  und das schaue ich mir jetzt an.
categories:
- Datenbank
tags:
- PowerShell
- SQLiteDB
image: /assets/wiki/sqlite.png
wordpress_id: 3780
layout: post
permalink: /wiki/sqlitedb/
render_with_liquid: false
---

SQLite ist eine Datenbank-Management-Lösung in einer C-Programmierbibliothek.

## PowerShell Module mySQLite von Jeffery Hicks

A set of PowerShell commands for working with SQLite database files. This is a simple alternative to installing any version of SQL Server on your desktop. **Note that this module will only work on Windows platforms**.



```
Install-Module -Name mySQLite
```

## New-SqlLiteDB

Eine neue Datenbank mit Tabelle aus einem CSV-File mit den Inventar-Daten von ESXiHosts erstellen:



```
$CSVFile      = 'C:\Temp\VMwareInv.csv'
$DBFile       = 'C:\Temp\VMwareInv.db'
$SqlTableName = 'ESXiHosts'
$SqlTypeName  = 'PSXi' 

$data = Import-Csv -Delimiter ';' -Path $CSVFile -Encoding utf8
$data | Add-Member NoteProperty Created $(Get-Date)

"Create $($DBFile) with table $($SqlTableName)" | Out-Default
$SQLiteProperties = @{
    Path      = $DBFile
    TableName = $SqlTableName
    TypeName  = $SqlTypeName
    Primary   = 'HostName'
}
$data | ConvertTo-MySQLiteDB @SQLiteProperties -Force
```

## Insert-IntoDB

Daten aus einem CSV-File mit den Inventar-Daten von ESXiHosts einer bestehenden Tabelle hinzufügen:



```
$data | foreach-object -begin { 
    $MySQLiteDB = Open-MySQLiteDB -Path $DBFullPath
} -process { 
    $SqliteQuery = "Insert into $($SqlTableName) Values(
        '$($_.HostName)',
        '$($_.Version)',
        '$($_.Manufacturer)',
        '$($_.Model)',
        '$($_.vCenterServer)',
        '$($_.Cluster)',
        '$($_.PhysicalLocation)',
        '$($_.ConnectionState)',
        '$(Get-Date)'
    )"
    Invoke-MySQLiteQuery -connection $MySQLiteDB -keepalive -query $SqliteQuery
} -end { 
    Close-MySQLiteDB $MySQLiteDB
}
```

## Update-Table

Daten aus einem CSV-File mit den Inventar-Daten von ESXiHosts aktualisieren. Massgebend für die Aktualisierung ist hier der HostName, da dieser eindeutig sein muss:



```
$sqlite = Invoke-MySQLiteQuery -Path $DBFile -Query "Select * from $SqlTableName"
$data   = Import-Csv -Delimiter ';' -Path $CSVFile -Encoding utf8

if(
    ($data | Select-Object -last 1 -ExpandProperty HostName) -eq
    ($sqlite | Select-Object -Last 1 -ExpandProperty HostName)
){
    $data | foreach-object -begin { 
    $MySQLiteDB = Open-MySQLiteDB -Path $DBFullPath
    } -process { 
        $SqliteQuery = "Update $($SqlTableName)
        Set
            'Version'          = '$($_.Version)',
            'Manufacturer'     = '$($_.Manufacturer)',
            'Model'            = '$($_.Model)',
            'vCenterServer'    = '$($_.vCenterServer)',
            'Cluster'          = '$($_.Cluster)',
            'PhysicalLocation' = '$($_.PhysicalLocation)',
            'ConnectionState'  = '$($_.ConnectionState)',
            'Created'          = '$(Get-Date)'
        WHERE HostName LIKE '$($_.HostName)'"
        Invoke-MySQLiteQuery -connection $MySQLiteDB -keepalive -query $SqliteQuery
    } -end { 
        Close-MySQLiteDB $MySQLiteDB
    }
}
```

Weitere Informationen: [SQLite Tutorial](https://www.sqlitetutorial.net/), [sqlite.org](https://sqlite.org/index.html)

