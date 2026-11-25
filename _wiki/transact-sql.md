---
title: Transact-SQL
date: '2021-05-19T18:47:54+02:00'
author: Tinu
excerpt: In diesem Post zeige ich euch meine meist-genutzten TSQL-Statements. Diese
  Statements benutze ich in VSCode auf einem Linux SQL Docker Container.
categories:
- Datenbank
tags:
- MSSQL
- Scripting
- VSCode
image: /assets/wiki/MSSQL-e1620819331995.png
wordpress_id: 2958
layout: post
permalink: /wiki/transact-sql/
render_with_liquid: false
---

In diesem Post zeige ich euch meine meist-genutzten TSQL-Statements. Diese Statements benutze ich in VSCode auf einem Linux SQL Docker Container.

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

## Stored Procedures

### List all databases

```
EXEC sp_databases;
GO
```

### Check Database State

```
SELECT name
,create_date
,collation_name
,user_access
,state_desc
,recovery_model_desc
from sys.databases 
GO
```

## T-SQL Scripting

### Create database

Connect to the 'master' database to run this snippet

```
-- Create a new database called 'tinu'
USE master
GO
-- Create the new database if it does not exist already
IF NOT EXISTS (
    SELECT [name]
        FROM sys.databases
        WHERE [name] = N'tinu'
)
CREATE DATABASE tinu
GO
```

### Create table

Connect to the 'tinu' database to run this snippet

```
-- Create a new table called '[inventory]' in schema '[dbo]'
USE tinu;
GO
-- Create the table in the specified schema
CREATE TABLE [dbo].[inventory]
(
    [ID] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWSEQUENTIALID() PRIMARY KEY,
    [RunTime] DATETIME NOT NULL,
    [DeviceType] NVARCHAR(50) NOT NULL,
    [DeviceName] NVARCHAR(50) NOT NULL
    -- Specify more columns here
);
GO
```

### Insert rows

Connect to the 'tinu' database to run this snippet

```
-- Insert rows into table 'inventory' in schema '[dbo]'
USE tinu;
GO

INSERT INTO [dbo].[inventory]
( -- Columns to insert data into
 [RunTime], [DeviceType], [DeviceName]
)
VALUES
( -- First row: values for the columns in the list above
 GETDATE(), 'Convertable', 'Microsoft Surface'
),
( -- Second row: values for the columns in the list above
 GETDATE(), 'iMac', 'iMac Tinu'
)
-- Add more rows here
GO
```

### Update rows

Update rows with TimeStamp, DateTime, and Currency

```
-- Update rows in table 'Inventory'
DECLARE (at)datetime datetime = '2019-07-01'
UPDATE Inventory
SET
    [RunTime]        = GETDATE(),
    [Physical cores] = '4',
    [Memory]         = '16GB',
    [Disk]           = '500GB'
    [Purchase]       = (at)datetime,
    [Price]          = 2341.40
WHERE [DeviceType] LIKE 'iMac'
GO
```

### Remove rows

```
-- Delete rows from table 'Inventory'
DELETE FROM Inventory
WHERE [DeviceType] LIKE 'Convertable'
GO
```

### Insert new column

```
-- Add a new column 'NewColumnName' to table 'Inventory' in schema '[dbo]'
ALTER TABLE [dbo].[inventory]
    /*new_column_name new_column_datatype new_column_nullability*/
    ADD ID UNIQUEIDENTIFIER NOT NULL DEFAULT NEWSEQUENTIALID() PRIMARY KEY
GO
ALTER TABLE [dbo].[inventory]
    /*new_column_name new_column_datatype new_column_nullability*/
    ADD "Physical cores" NVARCHAR(50) NULL
GO
ALTER TABLE [dbo].[inventory]
    /*new_column_name new_column_datatype new_column_nullability*/
    ADD "Memory" NVARCHAR(50) NULL
GO
ALTER TABLE [dbo].[inventory]
    /*new_column_name new_column_datatype new_column_nullability*/
    ADD "Disk" NVARCHAR(50) NULL
GO
ALTER TABLE [dbo].[inventory]
    /*new_column_name new_column_datatype new_column_nullability*/
    ADD "Purchase" DATETIME NULL
GO
ALTER TABLE [dbo].[inventory]
    /*new_column_name new_column_datatype new_column_nullability*/
    ADD "Price" DECIMAL(20,2) NULL
GO
```

