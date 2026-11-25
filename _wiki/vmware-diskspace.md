---
title: VMware Diskspace
date: '2016-06-21T19:18:00+02:00'
author: Tinu
excerpt: Mit PowerCLI auf die VIServer verbinden und den Diskspcae einer VM vergrössern
  ohne RDP-Login auf das Guest OS.
categories:
- Virtualisierung
tags:
- PowerCLI
- VMware
image: /assets/wiki/vmware-e1620821111224.png
wordpress_id: 1478
layout: post
permalink: /wiki/vmware-diskspace/
render_with_liquid: false
---

Mit PowerCLI den Diskspace vergössern ohne RDP-Login auf das Guest OS.

## List Disks

Alle Disks der VM auflisten.

```
function Get-VMHarddisk{
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [String]$VMName,

        [Parameter(Mandatory = $false)]
        [Switch]$Out = $false
    )
    $function = $($MyInvocation.MyCommand.Name)
    Write-Verbose "Running $function"

    $ret = $null
    $guest  = Get-VM -Name "$($search)*" 
    if([String]::IsNullOrEmpty($guest)){
        Write-Output "Could not find a guest with name $($search)"
    }
    else{
        try{ 
            Write-Output "Found a guest with name $($guest.name)"
            $guest_disks = Get-HardDisk -vm $guest | Select-Object Parent,Name,CapacityGB 
            $ret = $guest_disks
            if($out){
                $guest_disks | Format-Table -AutoSize
            }
        }
        catch{
            Write-Verbose "Error on $($guest.name): $($_.Exception.Message)"
            $error.Clear()
        }
    }
    return $ret
}
```

## Extend Disksize

Disk erweitern.

```
function Resize-VMHarddisk{
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [String]$VMName,

        [Parameter(Mandatory = $true)]
        [String]$VMDisk,

        [Parameter(Mandatory = $true)]
        [int]$NewCapacityGB
    )
    $function = $($MyInvocation.MyCommand.Name)
    Write-Verbose "Running $function"

    $guest  = Get-VM -Name "$($search)*" 
    if([String]::IsNullOrEmpty($guest)){
        Write-Output "Could not find a guest with name $($search)"
    }
    else{
        try{ 
            Write-Output "Found a guest with name $($guest.name)"
            $guest_harddisk = Get-HardDisk -VM $guest | Where-Object {$_.Name -like $VMDisk}
    
            if([String]::IsNullOrEmpty($VMDisk)){
                Write-Output "Could not found any disk with name $($VMDisk)"
            }else{
                $guest_domain = ($guest.name).Split('.')[1]
                $guest_cred   = Get-Credential -Message "Enter the Guest-OS Credentials for $($guest)" -UserName "$($guest_domain.ToUpper())\$($env:USERNAME)"
                if([string]::IsNullOrEmpty($guest_cred)){
                    Write-Output "Aborted by $($env:USERNAME)"
                }else{
                    Set-HardDisk -HardDisk $guest_harddisk -CapacityGB $NewCapacityGB -ResizeGuestPartition -GuestCredential $guest_cred | Out-Null
                    Get-HardDisk -vm $guest | Select-Object Parent,Name,CapacityGB | Format-Table -AutoSize
                }
            }
        }
        catch{
            Write-Verbose "Error on $($guest.name): $($_.Exception.Message)"
            $error.Clear()
        }
    }
}
```

## Aufruf der Functions

```
Write-Output 'Connect to VI Server'
Connect-VIServer -Server VIServer1, VIServer2

$search = Read-Host 'Enter the Name of the Guest to search'
Write-Output 'Resize Disk ...'
Get-VMHarddisk -VMName $search
$disktoresize = Read_host 'Enter the disk to resize'
Resize-VMHarddisk -VMName $search -VMDisk $disktoresize -NewCapacityGB 120

Write-Output "Resize finished."
```

