---
layout: post
title:  "Device Manager"
author: Tinu
categories: "System-Engineering"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Find Information about Device Errors](#find-information-about-device-errors)
- [See also](#see-also)

## Find Information about Device Errors

Get-CimInstance -ClassName Win32_PNPEntity.

````powershell
function Get-ErrorDeviceList{
    <#
       Get Devices with some problems
       Error codes = https://support.microsoft.com/en-us/kb/310123
       Availability codes = https://msdn.microsoft.com/en-us/library/aa394353%28v=vs.85%29.aspx
    #>
    [CmdletBinding()]
    param()
    $function = $($MyInvocation.MyCommand.Name)
    Write-Verbose "Running $function"
    try{
        Get-CimInstance -ClassName Win32_PNPEntity | Where-Object{$_.ConfigManagerErrorCode -ne 0} | %{
            #region Error code matrix
            switch ($_.ConfigManagerErrorCode){
                1 {$errorcode = "This device is not configured correctly."}
                3 {$errorcode = "The driver for this device might be corrupted, or your system may be running low on memory or other resources."}
                10 {$errorcode = "This device cannot start."}
                12 {$errorcode = "This device cannot find enough free resources that it can use. If you want to use this device, you will need to disable one of the other devices on this system."}
                14 {$errorcode = "This device cannot work properly until you restart your computer."}
                16 {$errorcode = "Windows cannot identify all the resources this device uses."}
                18 {$errorcode = "Reinstall the drivers for this device. "}
                19 {$errorcode = "Windows cannot start this hardware device because its configuration information (in the registry) is incomplete or damaged."}
                21 {$errorcode = "Windows is removing this device."}
                22 {$errorcode = "This device is disabled."}
                24 {$errorcode = "This device is not present, is not working properly, or does not have all its drivers installed."}
                28 {$errorcode = "The drivers for this device are not installed."}
                29 {$errorcode = "This device is disabled because the firmware of the device did not give it the required resources."}
                31 {$errorcode = "This device is not working properly because Windows cannot load the drivers required for this device."}
                32 {$errorcode = "A driver (service) for this device has been disabled. An alternate driver may be providing this functionality."}
                33 {$errorcode = "Windows cannot determine which resources are required for this device."}
                34 {$errorcode = "Windows cannot determine the settings for this device."}
                35 {$errorcode = "Your computer's system firmware does not include enough information to properly configure and use this device.`nTo use this device, contact your computer manufacturer to obtain a firmware or BIOS update."}
                36 {$errorcode = "This device is requesting a PCI interrupt but is configured for an ISA interrupt (or vice versa). Please use the computer's system setup program to reconfigure the interrupt for this device."}
                37 {$errorcode = "Windows cannot initialize the device driver for this hardware."}
                38 {$errorcode = "Windows cannot load the device driver for this hardware because a previous instance of the device driver is still in memory."}
                39 {$errorcode = "Windows cannot load the device driver for this hardware. The driver may be corrupted or missing."}
                40 {$errorcode = "Windows cannot access this hardware because its service key information in the registry is missing or recorded incorrectly."}
                41 {$errorcode = "Windows successfully loaded the device driver for this hardware but cannot find the hardware device."}
                42 {$errorcode = "Windows cannot load the device driver for this hardware because there is a duplicate device already running in the system."}
                43 {$errorcode = "Windows has stopped this device because it has reported problems."}
                44 {$errorcode = "An application or service has shut down this hardware device."}
                45 {$errorcode = "Currently, this hardware device is not connected to the computer."}
                46 {$errorcode = "Windows cannot gain access to this hardware device because the operating system is in the process of shutting down."}
                47 {$errorcode = "Windows cannot use this hardware device because it has been prepared for safe removal, but it has not been removed from the computer."}
                48 {$errorcode = "The software for this device has been blocked from starting because it is known to have problems with Windows. Contact the hardware vendor for a new driver."}
                49 {$errorcode = "Windows cannot start new hardware devices because the system hive is too large (exceeds the Registry Size Limit)."}
                52 {$errorcode = "Windows cannot verify the digital signature for the drivers required for this device."}
                default {}
            }
            Write-Verbose "$($_.ConfigManagerErrorCode): $($errorcode)"
            #endregion
            [PSCustomObject] @{
                Availability = $_.Availability
                Name         = $_.Name
                Description  = $_.Description
                Service      = $_.Service
                Status       = $_.Status
                ErrorCode    = $errorcode
                ClassGuid    = $_.ClassGuid
            }
        }
    }
    catch{
          write-host "$($function): $($_.Exception.Message)" -ForegroundColor Red
          $error.clear()
    }
}
Get-ErrorDeviceList  -Verbose
````

## See also

[Error codes in Device Manager in Windows](https://support.microsoft.com/en-us/help/310123/error-codes-in-device-manager-in-windows)

[Win32_PnPEntity class](https://docs.microsoft.com/de-de/windows/win32/cimwin32prov/win32-pnpentity?redirectedfrom=MSDN)

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]
