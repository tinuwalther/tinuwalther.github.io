---
title: Get Disks
date: '2015-02-04T16:19:42+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Disk
- PSObject
- Remote Commands
wordpress_id: 614
layout: post
permalink: /wiki/getdisks/
render_with_liquid: false
---

Arbeiten mit Disks, Volumes und Partitions per PowerShell.

## Get-Member

 Alle Properties und Methods der wichtigsten WMI-Objects von Disks, Volumes und Partitions auflisten (funktioniert natürlich mit allen anderen Cmdlets auch). 

```csharp
Get-WmiObject Win32_logicaldisk | gm

```

```csharp
Get-WmiObject Win32_Volume | gm
```

```csharp
Get-WmiObject Win32_DiskPartition | gm
```

```csharp
Get-WmiObject Win32_DiskDrive | gm
```

```csharp
Get-WmiObject Win32_MappedLogicalDisk | gm
```

## Diskspace auslesen

 Remote per PowerShell rasch die Disks von mehreren Servern auslesen - kein Problem. 

```csharp
function GetDisks{
    param (
        [Parameter(Mandatory=$true)][String] $Computer
    )
    # DeviceID, MediaType, TotalSize, FreeSize, Percent
	$ret = @()
	Get-WmiObject Win32_logicaldisk -ComputerName $Computer | where {$_.MediaType -eq 12} | %{
		$obj = New-Object PSObject
		$size = $([math]::round($_.size/1gb))
		$free = $([math]::round($_.freespace/1gb))
		$percent = $([math]::round(($free*100) / ($size)))
		Add-Member -InputObject $obj -MemberType NoteProperty -Name DeviceID -Value $_.DeviceID
		Add-Member -InputObject $obj -MemberType NoteProperty -Name "Size(GB)" -Value $size
		Add-Member -InputObject $obj -MemberType NoteProperty -Name "Free Space(GB)" -Value $free
		Add-Member -InputObject $obj -MemberType NoteProperty -Name "Free (%)" -Value $percent
		$ret += $obj
	}
	return $ret
}
$computers = @("Server1","Server2","Server3")
cls
$computers | %{
    $_
    GetDisks -Computer $($_) | ft -auto
}
```

## Freie Laufwerksbuchstaben auflisten

 Alle freien Laufwerksbuchstaben auflisten. A und B waren frührer mal Diskettenlaufwerke und C ist standardmässig das System. Diese Buchstaben werden gra nicht erst abgefragt. 

```csharp
ls function:[d-z]: -n | where-object{ !(test-path $_) }

```

 Mit dem Parameter -Last 1 wird der letzte freie Laufwerksbuchstabe ausgegeben. 

```csharp
ls function:[d-z]: -n | where-object{ !(test-path $_) } | Select -Last 1
```