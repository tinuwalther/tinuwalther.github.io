---
layout: post
title:  "File Handling"
author: Tinu
categories: "PowerShell-Basic"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

## Table of Contents

- [Table of Contents](#table-of-contents)
  - [Define the Function](#define-the-function)
  - [Call the function](#call-the-function)
- [See also](#see-also)

### Define the Function

A function for some file-handling examples. First we see a parameter block with ValidateScript to ensure that a file has been specified. The type of this parameter must be a file. The second paramter is only a switch for the output.

````powershell
function Invoke-MwaFileReader {
    [CmdletBinding()]
    param(
        # Parameter block with ValidateScript and a custom message if the file not exists
        [Parameter(
            HelpMessage                     = 'Specify a valide fullname of a file to read.',    
            Mandatory                       = $true,
            ValueFromPipeline               = $true,
            ValueFromPipelineByPropertyName = $true,
            Position                        = 0
        )]
        [ValidateScript({ if(Test-Path -Path $($_) ){$true}else{Throw "File '$($_)' not found"} })]
        [System.IO.FileInfo]$file,

        # Only a switch for output or not
        [Parameter(Mandatory = $false)]
        [Switch]$Out
    )

    begin{
        $StartTime = Get-Date
        $function = $($MyInvocation.MyCommand.Name)
        Write-Verbose $('[', (Get-Date -f 'yyyy-MM-dd HH:mm:ss.fff'), ']', '[ Begin   ]', $function -Join ' ')
        $ret = $null
    }

    process{
        Write-Verbose $('[', (Get-Date -f 'yyyy-MM-dd HH:mm:ss.fff'), ']', '[ Process ]', $function -Join ' ')
        try{
            Write-Verbose "$($file)"
            switch -RegEx ($file.Extension -replace '\.'){
                'csv'  {
                    # if the file-extension is a csv, then you can use Import-Csv to read it as an object
                    Write-Verbose "Its a $($_)"
                    $ret = Import-Csv -Delimiter ';' -Path $file.FullName
                }
                'json' {
                    # if the file-extension is a json, then you can user Get-Content and | ConvertFrom-Json to read and format ist as an object
                    Write-Verbose "Its a $($_)"
                    $ret = Get-Content -Path $file.FullName | ConvertFrom-Json
                }
                default  {
                    # the default ist not defined and use Get-Content to read it
                    Write-Verbose "Its a $($_)"
                    $ret = Get-Content -Path $file.FullName
                }
            }
        }catch{
            Write-Warning $('ScriptName:', $($_.InvocationInfo.ScriptName), 'LineNumber:', $($_.InvocationInfo.ScriptLineNumber), 'Message:', $($_.Exception.Message) -Join ' ')
            $Error.Clear()
        }
    }

    end{
        Write-Verbose $('[', (Get-Date -f 'yyyy-MM-dd HH:mm:ss.fff'), ']', '[ End     ]', $function -Join ' ')
        $TimeSpan  = New-TimeSpan -Start $StartTime -End (Get-Date)
        $Formatted = $TimeSpan | ForEach-Object {
            '{1:0}h {2:0}m {3:0}s {4:000}ms' -f $_.Days, $_.Hours, $_.Minutes, $_.Seconds, $_.Milliseconds
        }
        Write-Verbose $('Finished in:', $Formatted -Join ' ')
        if($Out){ return $ret }
    }
}
````

### Call the function

We call the function with the named parameter file:

````powershell
Invoke-MwaFileReader -file "D:\github.com\PSXiDiag\data\inventory.csv" -Verbose
````

The file is a CSV and is importet as an objet with Import-Csv.

````powershell
VERBOSE: [ 2023-04-24 18:31:23.086 ] [ Begin   ] Invoke-MwaFileReader
VERBOSE: [ 2023-04-24 18:31:23.087 ] [ Process ] Invoke-MwaFileReader
VERBOSE: D:\github.com\PSXiDiag\data\inventory.csv
VERBOSE: Its a csv
VERBOSE: [ 2023-04-24 18:31:23.087 ] [ End     ] Invoke-MwaFileReader
VERBOSE: Finished in: 0h 0m 0s 001ms
````

````powershell
HostName         : ESXi7912.my.company.ch
Version          : 6.7
Manufacturer     : HPE
Model            : ProLiant DL380 Gen10
vCenterServer    : vCSA021.my.company.ch
Cluster          : Oracle
PhysicalLocation : Ost
ConnectionState  : Connected
````

Next we call the function with the parameter at position 0 for file:

````powershell
Invoke-MwaFileReader "D:\github.com\PSXiDiag\data\Inventory.json" -Verbose
````

The file is a JSON and is importet with Get-Content and formatet as object with ConvertFrom-Json.

````powershell
VERBOSE: [ 2023-04-24 18:31:28.611 ] [ Begin   ] Invoke-MwaFileReader
VERBOSE: [ 2023-04-24 18:31:28.611 ] [ Process ] Invoke-MwaFileReader
VERBOSE: D:\github.com\PSXiDiag\data\Inventory.json
VERBOSE: Its a json
VERBOSE: [ 2023-04-24 18:31:28.613 ] [ End     ] Invoke-MwaFileReader
VERBOSE: Finished in: 0h 0m 0s 002ms
````

````powershell
HostName         : ESXi7912.my.company.ch
Version          : 6.7
Manufacturer     : HPE
Model            : ProLiant DL380 Gen10
vCenterServer    : vCSA021.my.company.ch
Cluster          : Oracle
PhysicalLocation : Ost
ConnectionState  : Connected
````

Next we use the function with pipe the parameter for file:

````powershell
"D:\temp\words.txt" | Invoke-MwaFileReader -Verbose
````

The file is a Textfile and importet with Get-Content.

````powershell
VERBOSE: [ 2023-04-24 18:31:32.502 ] [ Begin   ] Invoke-MwaFileReader
VERBOSE: [ 2023-04-24 18:31:32.502 ] [ Process ] Invoke-MwaFileReader
VERBOSE: D:\temp\words.txt
VERBOSE: Its a txt
VERBOSE: [ 2023-04-24 18:31:32.510 ] [ End     ] Invoke-MwaFileReader
VERBOSE: Finished in: 0h 0m 0s 008ms
````

````powershell
Show-NetFirewallRule
Show-NetIPsecRule
Show-StorageHistory
Show-Tree
Show-VirtualDisk
Start-AppBackgroundTask
Start-AppvVirtualProcess
Start-AutologgerConfig
````

Next we call the function with a wrong file-path:

````powershell
Invoke-MwaFileReader "D:\NotExists.txt" -Verbose
````

The file does not exists and the ValidateScript-Block returned the custom-defined message.

````powershell
Invoke-MwaFileReader: Cannot validate argument on parameter 'file'. File 'D:\NotExists.txt' not found
````

Next we call the function with an empty file-path:

````powershell
Invoke-MwaFileReader -file 
````

We forgot the file-path and the type-definition in the paramter returned the default message.

````powershell
Invoke-MwaFileReader: Missing an argument for parameter 'file'. Specify a parameter of type 'System.IO.FileInfo' and try again.
````

Next we call the function with no parameter and type at the prompt for file '!?' to get the HelpMessage:

````powershell
Invoke-MwaFileReader # Type !? at the prompt for file
````

````powershell
cmdlet Invoke-MwaFileReader at command pipeline position 1
Supply values for the following parameters:
(Type !? for Help.)
file: !?
Specify a valide fullname of a file to read.
file:
````

## See also

[ValidateScript Attribute Declaration](https://learn.microsoft.com/en-us/powershell/scripting/developer/cmdlet/validatescript-attribute-declaration?view=powershell-7.3) on Microsoft.

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]
