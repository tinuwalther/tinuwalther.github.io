---
layout: post
title:  "Certificates"
author: Tinu
categories: "System-Engineering"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

# Table of Contents

- [Table of Contents](#table-of-contents)
- [List certificates](#list-certificates)
  - [List all expired certificates](#list-all-expired-certificates)
- [Import certificates](#import-certificates)
- [Remove certificates](#remove-certificates)
- [See also](#see-also)

# List certificates

````powershell
$Issuer = '*'
Get-ChildItem Cert:\LocalMachine -Recurse | Where-Object Issuer -match "CN=$Issuer"
````

## List all expired certificates

````powershell
$ret = @()
$Issuer = '*'
$certs = Get-ChildItem Cert:\LocalMachine -Recurse | Where-Object Issuer -match "CN=$Issuer"
foreach($item in $certs){
   if($item.NotAfter.Date -le (Get-Date)){
      $obj = [PSCustomObject]@{
         Issuer     = $item.Issuer
         ValidFrom  = $item.NotBefore.Date
         ExpiresOn  = $item.NotAfter.Date
         KeyLength  = $item.PublicKey.Key.KeySize
         Thumbprint = $item.Thumbprint
      }
      $ret += $obj
   }
}
$ret | Format-List
````

# Import certificates

````powershell
$Source = 'C:\temp\certstoimport'
$Target = 'Cert:\LocalMachine\Root'
foreach($item in (Get-ChildItem $Source -Filter '*.cer')){
   Import-Certificate -FilePath $item.FullName -CertStoreLocation $Target
}
````

# Remove certificates

````powershell
$Issuer = '*'
$certs  = Get-ChildItem Cert:\LocalMachine -Recurse | Where-Object Issuer -match "CN=$Issuer"
foreach($item in $certs){
   Remove-Item $item
}
````

# See also

[Certificate Provider](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.security/about/about_certificate_provider?view=powershell-6) on Microsoft Docs.

[ [Top](#table-of-contents) ] [ [Blog](../devops.html) ]