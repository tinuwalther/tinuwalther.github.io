---
title: Web Server Class
date: '2017-12-10T13:13:50+01:00'
author: Tinu
excerpt: Einen IIS Webserver mit PowerShell auf Windows Server installieren.
categories:
- PowerShell
- Webserver
tags:
- Class
- IIS
image: /assets/wiki/powershell-1.png
wordpress_id: 2413
layout: post
permalink: /wiki/web-server-class/
render_with_liquid: false
---

## Web Server IIS 10

Webserver mit PowerShell auf Windows Server 2016 installieren (Beta Version): <div>

```
<#

    .SYNOPSIS
       Installation and configuration of a IIS Webserver v10

    .DESCRIPTION
       Installation and configuration of a IIS Webserver on Windows Server 2016

    .NOTES
       Author: Martin Walther
       Date created: 17.10.2017
       Version: 1.0.0.00005

#>

class PSWinFeatures{

    <#

       .SYNOPSIS
            Manipulate WindowsFeatures

       .DESCRIPTION
            Get-WindowsFeatures installed | all
            Install-WindowsFeatures @(FeatureList)
            Remove-WindowsFeatures  @(FeatureList)
    
    #>
        
    hidden [object] $WindowsFeatures   = $null
        
    [object] $Success                  = $null
    [object] $ExitCode                 = $null
    [object] $RestartNeeded            = $null
    [object] $FeatureResult            = $null
    [object] $ClassError               = $null
    
    WinFeatures([bool]$installed){
        $this.WindowsFeatures = [PSWinFeatures]::GetWindowsFeatures($installed)    
    }
        
    [object]static GetWindowsFeatures([bool]$installed){
        $Error.Clear()
        Import-Module ServerManager
        if ($installed){
            return Get-WindowsFeature | Where-Object InstallState -like installed | Select-Object Name, DisplayName, InstallState
        }
        else{
            return Get-WindowsFeature | Select-Object Name, DisplayName, InstallState
        }
    }
        
    [object]static InstallWindowsFeatures([object]$Features,[String]$Logfile){
        $Error.Clear()
        Import-Module ServerManager
        $ret     = @{}
        $install = $null
        foreach($item in $Features){
            try{
                $install = Add-WindowsFeature -name $item -LogPath $Logfile -WarningAction SilentlyContinue -ErrorAction Stop
            }
            catch{
                $ret.ClassError += @{"Error[$($item)]"=$($_.Exception.Message)}
                $Error.Clear()
            }
            if(-not([string]::IsNullOrEmpty($install))){
                $ret.Success       += @{$($item)=$($install.Success)}
                $ret.ExitCode      += @{$($item)=$($install.ExitCode)}
                $ret.RestartNeeded += @{$($item)=$($install.RestartNeeded)}
                $ret.FeatureResult += @{$($item)=$($install.FeatureResult)}
            }
        }
        return $ret        
    }
       
    [object]static RemoveWindowsFeatures([object]$Features){
        $Error.Clear()
        Import-Module ServerManager
        $ret     = @{}
        $remove  = $null
        foreach($item in $Features){
            $remove = Remove-WindowsFeature -name $item -WarningAction SilentlyContinue -ErrorAction SilentlyContinue
            if($Error){
                for ($i = 0; $i -lt $Error.Count; $i++){
                    $ret.ClassError += @{"Error[$($item)]"=$error[$i].Exception}
                }
                $Error.Clear()
            }
            if(-not([string]::IsNullOrEmpty($remove))){
                $ret.Success       += @{$($item)=$($remove.Success)}
                $ret.ExitCode      += @{$($item)=$($remove.ExitCode)}
                $ret.RestartNeeded += @{$($item)=$($remove.RestartNeeded)}
                $ret.FeatureResult += @{$($item)=$($remove.FeatureResult)}
            }
        }
        return $ret
    }
        
}

class PSWebServer{

    <#

       .SYNOPSIS
            Configure WebServer

       .DESCRIPTION
            Create-WebServerDirecory
            Set-WebManagementService
            Remove-DefaultWebsite
            Remove-DefaulApplicationPool
            Set-ApplicationPoolDefaults
            Create-DefaultWebsite

    #>
        
    [object]$WebserverDirectory      = $null
    [object]$WebManagementService    = $null
    [object]$DefaultWebsite          = $null
    [object]$DefaulApplicationPool   = $null
    [object]$ApplicationPoolDefaults = $null
    [object]$ClassError              = $null
    
    PSWebServer(){
    }
        
    [object]static CreateWebServerDirecory([hashtable]$WebServerVar){
        $Error.Clear()
        Import-Module WebAdministration
        $ret = @{}

        #region purge acl
        #$ret.Acls += cacls $($WebServerVar.WebServerDrive) /E /R Users "CREATOR OWNER" Everyone
        #endregion

        if(Test-Path -Path $($WebServerVar.WebServerRootPath)){
            $ret.$($WebServerVar.WebServerRootPath) = 'already exists'
        }
        else{
            $ret.$($WebServerVar.WebServerRootPath) = if(New-Item -Path $WebServerVar.WebServerRootPath -type directory -Force -ErrorAction SilentlyContinue){'created'}else{$false}
        }
        if(Test-Path -Path $($WebServerVar.DefaultWebSitePath)){
            $ret.$($WebServerVar.DefaultWebSitePath) = 'already exists'
        }
        else{
            $ret.$($WebServerVar.DefaultWebSitePath) = if(New-Item -Path $WebServerVar.DefaultWebSitePath -type directory -Force -ErrorAction SilentlyContinue){'created'}else{$false}
        }
        if(Test-Path -Path $($WebServerVar.WebSiteLogPath)){
            $ret.$($WebServerVar.WebSiteLogPath) = 'already exists'
        }
        else{
            $ret.$($WebServerVar.WebSiteLogPath) = if(New-Item -Path $WebServerVar.WebSiteLogPath -type directory -Force -ErrorAction SilentlyContinue){'created'}else{$false}
        }
        if(Test-Path -Path $($WebServerVar.WmsvcPath)){
            $ret.$($WebServerVar.WmsvcPath)  = 'already exists'
        }
        else{
            $ret.$($WebServerVar.WmsvcPath)  = if(New-Item -Path $WebServerVar.WmsvcPath -type directory -Force -ErrorAction SilentlyContinue){'created'}else{$false}
        }

        #region set acl
        #$ret.Acls += cacls $($WebServerVar.DefaultWebSitePath) /E /G IUSR:R IIS_IUSRS:R "NT Service\WMSVC:F"
        #endregion 

        if($Error){
            for ($i = 0; $i -lt $Error.Count; $i++){
                $ret.ClassError += @{"Error[CreateWebServerDirecory]"=$error[$i].Exception}
            }
            $Error.Clear()
        }
        return $ret
    }
    
    [object]static RemoveWebServerDirecory([hashtable]$WebServerVar){
        $Error.Clear()
        Import-Module WebAdministration
        $ret = @{}
        if(Test-Path -Path $($WebServerVar.WebServerRootPath)){
            $ret.$($WebServerVar.WebServerRootPath) = if(Remove-Item -Path $WebServerVar.WebServerRootPath -Recurse -Force -ErrorAction SilentlyContinue){$true}else{'deleted'}
        }
        if(Test-Path -Path $($WebServerVar.DefaultWebSitePath)){
            $ret.$($WebServerVar.DefaultWebSitePath) = if(Remove-Item -Path $WebServerVar.DefaultWebSitePath -Recurse -Force -ErrorAction SilentlyContinue){'created'}else{$false}
        }
        if(Test-Path -Path $($WebServerVar.WebSiteLogPath)){
            $ret.$($WebServerVar.WebSiteLogPath)    = if(Remove-Item -Path $WebServerVar.WebSiteLogPath -Recurse -Force -ErrorAction SilentlyContinue){$true}else{'deleted'}
        }
        if(Test-Path -Path $($WebServerVar.WmsvcPath)){
            $ret.$($WebServerVar.WmsvcPath)         = if(Remove-Item -Path $WebServerVar.WmsvcPath -Recurse -Force -ErrorAction SilentlyContinue){$true}else{'deleted'}
        }
        if($Error){
            for ($i = 0; $i -lt $Error.Count; $i++){
                $ret.ClassError += @{"Error[RemoveWebServerDirecory]"=$error[$i].Exception}
            }
            $Error.Clear()
        }
        return $ret
    }
    
    [object]static SetWebManagementService($Service){
        $Error.Clear()
        $ret = @{}
        #Get-WmiObject win32_service | where name -eq 'WMSVC'
        $InstallArgs = @{}
        $InstallArgs.FilePath     = "$($env:SystemRoot)\System32\sc.exe"
        $InstallArgs.ArgumentList = @()
        $InstallArgs.ArgumentList += "config $($Service)"
        $InstallArgs.ArgumentList += "start=delayed-auto"
        $InstallArgs.WindowStyle  = 'Hidden'
        $InstallArgs.Wait         = $true
        $ret.Service              = $($Service)
        $ret.StartType = "delayed-auto (RC $((Start-Process @InstallArgs -PassThru).ExitCode))"
        $null = (Start-service $($Service))
        $ret.Status    = (Get-Service $($Service)).Status
        if($Error){
            for ($i = 0; $i -lt $Error.Count; $i++){
                $ret.ClassError += @{"Error[SetWebManagementService]"=$error[$i].Exception}
            }
            $Error.Clear()
        }
        return $ret
    }
        
    [object]static RemoveDefaultWebsite($WebServerVar){
        $Error.Clear()
        $ret = @{}
        if(Get-Website -Name $WebServerVar.DefaultWebSite){
            $ret.DefaultWebSite += (Stop-Website -name $WebServerVar.DefaultWebSite -Passthru).State
            $ret.DefaultWebSite += Remove-Website -name $WebServerVar.DefaultWebSite
        }
        if(Test-Path -Path "$($WebServerVar.DefaultWebSitePath)\index.htm"){
            Remove-Item -Path "$($WebServerVar.DefaultWebSitePath)\index.htm" -Force
        }
        if($Error){
            for ($i = 0; $i -lt $Error.Count; $i++){
                $ret.ClassError += @{"Error[RemoveDefaultWebsite]"=$error[$i].Exception}
            }
            $Error.Clear()
        }
        return $ret
    }
    
    [object]static RemoveDefaulApplicationPool($WebServerVar){
        $Error.Clear()
        $ret = @{}
        $ret.AppPool += (Stop-WebAppPool -Name $WebServerVar.DefaultAppPool -Passthru).State
        $ret.AppPool += (Remove-WebAppPool -name $WebServerVar.DefaultAppPool)
        if($Error){
            for ($i = 0; $i -lt $Error.Count; $i++){
                $ret.ClassError += @{"Error[RemoveDefaulApplicationPool]"=$error[$i].Exception}
            }
            $Error.Clear()
        }
        return $ret
    }
    
    [object]static SetApplicationPoolDefaults($WebServerVar){
        $Error.Clear()
        $ret = @()
        [int]$physicalMemory = [math]::Round((((Get-WmiObject -Class Win32_ComputerSystem).TotalPhysicalMemory)/1kb)*0.8)
        
        $AppPoolDefaults = '/system.applicationHost/applicationPools/applicationPoolDefaults'

        Set-WebConfigurationProperty "/system.applicationHost/sites/siteDefaults" -name logfile.directory -value $WebServerVar.WebSiteLogPath
        $ret += Get-webconfigurationproperty "/system.applicationHost/sites/siteDefaults" -name logfile.directory | Select-Object name,value
        $RegPath = "HKLM:\SOFTWARE\Microsoft\WebManagement\Server"
        New-ItemProperty -Path $RegPath -Name LoggingDirectory -PropertyType String -Value $WebServerVar.WmsvcPath -Force
        New-ItemProperty -Path $RegPath -Name EnableRemoteManagement -PropertyType DWORD -Value 1 -Force
        
        Set-webconfigurationproperty $($AppPoolDefaults) -name queueLength -value 9000
        $ret += Get-webconfigurationproperty $($AppPoolDefaults) -name queueLength | Select-Object name,value

        Set-webconfigurationproperty "$($AppPoolDefaults)/recycling" -name logEventOnRecycle -value 255
        #$ret += Get-webconfigurationproperty $($AppPoolDefaults)/recycling -name logEventOnRecycle | Select-Object name,value

        Set-webconfigurationproperty "$($AppPoolDefaults)/recycling/periodicRestart" -name time -value 0.00:00:00
        $ret += Get-webconfigurationproperty "$($AppPoolDefaults)/recycling/periodicRestart" -name time | Select-Object name,value
        
        Set-webconfigurationproperty "$($AppPoolDefaults)/recycling/periodicRestart" -name memory -value $physicalMemory
        $ret += Get-webconfigurationproperty "$($AppPoolDefaults)/recycling/periodicRestart" -name memory | Select-Object name,value
        
        Remove-webconfigurationproperty "$($AppPoolDefaults)/recycling/periodicRestart/schedule" -name '.'
        
        Set-webconfigurationproperty "$($AppPoolDefaults)/processModel" -name idleTimeout -value 06:00:00
        $ret += Get-webconfigurationproperty "$($AppPoolDefaults)/processModel" -name idleTimeout | Select-Object name,value
        
        Set-webconfigurationproperty "$($AppPoolDefaults)/processModel" -name pingResponseTime -value 00:00:10
        $ret += Get-webconfigurationproperty "$($AppPoolDefaults)/processModel" -name pingResponseTime | Select-Object name,value
        
        Set-webconfigurationproperty "$($AppPoolDefaults)/processModel" -name pingInterval -value 00:00:10
        $ret += Get-webconfigurationproperty "$($AppPoolDefaults)/processModel" -name pingInterval | Select-Object name,value
        
        Set-webconfigurationproperty "$($AppPoolDefaults)/failure" -name rapidFailProtection -value false
        $ret += Get-webconfigurationproperty "$($AppPoolDefaults)/failure" -name rapidFailProtection | Select-Object name,value
        
        New-WebAppPool -Name $WebServerVar.DefaultAppPool -Force | Start-WebAppPool
        
        if($Error){
            for ($i = 0; $i -lt $Error.Count; $i++){
                $ret.ClassError += @{"Error[SetApplicationPoolDefaults]"=$error[$i].Exception}
            }
            $Error.Clear()
        }
        return $ret
    }
    
    [object]static CreateDefaultWebsite($WebServerVar){
        $Error.Clear()
        $ret = @{}

        $retDefaultWebSite = New-WebSite -name $($WebServerVar.DefaultWebSite) -iD ($WebServerVar.WebSiteId) -Port ($WebServerVar.DefaultPort) -physicalPath:$($WebServerVar.DefaultWebSitePath) -ApplicationPool $($WebServerVar.DefaultAppPool) -Force
        
        $ret.DefaultWebSiteID              = $($retDefaultWebSite.ID)
        $ret.DefaultWebSiteName            = $($retDefaultWebSite.Name)
        $ret.DefaultWebSiteState           = $retDefaultWebSite.state
        $ret.DefaultWebSiteApplicationPool = $($retDefaultWebSite.applicationPool)
        $ret.DefaultWebSitePhysicalPath    = $($retDefaultWebSite.physicalPath)

$DefaultWebSiteContent = @"





<h1>PowerShell</h1>



<hr></hr>




<h2>PowerShell created WebSite</h2>



<hr></hr>




This is a PowerShell-created Demo Default WebSite



"@

        $ret.DefaultWebSiteContent += Set-Content "$($WebServerVar.DefaultWebSitePath)\index.htm" $DefaultWebSiteContent -PassThru
        
        if($Error){
            for ($i = 0; $i -lt $Error.Count; $i++){
                $ret.ClassError += @{"Error[CreateDefaultWebsite]"=$error[$i].Exception}
            }
            $Error.Clear()
        }
        return $ret
    }

    [object]static RestartWebServer(){
        $Error.Clear()
        $ret = @{}

        $InstallArgs = @{}
        $InstallArgs.FilePath     = "iisreset"
        $InstallArgs.ArgumentList = @()
        $InstallArgs.ArgumentList += "/noforce"
        $InstallArgs.WindowStyle  = 'Hidden'
        $InstallArgs.Wait         = $true
        $ret.iisreset = (Start-Process @InstallArgs -PassThru).ExitCode
        if($Error){
            for ($i = 0; $i -lt $Error.Count; $i++){
                $ret.ClassError += @{"Error[RestartWebServer]"=$error[$i].Exception}
            }
            $Error.Clear()
        }
        return $ret
    }

    [object]static SetAcl([PSCustomObject]$AclArgs){
        $Error.Clear()

        <#
            https://blog.netwrix.com/2018/04/18/how-to-manage-file-system-acls-with-powershell-scripts/
        #>

        $ret = @()
        foreach($item in $AclArgs){
        
            foreach($user in $item.Account){
        
                foreach($path in $item.WebSitePath){
                    $ret += "$($user)=$($path):$($item.Permission),$($item.PermissionType))" 
                    $acl = Get-Acl -Path $path
                    $acl | Select-Object
                    $AccessRule = New-Object System.Security.AccessControl.FileSystemAccessRule($user,$item.Permission,$item.PermissionType)
                    $acl.SetAccessRule($AccessRule)
                    $acl | Set-Acl -Path $path
                    $acl | Select-Object
                    if($Error){
                        for ($i = 0; $i -lt $Error.Count; $i++){
                            $ret.ClassError += @{"Error[SetAcl]"=$error[$i].Exception}
                        }
                        $Error.Clear()
                    }
                }
            }
               
        }        
        return $ret
    }
    
    [object]static PurgeAcl([PSCustomObject]$AclArgs){
        $Error.Clear()

        <#
            https://blog.netwrix.com/2018/04/18/how-to-manage-file-system-acls-with-powershell-scripts/
        #>

        $ret = @()
        foreach($item in $AclArgs){
        
            foreach($user in $item.Account){
        
                foreach($path in $item.WebSitePath){
                    $ret += "$($user)=$($path)" 
                    $acl = Get-Acl -Path $path
                    $acl | Select-Object
                    $usersid = New-Object System.Security.Principal.Ntaccount($user)
                    $acl.PurgeAccessRules($usersid)
                    $acl | Set-Acl -Path $path
                    $acl | Select-Object
                    if($Error){
                        for ($i = 0; $i -lt $Error.Count; $i++){
                            $ret.ClassError += @{"Error[SetAcl]"=$error[$i].Exception}
                        }
                        $Error.Clear()
                    }
                }
            }
               
        }        
        return $ret
    }
    
}

<# List WindowsFeatures
$onlyinstalled = $true
$WinFeature = [PSWinFeatures]::GetWindowsFeatures($onlyinstalled)
$WinFeature | Sort-Object Name
#>

#region Functions to export
function Uninstall-WindowsWebServer{
    param(
        [Parameter(Mandatory=$true)]    
        [System.Array]$WindowsFeatures
    )
    $function = $($MyInvocation.MyCommand.Name); Write-verbose $function

    $WinFeature = [PSWinFeatures]::RemoveWindowsFeatures($WindowsFeatures)
    $WinFeature.ExitCode
    if($WinFeature.ExitCode.Values -contains 'Failed'){
        $WinFeature.ClassError.Keys
        $WinFeature.ClassError.Values
    }

    if((Get-WebAppPoolState -Name "DefaultAppPool").Value -ne 'Stopped'){Stop-WebAppPool -Name "DefaultAppPool"}
    if((Get-Website -Name "Default Web Site").State -ne 'Stopped'){Stop-WebSite -Name "Default Web Site"}

    if(Test-Path -Path $WebServerVar.DefaultWebSitePath){Remove-Item -Path $WebServerVar.DefaultWebSitePath -Recurse -Force}
    if(Test-Path -Path $WebServerVar.DefaultWebSitePath){Remove-Item -Path $WebServerVar.WmsvcPath -Recurse -Force}
    if(Test-Path -Path $WebServerVar.DefaultWebSitePath){Remove-Item -Path $WebServerVar.WebSiteLogPath -Recurse -Force}
    if(Test-Path -Path $WebServerVar.DefaultWebSitePath){Remove-Item -Path $WebServerVar.WebServerRootPath -Recurse -Force}
}

function Install-WindowsWebServer{
    param(
        [Parameter(Mandatory=$true)]    
        [System.Array]$WindowsFeatures,

        [Parameter(Mandatory=$true)]    
        [String]$Logfile
    )
    $function = $($MyInvocation.MyCommand.Name); Write-verbose $function
    "$(Get-Date -f 'yyyy-MM-dd HH:mm:ss') $function" | Out-File $Logfile -Append -Encoding default

    $WinFeature = [PSWinFeatures]::InstallWindowsFeatures($WindowsFeatures,$Logfile)
    $WinFeature.ExitCode | Out-File $Logfile -Append -Encoding default
    if($WinFeature.ExitCode.Values -contains 'Failed'){
        $WinFeature.ClassError.Keys
        $WinFeature.ClassError.Values
    }
}

function Remove-DefaultAclFromWebDrive{
    param(
        [Parameter(Mandatory=$true)]    
        [hashtable]$WebServerVar
    )
    $function = $($MyInvocation.MyCommand.Name); Write-verbose $function
    "$(Get-Date -f 'yyyy-MM-dd HH:mm:ss') $function" | Out-File $WebServerVar.Logfile -Append -Encoding default

    $aclset = @()

    $Purge = @{
        WebSitePath = "$($WebServerVar.WebServerDrive)"
        Account     = "CREATOR OWNER","Everyone"
    }
    $aclset += [PSCustomObject]$Purge        
    [PSWebServer]::PurgeAcl($aclset) | Out-File $WebServerVar.Logfile -Append -Encoding default

}
function Set-WebServerDirecoryConfiguration{
    param(
        [Parameter(Mandatory=$true)]    
        [hashtable]$WebServerVar
    )
    $function = $($MyInvocation.MyCommand.Name); Write-verbose $function
    "$(Get-Date -f 'yyyy-MM-dd HH:mm:ss') $function" | Out-File $WebServerVar.Logfile -Append -Encoding default

    $aclset = @()

    $FullControl = @{
        WebSitePath = $($WebServerVar.DefaultWebSitePath),$($WebServerVar.WebSiteLogPath),$($WebServerVar.WmsvcPath)
        Account     = "NT Service\WMSVC"
        Permission  = "FullControl"
        PermissionType = 'Allow'
    }
    $aclset += [PSCustomObject]$FullControl
    
    $Read = @{
        WebSitePath = $($WebServerVar.DefaultWebSitePath),$($WebServerVar.WebSiteLogPath),$($WebServerVar.WmsvcPath)
        Account     = "IUSR","IIS_IUSRS"
        Permission  = "Read"
        PermissionType = 'Allow'
    }
    $aclset += [PSCustomObject]$Read

    [PSWebServer]::CreateWebServerDirecory([hashtable]$WebServerVar) | Out-File $WebServerVar.Logfile -Append -Encoding default
    [PSWebServer]::SetAcl($aclset) | Out-File $WebServerVar.Logfile -Append -Encoding default

}

function Set-WebManagementServiceConfiguration{
    param(
        [Parameter(Mandatory=$true)]    
        [hashtable]$WebServerVar
    )
    $function = $($MyInvocation.MyCommand.Name); Write-verbose $function
    "$(Get-Date -f 'yyyy-MM-dd HH:mm:ss') $function" | Out-File $WebServerVar.Logfile -Append -Encoding default

    [PSWebServer]::SetWebManagementService($WebServerVar.Service) | Out-File $WebServerVar.Logfile -Append -Encoding default
}

function Set-WebServerConfiguration{
    param(
        [Parameter(Mandatory=$true)]    
        [hashtable]$WebServerVar
    )
    $function = $($MyInvocation.MyCommand.Name); Write-verbose $function
    "$(Get-Date -f 'yyyy-MM-dd HH:mm:ss') $function" | Out-File $WebServerVar.Logfile -Append -Encoding default

    [PSWebServer]::RemoveDefaultWebsite($WebServerVar) | Out-File $WebServerVar.Logfile -Append -Encoding default
    [PSWebServer]::RemoveDefaulApplicationPool($WebServerVar) | Out-File $WebServerVar.Logfile -Append -Encoding default
    [PSWebServer]::SetApplicationPoolDefaults($WebServerVar) | Out-File $WebServerVar.Logfile -Append -Encoding default
}

function Set-DefaultWebsiteConfiguration{
    param(
        [Parameter(Mandatory=$true)]    
        [hashtable]$WebServerVar
    )
    $function = $($MyInvocation.MyCommand.Name); Write-verbose $function
    "$(Get-Date -f 'yyyy-MM-dd HH:mm:ss') $function" | Out-File $WebServerVar.Logfile -Append -Encoding default

    $aclset = @()

    $FullControl = @{
        WebSitePath = "$($WebServerVar.DefaultWebSitePath)","$($WebServerVar.DefaultWebSitePath)\index.htm"
        Account     = "NT Service\WMSVC"
        Permission  = "FullControl"
        PermissionType = 'Allow'
    }
    $aclset += [PSCustomObject]$FullControl
            
    $Read = @{
        WebSitePath = "$($WebServerVar.DefaultWebSitePath)","$($WebServerVar.DefaultWebSitePath)\index.htm"
        Account     = "IUSR","IIS_IUSRS"
        Permission  = "Read"
        PermissionType = 'Allow'
    }
    $aclset += [PSCustomObject]$Read

    [PSWebServer]::CreateDefaultWebsite([hashtable]$WebServerVar) | Out-File $WebServerVar.Logfile -Append -Encoding default
    [PSWebServer]::SetAcl($aclset) | Out-File $WebServerVar.Logfile -Append -Encoding default
    [PSWebServer]::RestartWebServer() | Out-File $WebServerVar.Logfile -Append -Encoding default

}
#endregion

#requires -Version 5

#region Script Variavles
$ErrorActionPreference = 'Stop'
$script:Scriptpath     = Split-Path -Parent $MyInvocation.MyCommand.Path
$script:Scriptname     = $MyInvocation.MyCommand.ToString()
$script:Basename       = $script:Scriptname.Remove($script:Scriptname.Length -4)
$script:Logpath        = "C:\Admin\Logs"
$script:Logfile        = "$($script:Logpath)\$($script:Basename).log"
$script:Return         = 0
$script:ScriptStart    = (get-date)
#endregion

#region set Windows Features
$WindowsFeatures = @(
    'Web-Server',
    'Web-Request-Monitor',
    'Web-Asp-Net',
    'Web-Asp-Net45',
    'Web-Windows-Auth',
    'Web-Mgmt-Service',
    'Web-Mgmt-Console'
)
#endregion

#region WebServer Variables
[hashtable]$WebServerVar = @{}
$WebServerVar.Service               = 'wmsvc'
$WebServerVar.WebSiteId             = 10
$WebServerVar.DefaultPort           = 80
$WebServerVar.DefaultWebSite        = 'Default Web Site'
$WebServerVar.DefaultAppPool        = 'DefaultAppPool'
$WebServerVar.WebServerDrive        = "D:"
$WebServerVar.WebServerRootPath     = "$($WebServerVar.WebServerDrive)\IIS_Server"
$WebServerVar.DefaultWebSitePath    = "$($WebServerVar.WebServerRootPath)\Default Web Site"
$WebServerVar.WebSiteLogPath        = "$($WebServerVar.WebServerDrive)\IIS_Log"
$WebServerVar.WmsvcPath             = "$($WebServerVar.WebSiteLogPath)\wmsvc"
$WebServerVar.InetRootPath          = "$($env:SystemRoot)\System32\inetsrv"
$WebServerVar.Logfile               = $script:Logfile
#endregion

"Starting $($script:Scriptname)" | Out-File $script:Logfile -Encoding default

Install-WindowsWebServer -WindowsFeatures $WindowsFeatures -Logfile $script:Logfile -Verbose
Remove-DefaultAclFromWebDrive -WebServerVar $WebServerVar -Verbose
Set-WebServerDirecoryConfiguration -WebServerVar $WebServerVar -Verbose
Set-WebManagementServiceConfiguration -WebServerVar $WebServerVar -Verbose
Set-WebServerConfiguration -WebServerVar $WebServerVar -Verbose
Set-DefaultWebsiteConfiguration -WebServerVar $WebServerVar -Verbose

#Start-Process -FilePath "$($WebServerVar.InetRootPath)\InetMgr.exe"

#Delegating IIS administration to Domain Users
#https://blogs.technet.microsoft.com/leesab/2014/07/30/delegating-iis-administration-to-domain-users-non-administrators/

$time = $([math]::round(((New-TimeSpan $($script:ScriptStart) $(get-date)).TotalMinutes),2))
"Finish $($script:Scriptname) in $($time) Minutes)" | Out-File $script:Logfile -Append -Encoding default
Write-Output "End Script (Returncode $($script:Return), Time $($time) Minutes)"

$DelegateIISAdmin = @"
To delegate management of IIS to domain users

1) Enable Remote Connections through Management service.
2) Adding the AD user(s)/group(s) to the separate sites listed in IIS, using IIS Manager Permissions
3) Delegating the IIS features to the above users to be able to use, this is set using feature Delegation.   
4) Connecting to IIS as a non-administrator

https://blogs.technet.microsoft.com/leesab/2014/07/30/delegating-iis-administration-to-domain-users-non-administrators/
"@
Write-host $DelegateIISAdmin -ForegroundColor Yellow
```

</div>