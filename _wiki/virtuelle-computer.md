---
title: HyperV VMs
date: '2014-11-27T16:53:51+01:00'
author: Tinu
excerpt: Neue virtuelle Computer auf Basis eines Images mit PowerShell erstellen.
categories:
- Virtualisierung
- Windows Server
tags:
- Hyper-V
- Staging
image: /assets/wiki/hyperv-icon.png
wordpress_id: 203
layout: post
permalink: /wiki/virtuelle-computer/
render_with_liquid: false
---

# Neue virtuelle Computer

Nachdem das Basisimage erstellt und mit einem Schreibschutz versehen worden ist, können nun neue virtuelle Computer auf diesem Image basierend angelegt werden. 

### Manuelle Variante

Wenn Sie nun einen neuen virtuellen Computer erstellen, wählen Sie bei *virtuelle Festplatte verbinden* die Option *virtuelle Festplatte später zuordnen* und führen Sie den Assistenten wie gewohnt zu Ende. Wenn die virtuelle Maschine erstellt wurde, wechseln Sie in die Eigenschaften des virtuellen Computers und fügen eine neue virtuelle Festplatte hinzu. Wählen Sie als Datenträgertyp *Differenzierend*, geben Sie der neuen virtuellen Festplatte einen Namen und wählen Sie im nächsten Schritt die **übergeordnete Festplatte** an. Dies ist unser Basisimage mit dem Schreibschutz. 

### PowerShell-Code

Wie Sie sich schon denken können, kann das Anlegen von neuen virtuellen Computern mit PowerShell automatisiert werden. Die neuen virtuellen Computer werden mit einem sogenannten Pre-Staging Script angelegt. Hier der Auszug der Function CreateNewVMGuest: 

```csharp
function CreateNewVMGuest{
    <#
    .SYNOPSIS
        CreateNewVM
    #>
    param(
        [Parameter(Mandatory=$true)][String] $VmName,
        [Parameter(Mandatory=$true)][String] $Memory,
        [Parameter(Mandatory=$true)][String] $VmSwitch,
        [Parameter(Mandatory=$true)][String] $BaseImage,
        [Parameter(Mandatory=$true)][String] $VHdxPath
    )
    $function = $($MyInvocation.MyCommand.Name)
    try{    
        $ret = Get-VM -Name $VmName -ErrorAction Stop
        Write-Host $ret
        $exists = $true
   }
    catch{
        $exists = $false
    }

    if ($exists){
        Write-Host "VM-Guest $($VmName) already exists"
    }
    else{
        Write-Host "Creating VM-Guest $($VmName)"
        $ret = New-VM $VmName -ComputerName $env:COMPUTERNAME -MemoryStartupBytes $Memory -NoVHD -SwitchName $VmSwitch
        Write-Host "$($ret.Name), $($ret.State), $($ret.Status)"
        if (Test-Path "$($VHdxPath)\$($VmName)-system.vhdx"){
            Write-Host "$($VHdxPath)\$($VmName)-system.vhdx already exists"
        }
        else{
            $ret = New-VHD -ParentPath $BaseImage -Path "$($VHdxPath)\$($VmName)-system.vhdx" -ComputerName $env:COMPUTERNAME -Differencing
            Write-Host "$($VmName), $($ret.path), $($ret.VhdFormat), $($ret.VhdType)"
        }
        $ret = Add-VMHardDiskDrive -VMName $VmName -ControllerLocation 1 -ControllerNumber 0 -ControllerType 'IDE' -Passthru -Path "$($VHdxPath)\$($VmName)-system.vhdx"
        Write-Host "$($ret.VMName), $($ret.ControllerType), $($ret.ControllerNumber), $($ret.ControllerLocation)"

        $ret = Start-VM -Name $VmName -Passthru
        Write-Host "$($ret.Name), $($ret.State), $($ret.Status)"
        vmconnect.exe $env:COMPUTERNAME $VmName
    }
}
CreateNewVMGuest -VmName vm1456 -Memory "1GB" -VmSwitch "Internal HyperV" -BaseImage "D:\HyperV\Appliance\BasicImage.vhdx" -VHdxPath "D:\HyperV\VHD"

```

Mit New-VHD wird eine neue VM basieren auf dem Basisimage und der Option "Virtuelle Festplatte später zuordnen" und mit dem Datenträgertyp "Differenzierend" erstellt. Mit Add-VMHardDiskDrive wird diese Disk der VM angehängt und mit Start-VM wird der neue virtuelle Computer gestartet. Weiter geht es mit der [Konfiguration ](/wiki/post-staging/ "Post-Staging")des neuen virtuellen Computers.