### Rename column

```
EXEC sp_rename 'dbo.inventory.Memory', 'MemoryGB', 'COLUMN';
EXEC sp_rename 'dbo.inventory.Disk', 'DiskspaceGB', 'COLUMN';
```

### Change the data type of a column

```
ALTER TABLE inventory
    ALTER COLUMN [Physical cores] INT NULL;
GO

ALTER TABLE inventory
    ALTER COLUMN MemoryGB INT NULL;
GO

ALTER TABLE inventory
    ALTER COLUMN DiskspaceGB INT NULL;
GO
```

### Create Primary Key

```
-- Change data type to int
ALTER TABLE inventory
    ALTER COLUMN [ID] INT NULL
GO

-- Change to value not null
ALTER TABLE inventory
    ALTER COLUMN [ID] INT NOT NULL
GO

-- Create the primary key
ALTER TABLE inventory
    ADD CONSTRAINT PK_Inventory_ID PRIMARY KEY CLUSTERED (ID)
GO
```

### Drop column

```
-- Drop 'ColumnName' from table 'TableName' in schema 'SchemaName'
ALTER TABLE [dbo].[inventory]
    DROP COLUMN ColumnName
GO
```

### Select Top

```
SELECT TOP (10) [ID]
      ,[RunTime]
      ,[DeviceType]
      ,[DeviceName]
  FROM [tinu].[dbo].[inventory]
  WHERE [RunTime] > '2021-05-19'
  ORDER BY [RunTime] DESC
```

### Remove table

Connect to the 'master' database to run this snippet

```
USE master
GO

-- Drop table 'inventory'
IF  EXISTS (
    SELECT * FROM sys.objects 
        WHERE object_id = OBJECT_ID(N'[dbo].[inventory]'
    ) 
    AND type in (N'U')
)
DROP TABLE [dbo].[inventory]
GO
```

### Get Diskspace

```
SELECT DISTINCT 
    CONVERT(CHAR(100), SERVERPROPERTY('Servername')) AS Server,
    volume_mount_point [Disk], 
    file_system_type [File System], 
    logical_volume_name as [Logical Drive Name], 
    CONVERT(DECIMAL(18,2),total_bytes/1073741824.0) AS [Total Size in GB], ---1GB = 1073741824 bytes
    CONVERT(DECIMAL(18,2),available_bytes/1073741824.0) AS [Available Size in GB],  
    CAST(CAST(available_bytes AS FLOAT)/ CAST(total_bytes AS FLOAT) AS DECIMAL(18,2)) * 100 AS [Space Free %] 
FROM sys.master_files 
CROSS APPLY sys.dm_os_volume_stats(database_id, file_id)
```

### Join two tables

```
-- Query LastPatchStatus and PoweredOffVMs
USE JupyterNB
GO

SELECT A.ID
    , A.LastRunTime
    , B.VMName
    , A.PSComputerName
    , A.LastPatchRun
    , A.LastPatchStatus
    , B.PowerState
    , B.PatchingWindow
    , A.Comment AS PatchComment
FROM LastPatchStatus A
LEFT JOIN PoweredOffVMs B on A.PSComputerName = B.ComputerName
WHERE B.PowerState IS NULL AND A.LastRunTime > '2021-05-02' --AND Comment IS NULL
ORDER BY PSComputerName
```

### Calculate some things

```
SELECT 
  COUNT(ID) AS 'Total rows'
  ,SUM([Physical cores]) AS 'Total Cores'
  ,SUM(MemoryGB) AS 'Total Memory'
  ,SUM(DiskspaceGB) AS 'Total Diskspace'
  ,SUM(Price) AS 'Total Costs'
FROM dbo.inventory
```

### Create a View

```
CREATE VIEW InventoryTotals
  AS 
SELECT 
  COUNT(ID) AS 'Total rows'
  ,SUM([Physical cores]) AS 'Total Cores'
  ,SUM(MemoryGB) AS 'Total Memory'
  ,SUM(DiskspaceGB) AS 'Total Diskspace'
  ,SUM(Price) AS 'Total Costs'
FROM dbo.inventory
```

## References

[SQL Tutorial](https://www.w3schools.com/sql/default.asp), [SQL Server Maintenance Solution](https://ola.hallengren.com/)

