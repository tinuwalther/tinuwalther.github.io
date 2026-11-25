---
title: SoftwareLicense Class
date: '2017-10-09T15:27:49+02:00'
author: Tinu
excerpt: Windows Lizenzierung als PowerShell-Class
categories:
- PowerShell
tags:
- Class
- Software
image: /assets/wiki/powershell-1.png
wordpress_id: 2398
layout: post
permalink: /wiki/kms/
render_with_liquid: false
---

Windwos Lizenzierung aus der CimInstance SoftwareLicensingProduct als PowerShell-Class. LicenseStatus 1 = <span class="short_text" id="result_box" lang="en"><span class="">licensed</span></span>, 0 = not <span class="short_text" id="result_box" lang="en"><span class="">licensed</span></span>

```
Class PSSoftwareLicensingProduct{

    #region Properties
    [object] hidden $SoftwareLicensingProduct = $null
    [object]$ID                               = $null
    [object]$ApplicationID                    = $null
    [object]$Name                             = $null
    [object]$Description                      = $null
    [object]$LicenseFamily                    = $null
    [object]$LicenseStatus                    = $null
    [object]$PartialProductKey                = $null
    [object]$VLActivationInterval             = $null
    [object]$VLActivationTypeEnabled          = $null
    [object]$VLRenewalInterval                = $null
    [object]$RemainingAppReArmCount           = $null
    #endregion

    #region Constructor
    PSSoftwareLicensingProduct($Name){
        $this.SoftwareLicensingProduct = [PSSoftwareLicensingProduct]::GetSoftwareLicensingProduct($Name)
        $this.ID                       = $this.SoftwareLicensingProduct.ID   
        $this.ApplicationID            = $this.SoftwareLicensingProduct.ApplicationID   
        $this.Name                     = $this.SoftwareLicensingProduct.Name
        $this.Description              = $this.SoftwareLicensingProduct.Description
        $this.LicenseFamily            = $this.SoftwareLicensingProduct.LicenseFamily
        $this.LicenseStatus            = $this.SoftwareLicensingProduct.LicenseStatus
        $this.PartialProductKey        = $this.SoftwareLicensingProduct.PartialProductKey
        $this.VLActivationInterval     = $this.SoftwareLicensingProduct.VLActivationInterval
        $this.VLActivationTypeEnabled  = $this.SoftwareLicensingProduct.VLActivationTypeEnabled
        $this.VLRenewalInterval        = $this.SoftwareLicensingProduct.VLRenewalInterval
        $this.RemainingAppReArmCount   = $this.SoftwareLicensingProduct.RemainingAppReArmCount
    }
    #endregion

    #region Methods
    [object]static GetSoftwareLicensingProduct($Name){
        $ret = @{}
        $objCimInstance = Get-CimInstance SoftwareLicensingProduct | Where-Object {
            ($_.LicenseStatus -eq 1 -and $_.Name -match $Name)
        }
        $ret.ID                       = $objCimInstance.ID
        $ret.ApplicationID            = $objCimInstance.ApplicationID
        $ret.Name                     = $objCimInstance.Name
        $ret.Description              = $objCimInstance.Description
        $ret.LicenseFamily            = $objCimInstance.LicenseFamily
        $ret.LicenseStatus            = $objCimInstance.LicenseStatus
        $ret.PartialProductKey        = $objCimInstance.PartialProductKey
        $ret.VLActivationInterval     = $objCimInstance.VLActivationInterval
        $ret.VLActivationTypeEnabled  = $objCimInstance.VLActivationTypeEnabled
        $ret.VLRenewalInterval        = $objCimInstance.VLRenewalInterval
        $ret.RemainingAppReArmCount   = $objCimInstance.RemainingAppReArmCount
        return $ret
    }
    #endregion

}
New-Object PSSoftwareLicensingProduct('windows')
```