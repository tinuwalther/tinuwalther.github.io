---
title: MssqlDB
date: '2021-05-23T14:02:27+02:00'
author: Tinu
excerpt: MssqlDBs mussten früher mit sqlcmd oder SQL Server Management Objects (SMO)
  bearbeitet werden. Heute kann das viel einfacher mit den dbatools und VSCode gemacht
  werden.
categories:
- Datenbank
tags:
- MSSQL
- PowerShell
- Scripting
- VSCode
image: /assets/wiki/MSSQL-e1620819331995.png
wordpress_id: 566
layout: post
permalink: /wiki/mssqldb/
render_with_liquid: false
---

MssqlDBs mussten früher mit sqlcmd oder SQL Server Management Objects (SMO) bearbeitet werden. Heute kann das viel einfacher mit den [dbatools](https://dbatools.io/) und VSCode gemacht werden.

## Docker

Mit Docker erstelle ich einen MSSQL Server Container auf Basis des offiziellen Images von Docker Hub.

### Environment erstellen

Custom Netzwerk und das Volume für den MSSQL Server erstellen:

```
docker network create custom
docker volume create sqldata
```

### Image und Container erstellen

Download the latest MSSQL Image.

```
docker pull mcr.microsoft.com/mssql/server:2019-latest
docker tag mcr.microsoft.com/mssql/server:2019-latest mssql:2019-latest
docker rmi mcr.microsoft.com/mssql/server:2019-latest

```

Create a container. Wichtig ist hier die Zeitzone (-e TZ="Europe/Zurich") zu setzen, damit bei einem Insert des aktuellen Datum/Zeit der korrekte TimeStamp geschrieben wird.

```
docker run -e TZ="Europe/Zurich" `
 -e 'ACCEPT_EULA=Y' `
 -e 'SA_PASSWORD=yourStrong(!)Password' `
 -p 8433:1433 `
 -v sqldata:/var/opt/mssql `
 --hostname mssqlsrv1 `
 --name mssqlsrv1 `
 --network custom `
 -d mssql:2019-latest
```

## Connect to MssqlDB

Nachdem der Container gestartet (`docker start mssqlsrv1`) ist, kann mit VSCode und den MSSQL Server Extensions auf die MssqlDB zugegriffen werden, siehe [Extension für MSSQL Server](/wiki/vs-code-datenbank-extensions/#Extension_fuer_MSSQL_Server).

## SQL Server Management Objects

Das Script liest alle Datenbanken der installierten Instanzen aus und listet den Namen, Owner, Collation, Default Schema und RecoveryModel auf.

```
$server = $($env:computername)
[System.Reflection.Assembly]::LoadWithPartialName('Microsoft.SqlServer.SMO')|Out-Null

(Get-ItemProperty 'HKLM:\Software\Microsoft\Microsoft SQL Server').InstalledIntances | % {
   "$($server)\$($_)"
   $sql = New-Object ('Microsoft.SqlServer.Management.Smo.Server') "$($server)\$($_)"
   $sql.Databases | Select Name,Owner,Collation,DefaultSchema,RecoveryModel | ft -auto
}
```

## dbatools

Mit dem PowerShell Module [dbatools](https://dbatools.io/) wird es viel einfacher mit MSSQL Server zu arbeiten.

### Connect to SQL Instance

```
if([String]::IsNullOrEmpty($sqlcred)){
    $sqlcred = Get-Credential sa
}
$mssqlsrv = Connect-DbaInstance -SqlInstance 'localhost:8433' -Database tinu -SqlCredential $sqlcred
```

### Get Database

```
Get-DbaDatabase -SqlInstance $mssqlsrv | FT
```

### Max Memory

Das häufigste Problem mit MSSQL Server im Support ist das Max Memory. Meine Erfahrung hat gezeigt, dass normalerweise (fast) kein DBA-Verantwortlicher das Max Memory einstellt und die Defaults lässt.

*MaxValue 2147483647 MB use the dynamically memory management. From the total OS memory, reserve 1GB-4GB to the OS itself. For more information see on [Server memory configuration options](https://docs.microsoft.com/en-us/sql/database-engine/configure-windows/server-memory-server-configuration-options?view=sql-server-ver15)*

Mit den dbatools kann das Memory einfach geprüft und eingestellt werden:

```
# Gets the 'Max Server Memory' configuration setting and the memory of the server
Get-DbaMaxMemory  -SqlInstance $mssqlsrv

# Calculates the recommended value for SQL Server 'Max Server Memory' configuration setting
Test-DbaMaxMemory -SqlInstance $mssqlsrv

# Sets SQL Server 'Max Server Memory' configuration setting to a new value then displays information this setting
Set-DbaMaxMemory  -SqlInstance $mssqlsrv
```

### Backup, Copy, Restore

Backup einer Datenbank erstellen, Backupfile vom Container auf den Docker Host kopieren, Backupfile vom Docker Host auf einen neuen Container kopieren und Backup restoren.

#### Backup

Full-Backup erstellen.

```
Backup-DbaDatabase -SqlInstance $mssqlsrv -Path '/var/opt/mssql/backup' -Database 'TestingDB' -Type Full -IgnoreFileChecks

BackupComplete        : True
BackupFile            : TestingDB_202106020915.bak
BackupFilesCount      : 1
BackupFolder          : /var/opt/mssql/backup
BackupPath            : /var/opt/mssql/backup\TestingDB_202106020915.bak
DatabaseName          : TestingDB
Notes                 : 
Script                : BACKUP DATABASE [TestingDB] TO  DISK = N'/var/opt/mssql
                        /backup\TestingDB_202106020915.bak' WITH NOFORMAT, NOIN
                        IT, NOSKIP, REWIND, NOUNLOAD,  STATS = 1
. . .
```

#### Copy

Backup vom Container zum Docker Host kopieren.

```
$Backupfile = "TestingDB_202106020915.bak"
docker cp "mssqlsrv1:/var/opt/mssql/backup/$Backupfile" "D:\Temp\$Backupfile"
Get-Item "D:\backup\$Backupfile"

```

Backup vom Docker Host zum Container kopieren

```
$Backupfile = "tinu-20210601-19-33-13.bak"
docker cp "D:\Temp\$Backupfile" "mssqlsrv1:/var/opt/mssql/backup/$Backupfile"
```

#### Restore

Restore in die Datenbank.

```
$BackupPath = '/var/opt/mssql/backup/TestingDB_202106020915.bak'
Restore-DbaDatabase -SqlInstance $mssqlsrv -Path $BackupPath -DatabaseName $database -WithReplace

. . .
Script                 : {RESTORE DATABASE [TestingDB] FROM  DISK = N'/var/opt/
                         mssql/backup/TestingDB_202106020915.bak' WITH  FILE = 
                         1,  MOVE N'TestingDB' TO N'/var/opt/mssql/data/Testing
                         DB.mdf',  MOVE N'TestingDB_log' TO N'/var/opt/mssql/da
                         ta/TestingDB_log.ldf',  NOUNLOAD,  REPLACE,  STATS = 1
                         0}
BackupFileRaw          : /var/opt/mssql/backup/TestingDB_202106020915.bak
FileRestoreTime        : 00:00:01
DatabaseRestoreTime    : 00:00:01
ExitError              : 
. . .
```

### Import CSV

Wenn das CSV als neue Tabelle importiert werden soll, muss der Parameter -AutoCreateTable mitgegeben werden.

```
$DBname    = 'tinu'
$Table     = 'inventory'
$downloads = Join-Path $env:HOME -ChildPath downloads
$csv_file  = Join-Path $downloads -ChildPath 'MssqlBD.local.tinu.inventory.csv'
Import-DbaCsv -Path $csv_file -SqlInstance $mssqlsrv -Database $DBname -Table $Table -Delimiter ";" -NullValue "NULL" -AutoCreateTable #-Truncate

```

Wenn die Daten an eine bestehende Tabelle angehängt werden sollen, darf der Primary Key nicht mitgenommen werden. In diesem Fall müssen die zu importierenden Felder mitgegeben werden. Sind NULL-Values im CSV-file vorhanden, werden diese mit dem Parameter -NullValue und einem Standard-Wert (NULL) mitgegeben.

```
$column = @(
    'RunTime',
    'DeviceType',
    'DeviceName',
    'Physical cores'
)
Import-DbaCsv -Path $csv_file -SqlInstance $mssqlsrv -Database $DBname -Table $Table -Delimiter ";" -NullValue "NULL" -Column $column
```

### Export CSV

Export einer Tabelle als CSV-file. Das File kann für den Import in MssqlDB, MongoDB, etc. oder für die Weiterverarbeitung als Excel benutzt werden.

```
$DBname     = 'tinu'
$Table      = 'inventory'
$downloads  = Join-Path $env:USERPROFILE -ChildPath downloads
$Backupfile = Join-Path $downloads -ChildPath "$($DBname)-$($Table)-$(Get-Date -f 'yyyy-MM-dd_HH-mm-ss').csv"

$SqlQuery   = @"
SELECT * FROM [$DBname].[dbo].[$Table]
GO
"@  

ResultSqlQuery = Invoke-DbaQuery -SqlInstance $mssqlsrv -Database $DBname -Query $SqlQuery
$ResultSqlQuery | ConvertTo-Csv -Delimiter ';' -NoTypeInformation | Set-Content $Backupfile
```

### Import JSON

Importiert ein JSON-file in eine Tabelle. Wenn die Tabelle nicht existiert, wird sie mit ineffizienten Datentypen erstellt. Diese müssen nachträglich auf effiziente Datentypen geändert werden.

```
$DBname     = 'tinu'
$Table      = 'inventory'
$downloads  = Join-Path $env:HOME -ChildPath downloads
$json_file  = Join-Path $downloads -ChildPath 'MongoDB.local.tinu.inventory.json'
$columns = @(
    'RunTime','DeviceType','DeviceName','Physical cores','MemoryGB','DiskspaceGB','PurchaseDate','Price','Payment','Warranty','Link'
)
$dataset = Get-Content $json_file | ConvertFrom-Json | Select-Object $columns | ConvertTo-DbaDataTable
$dataset | Write-DbaDbTableData -SqlInstance $mssqlsrv -Database $DBname -Table $table -AutoCreateTable -KeepNulls -Truncate
```

Ein neuer Primary Key und Index muss ebenfalls erstellt werden (bitte das ' vor TABLE entfernen).

```
$DBname     = 'tinu'
$Table      = 'inventory'
$SqlQuery   = @"
ALTER 'TABLE [$DBname].[dbo].[$Table]
    ADD ID UNIQUEIDENTIFIER NOT NULL DEFAULT NEWSEQUENTIALID() PRIMARY KEY
GO
"@
Invoke-DbaQuery -SqlInstance $mssqlsrv -Database $DBname -Query $SqlQuery
```

### Export JSON

Export einer Tabelle als JSON-file. Das File kann für den Import in MssqlDB, MongoDB, etc. oder für Webservices benutzt werden.

```
$DBname     = 'tinu'
$Table      = 'inventory'
$downloads  = Join-Path $env:USERPROFILE -ChildPath downloads
$Backupfile = Join-Path $downloads -ChildPath "$($DBname)-$($Table)-$(Get-Date -f 'yyyy-MM-dd_HH-mm-ss').json"

$SqlQuery   = @"
SELECT * FROM [$DBname].[dbo].[$Table]
GO
"@  

$ResultSqlQuery = Invoke-DbaQuery -SqlInstance $mssqlsrv -Database $DBname -Query $SqlQuery
$ResultSqlQuery | ConvertTo-Json -Depth 1 | Set-Content $Backupfile
```

## References

[dbatools](https://dbatools.io/), [Transact-SQL](/wiki/transact-sql/), [MongoDB](/wiki/mongodb/)

