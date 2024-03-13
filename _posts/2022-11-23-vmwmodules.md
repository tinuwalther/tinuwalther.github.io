---
layout: post
title:  "Offline VMware Modules"
author: Tinu
categories: "VMware"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

## Table of Contents

[Table of Contents](#table-of-contents)
[Get the latest VMware Modules](#get-the-latest-vmware-modules)
- [Table of Contents](#table-of-contents)
- [Get the latest VMware Modules](#get-the-latest-vmware-modules)
  - [Download Modules](#download-modules)
  - [Compress the PowerCLI-Modules](#compress-the-powercli-modules)
- [See also](#see-also)

## Get the latest VMware Modules

How to create offline VMware Modules.

### Download Modules

Download PowerCLI and their Dependencies:

````powershell
Save-Module -Name VMware.PowerCLI -Path F:\temp\VMware\ -Repository PSGallery
````

### Compress the PowerCLI-Modules

Required Modules from "F:\temp\VMware\VMware.PowerCLI\13.0.0.20829139\VMware.PowerCLI.psd1"

````powershell
[PSCustomObject]$RequiredModules = @(
    @{"ModuleName"="VMware.VimAutomation.Sdk";"ModuleVersion"="13.0.0.20791442"}
    @{"ModuleName"="VMware.VimAutomation.Common";"ModuleVersion"="13.0.0.20797081"}
    @{"ModuleName"="VMware.Vim";"ModuleVersion"="8.0.1.20797199"}
    @{"ModuleName"="VMware.VimAutomation.Core";"ModuleVersion"="13.0.0.20797821"}
    @{"ModuleName"="VMware.VimAutomation.Srm";"ModuleVersion"="12.7.0.20091290"}
    @{"ModuleName"="VMware.VimAutomation.License";"ModuleVersion"="12.0.0.15939670"}
    @{"ModuleName"="VMware.VimAutomation.Vds";"ModuleVersion"="13.0.0.20803944"}
    @{"ModuleName"="VMware.CloudServices";"ModuleVersion"="12.6.0.19606210"}
    @{"ModuleName"="VMware.VimAutomation.Vmc";"ModuleVersion"="13.0.0.20797723"}
    @{"ModuleName"="VMware.VimAutomation.Nsxt";"ModuleVersion"="13.0.0.20797706"}
    @{"ModuleName"="VMware.VimAutomation.vROps";"ModuleVersion"="12.5.0.19167825"}
    @{"ModuleName"="VMware.VimAutomation.Cis.Core";"ModuleVersion"="13.0.0.20797636"}
    @{"ModuleName"="VMware.VimAutomation.HorizonView";"ModuleVersion"="13.0.0.20685235"}
    @{"ModuleName"="VMware.VimAutomation.Cloud";"ModuleVersion"="13.0.0.20809912"}
    @{"ModuleName"="VMware.DeployAutomation";"ModuleVersion"="8.0.0.20826874"}
    @{"ModuleName"="VMware.ImageBuilder";"ModuleVersion"="8.0.0.20817746"}
    @{"ModuleName"="VMware.VimAutomation.Storage";"ModuleVersion"="13.0.0.20797966"}
    @{"ModuleName"="VMware.VimAutomation.StorageUtility";"ModuleVersion"="1.6.0.0"}
    @{"ModuleName"="VMware.VumAutomation";"ModuleVersion"="12.7.0.20091294"}
    @{"ModuleName"="VMware.VimAutomation.Security";"ModuleVersion"="13.0.0.20800625"}
    @{"ModuleName"="VMware.VimAutomation.Hcx";"ModuleVersion"="13.0.0.20803747"}
    @{"ModuleName"="VMware.VimAutomation.WorkloadManagement";"ModuleVersion"="12.4.0.18627055"}
    @{"ModuleName"="VMware.Sdk.Runtime";"ModuleVersion"="1.0.110.20623688"}
    @{"ModuleName"="VMware.Sdk.vSphere";"ModuleVersion"="8.0.110.20624081"}
    @{"ModuleName"="VMware.PowerCLI.VCenter";"ModuleVersion"="12.6.0.19600125"}
    @{"ModuleName"="VMware.Sdk.Nsx.Policy";"ModuleVersion"="4.0.0.20829136"}
    ## @{"ModuleName"="VMware.Sdk.Vcf.CloudBuilder";"ModuleVersion"="0.0.0.0"}
    ## @{"ModuleName"="VMware.Sdk.Vcf.SddcManager";"ModuleVersion"="0.0.0.0"}
)

$Source = $RequiredModules.ModuleName | ForEach-Object {

    $ModuleName = $_
    $Module = Get-Item "F:\temp\VMware\$($ModuleName)"
    foreach($item in $Module){
        $item.FullName
    }

}
$ArchiveFilePath = "F:\temp\VMware\VMware-Moduel.13.0.zip"

Compress-Archive -Path $Source -DestinationPath $ArchiveFilePath -CompressionLevel Optimal
````

## See also

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]
