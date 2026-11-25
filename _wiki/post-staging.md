---
title: HyperV Post-Staging
date: '2014-11-27T17:02:41+01:00'
author: Tinu
excerpt: Post-Staging Konfiguration eines Windows Servers mit PowerShell.
categories:
- Virtualisierung
- Windows Server
tags:
- Hyper-V
- Staging
image: /assets/wiki/hyperv-icon.png
wordpress_id: 207
layout: post
permalink: /wiki/post-staging/
render_with_liquid: false
---

# Post-Staging Konfiguration

Nachdem der virtuelle Computer angelegt ist, muss dieser noch Konfiguriert werden. Da wir nun schon Experten in PowerShell sind, lösen wir diese Aufgabe natürlich mit einem Script. 

## TCP/IP Konfiguration setzen

```
function Set-StaticIPAddress{
    <#
    .SYNOPSIS
        Set static IP Address
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][String] $InterfaceType,
        [Parameter(Mandatory=$true)][String] $Alias,
        [Parameter(Mandatory=$true)][String] $IPAddress
    )
    $function = $($MyInvocation.MyCommand.Name)
    try{
        $Interface = Get-NetIPAddress -IPAddress $IPAddress -ErrorAction Stop
        $exists = $true
    }
    catch{
        $exists = $false
    }
    if (!($exists)){
        $ret = New-NetIPAddress -InterfaceAlias $Alias -IPAddress $IPAddress -AddressFamily $InterfaceType -PrefixLength 24
        $ret = Get-NetIPAddress -AddressFamily $InterfaceType -InterfaceAlias $Alias
        $ret | % {
            Write-Host "InterfaceIndex $($_.InterfaceIndex), $($_.IPAddress)/$($_.PrefixLength), $($_.PrefixOrigin)/$($_.SuffixOrigin)"
        }
    }
}
```

---

```
function Set-DnsServers{
    <#
    .SYNOPSIS
        Set DNS Servers

    .DESCRIPTION
        Set the primary DNS Server IP
        Set the primary DNS Suffix
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][String] $InterfaceType,
        [Parameter(Mandatory=$true)][String] $Alias,
        [Parameter(Mandatory=$true)][String] $IPAddress
    )
    $function = $($MyInvocation.MyCommand.Name)
    $ret = Set-DnsClientServerAddress $Alias -ServerAddresses $IPAddress -PassThru
    Write-Host $($ret.ServerAddresses)
}
```

---

```
function Set-PrimaryDnsSuffix{
    <# .SYNOPSIS Set Primary Dns Suffix and DNS Suffix Search List #>
    [CmdletBinding()]
    param(
        $RegPath = 'HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\',
        $PrimaryDnsSuffix
    )
    $function = $($MyInvocation.MyCommand.Name)
    # Primary Dns Suffix
    $ret = Set-ItemProperty $RegPath -Name Domain -Value $DnsDomainName -PassThru
    "$(Get-Date -DisplayHint DateTime) [INFORMATION] $($function): Domain = $($ret.Domain)" | ` 
    Out-File -FilePath $script:Logfile -Append

    $ret = Set-ItemProperty $RegPath -Name 'NV Domain' -Value $DnsDomainName -PassThru
    "$(Get-Date -DisplayHint DateTime) [INFORMATION] $($function): NV Domain = $($ret.'NV Domain')" | ` 
    Out-File -FilePath $script:Logfile -Append

    # DNS Suffix Search List
    $ret = Set-DnsClientGlobalSetting -SuffixSearchList @($PrimaryDnsSuffix) -PassThru
    "$(Get-Date -DisplayHint DateTime) [INFORMATION] $($function): $($ret.SuffixSearchList)" | ` 
    Out-File -FilePath $script:Logfile -Append
}
```

## Computer umbenennen

```
function Set-ComputerName{
    <# .SYNOPSIS Set new ComputerName, Reboot required #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][String] $NewName
    )
    $function = $($MyInvocation.MyCommand.Name)
    if ($env:COMPUTERNAME.ToLower() -ne $NewName.ToLower()){
        try{
            $ret = Rename-Computer -NewName $NewName -PassThru -Verbose
            "$(Get-Date -DisplayHint DateTime) [INFORMATION] $($function): $($ret.HasSucceeded)" | ` 
             Out-File -FilePath $script:Logfile -Append
            if($ret.HasSucceeded){
                "$(Get-Date -DisplayHint DateTime) [INFORMATION] $($function): from $($ret.OldComputerName) to $($ret.NewComputerName)" | ` 
                 Out-File -FilePath $script:Logfile -Append
            }
            else{
                "$(Get-Date -DisplayHint DateTime) [  WARNING  ] $($function): from $($ret.OldComputerName) to $($ret.NewComputerName)" | ` 
                  Out-File -FilePath $script:Logfile -Append
            }
            return $ret.HasSucceeded
        }
        catch [Exception]{
            "$(Get-Date -DisplayHint DateTime) [   ERROR   ] $($function): $($_.Exception.Message)" | ` 
             Out-File -FilePath $script:Logfile -Append
            $error.Clear()
            return $false
        }
    }
}
```

## Computer in Domain aufnehmen

```
function Set-Domain{
    <# .SYNOPSIS Set local computer to a domain, Reboot required #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][String] $NewName
    )
    $function = $($MyInvocation.MyCommand.Name)
    try{
        $ret = Add-Computer -DomainName $NewName -Credential (Get-Credential -Message 'User-credentials with Domain-join Rights') -PassThru -Verbose
        "$(Get-Date -DisplayHint DateTime) [INFORMATION] $($function): $($ret.HasSucceeded)" | ` 
         Out-File -FilePath $script:Logfile -Append
        return $ret.HasSucceeded
    }
    catch [Exception]{
        "$(Get-Date -DisplayHint DateTime) [   ERROR   ] $($function): $($_.Exception.Message)" | ` 
         Out-File -FilePath $script:Logfile -Append
        $error.Clear()
        return $false
    }
}
```

## Windows aktivieren

```
function Activate-Windows{
    <#
    .SYNOPSIS
        Activate Windows

    .DESCRIPTION
        Internetconnection needed
    #>
    [CmdletBinding()]
    param(
        $LicenseKey = "XXXXX-XXXXX-XXXXX-XXXXX-XXXXX"
    )
    $function = $($MyInvocation.MyCommand.Name)
    $computer = $env:computername
    $service = get-wmiObject -query "select * from SoftwareLicensingService" -computername $computer
    $service.InstallProductKey($LicenseKey)
    $service.RefreshLicenseStatus()
    #LogInfo -Function $function -Message $($ret.ServerAddresses) -info
}
```

## Administrator umbenennen

```
function Set-LocalAdmin{
    <#
    .SYNOPSIS
        Set LocalAdmin
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][String] $password
    )
    $function = $($MyInvocation.MyCommand.Name)
    try{
        $user = Get-WMIObject Win32_UserAccount -Filter "Name='Administrator'"
        $user.Rename('Admin')
        $ret = Get-WMIObject Win32_UserAccount -Filter "Name='Admin'"
        Write-Host "User renamed to $($ret.Name)"
        net user Admin $password
    }
    catch{
        Write-Host "User not exists"
    }
}
```

Und als Abschluss, wird der Server noch neu gestartet. Somit haben wir einen brauchbaren Windows Server bereitgestellt. Nun kann damit ein Active Directory Forest aufgebaut und mit dem nächsten Server dann z.B. ein SharePoint Server installiert werden usw. Doch dazu gibts wieder eigene Beiträge.