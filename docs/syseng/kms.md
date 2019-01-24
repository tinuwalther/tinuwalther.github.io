# Get KMS Infos

## Registry

````powershell
Get-Item 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform'
````

The KMS Server is list on KeyManagementServiceName.  

## Software licensing service (slmgr)

````powershell
cscript "$($env:windir)\system32\slmgr.vbs" -dlv //Nologo
````

The KMS Server is list on 'KMS machine IP address'.  

````powershell
function Get-SettingsFromSlmgr{
    <#
        Get License Information from Windows Software Licensing Management Tool
    #>
    $ret = @()
    try{
        if($psdebug){write-host "Running $($function) ..." -ForegroundColor Yellow}
        $slm = cscript "$($env:windir)\system32\slmgr.vbs" -dlv //Nologo
        if($slm -is [system.array]){

            $windows = (($slm | select-string -pattern "Name:" -list).line)
            if ($windows -is [system.array]){$windowsName = $windows[0]}else{$windowsName = $windows}
            if($windowsName -ne $null){
                $windowsName = ($windowsName.Split(':')[1]).Trim()
            }

            $regkms = (($slm | select-string -pattern "KMS machine name" -list).line)
            if($regkms -ne $null){$KMSmachine = $regkms.Trim()} # R7VHC = SPLA
            if($KMSmachine -ne $null){
                $KMSServer = ($KMSmachine.Split(':')[1]).Trim()
                $KMSPort   = ($KMSmachine.Split(':')[2]).Trim()
            }else{
                $KMSServer = $false
                $KMSPort   = $null
            }

            $Description = (($slm | select-string -pattern "Description:" -list).line)
            $ProductKeyChannel = (($slm | select-string -pattern "Product Key Channel" -list).line)
            if($ProductKeyChannel -ne $null){
                $ProductKeyChannel = ($ProductKeyChannel.Split(':')[1]).trim() 
            }else{
                $ProductKeyChannel = $null
            }

            $ProductKey = (($slm | select-string -pattern "Partial Product Key:" -list).line)
            if($ProductKey -ne $null){
                $ProductKey = ($ProductKey.Split(':')[1]).trim()
            }else{
                $ProductKey = $null
            }

            $LicenseStatus = (($slm | select-string -pattern "License Status:" -list).line)
            if($LicenseStatus -ne $null){
                $LicenseStatus = ($LicenseStatus.Split(':')[1]).trim()  
            }else{
                $LicenseStatus = $null
            }

            $obj = [PSCustomObject]@{
                Product       = $windowsName
                KMSServer     = $KMSServer
                KMSPort       = $KMSPort
                Channel       = $ProductKeyChannel
                ProductKey    = $ProductKey
                LicenseStatus = $LicenseStatus
            }
            $ret += $obj
        }
    }
    catch [Exception]{
          write-host "$($function): $($_.Exception.Message)" -ForegroundColor Red
          $error.clear()
    }
    return $ret
}
````