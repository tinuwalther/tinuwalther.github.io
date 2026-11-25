---
title: XML Manipulationen
date: '2016-08-30T21:30:38+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Hashtable
- XML
wordpress_id: 1564
layout: post
permalink: /wiki/xml-manipulationen/
render_with_liquid: false
---

## Read XML Data

 Daten aus einem XML-File auslesen und als Hashtable zurückgeben: 

```
function Get-XmlData{
    <# Read XML data and return a hashtable #>
    [CmdletBinding()]
    param(
        $file,
        $xpath
    )

    $ret = @()
    [xml]$xml   = (Get-Content $file)
    $objxmldata = $xml.SelectNodes($xpath)

    #Load data to an xmlobject
    foreach($item in $objxmldata){
        $ret += @{Date="$($item.year)-$($item.month)-$($item.day)"}
    }
    return $ret
}
Get-XmlData -file 'C:\XML\config.xml' -xpath '/info/thing/dataxml/weight/when/date' -Verbose
```

 Output: 

```csharp
Name                           Value
----                           -----
Date                           2012-5-23
Date                           2012-5-22
Date                           2012-5-21
```

## Change XML Data

 Daten aus einem XML-File auslesen undbestimmte Werte ändern: 

```
function Set-XmlData{
    <# Change a value and save it back to the xml-file #>
    [CmdletBinding()]
    param(
        $file,
        $xpath
    )

    [xml]$xml   = (Get-Content $file)
    $objxmldata = $xml.SelectNodes($xpath)

    #Load data to an xmlobject
    foreach($item in $objxmldata){
        Write-Verbose "$($item.year)-$($item.month)-$($item.day)"
        $item | Where-Object {
            if($item.day -eq 23){
                $item.day = '20'
            }
        }
    }

    #Save back to the xml-file
    $xml.Save($file)
}
Set-XmlData -file 'C:\XML\config.xml' -xpath '/info/thing/dataxml/weight/when/date' -Verbose
```

## The XML-File

 Und das ist das XML-File: 

```csharp
`<info>  <thing>    <dataxml>      <weight>        <when>          <date>            <year>2012</year>            <month>5</month>            <day>23</day>          </date>          <date>            <year>2012</year>            <month>5</month>            <day>22</day>          </date>          <date>            <year>2012</year>            <month>5</month>            <day>21</day>          </date>        </when>      </weight>    </dataxml>  </thing></info>` 
```

## Export Object as XML

 Ein Objekt in ein XML-File abspeichern: 

```
[PSCustomObject]@{
     OSName    = 's321456'
     OSVersion = 'Windows Server 2012-R2'
     Customer  = 'Swisscom (Schweiz) AG'
} | Export-Clixml -Path .\Test.xml
```

## The XML-File

 Das XML-File nach dem Speichern: 

```csharp
<Objs Version="1.1.0.1" xmlns="http://schemas.microsoft.com/powershell/2004/04">
    <Obj RefId="0">
        <TN RefId="0">
            <T>System.Management.Automation.PSCustomObject</T>
            <T>System.Object</T>
        </TN>
        <MS>
            <S N="OSName">s321456</S>
            <S N="OSVersion">Windows Server 2012-R2</S>
            <S N="Customer">Customer AG</S>
            <MS N="Disks">
                <S N="Disk1">C</S>
                <S N="Disk2">D</S>
                <S N="Disk3">E</S>
                <S N="Disk4">F</S>
            </MS>
            <MS N="IPAddresses">
                <S N="Production">192.168.1.2</S>
                <S N="Backup">1.2.3.4</S>
            </MS>
        </MS>
    </Obj>
</Objs>
```

## Read from XML-File

 Und dann wollen wir es wieder einlesen und ausgeben: 

```
[xml]$xml  = (Get-Content .\Test.xml)
$xmlObject = $xml.Objs.Obj.MS.ChildNodes
foreach($item in $xmlObject)
{
    switch ($item.N)
    {
        'OSName'
        {
            # Hashtable
            $OSName = @{$item.N = $item.'#text'}
        }
        'OSVersion'
        {
            # Hashtable
            $OSVersion = @{$item.N = $item.'#text'}
        }
        'Customer'
        {
            # Hashtable
            $Customer = @{$item.N = $item.'#text'}
        }
        'Disks'
        {
            for ($i = 0; $i -lt ($item.S.N.count); $i++){
                write-host "$($item.S.N[$i]) $($item.S.'#text'[$i])"
            }
            ''
            # Hashtable
            $Disks = @{$item.S.N = $item.S.'#text'}
        }
        'IPAddresses'
        {
            for ($i = 0; $i -lt ($item.S.N.count); $i++){
                write-host "$($item.S.N[$i]) $($item.S.'#text'[$i])"
            }
            ''
            # Hashtable
            $IPAddresses = @{$item.S.N = $item.S.'#text'}
        }
        default {
            "$($item.N) not implemented yet"
        }
    }
}
$OSName.OSName
''
$OSName
$OSVersion
$Customer
$Disks
$IPAddresses
Remove-Variable * -ErrorAction SilentlyContinue
```