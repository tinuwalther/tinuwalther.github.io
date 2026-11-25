---
title: Active Directory abfragen
date: '2015-02-24T15:54:27+01:00'
author: Tinu
excerpt: ''
categories:
- Active Directory
tags:
- Active Directory
- PSObject
wordpress_id: 783
layout: post
permalink: /wiki/active-directory-abfragen/
render_with_liquid: false
---

Active Directory mit PowerShell abfragen

## Bind aufs Active Directory

 Der einfachste Bind aufs AD mit PowerShell lautet: 

```
[adsi]'LDAP://contoso.com'
```

 Output 

```
distinguishedName : {DC=contoso,DC=com}
Path              : LDAP://contoso.com
```

 Will man gleichzeitig noch ein Objekt (z.B. den Administrator) suchen, dann geht das so: 

```
$accountName = 'Administrator'
$domainDnsName = 'contoso.com'
$searcher = New-Object DirectoryServices.DirectorySearcher
$searcher.Filter = "(sAMAccountName=$accountName)"
$searcher.SearchRoot = "LDAP://$domainDnsName"
$searcher.PageSize = 1000
$searcher.FindALl() | %{$_.Path}
```

 Output 

```
LDAP://contoso.com/CN=Administrator,CN=Users,DC=contoso,DC=com
```

## Bind aufs Active Directory mit anderen Credentials

 Und nun noch ein Bind mit anderen Credentials auf den Administrator: 

```
$domainDnsName = read-host "Enter the DNS Domain Name to connect to"
$userName = read-host "Enter the user to connect to $($domainDnsName)"
$secpwd = read-host -AsSecureString "Enter the password for $($userName)"
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secpwd)
$pwd = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
$domainEntry = New-Object System.DirectoryServices.DirectoryEntry("LDAP://$domainDnsName", "$($domainDnsName)\$($userName)", $pwd)
$accountName = 'Administrator'
$searcher = New-Object DirectoryServices.DirectorySearcher
$searcher.Filter = "(sAMAccountName=$accountName)"
$searcher.SearchRoot = $domainEntry
$searcher.PageSize = 1000
$searcher.FindALl() | %{$_.Path}
```

## Schema Version

 Schema Version auslesen. 

```
$forestDns = (Get-ADDomain | Select Forest).Forest
$forestDn = (Get-ADDomain -Identity $forestDns).DistinguishedName
$schema = Get-ADObject -Identity "cn=Schema,cn=Configuration,$($forestDn)" `
 -Properties * | Select objectVersion
$schemaversion = ""
switch ($schema.objectVersion){
    13 { $schemaversion = "Windows 2000 Server"}
    30 { $schemaversion = "Windows Server 2003"}
    31 { $schemaversion = "Windows Server 2003 R2"}
    44 { $schemaversion = "Windows Server 2008"}
    47 { $schemaversion = "Windows Server 2008 R2"}  
    51 { $schemaversion = "Windows Server 8 Developers Preview"}
    52 { $schemaversion = "Windows Server 8 Beta"}
    56 { $schemaversion = "Windows Server 2012"}
    69 { $schemaversion = "Windows Server 2012 R2"}
    72 { $schemaversion = "Windows Server Technical Preview (2014)"}
    default { $schemaversion = "unknown - $($schema.objectVersion)"}
}
Write-Host "Schema version is $($schemaversion)" -ForegroundColor Yellow
```

## Forest und FSMO-Rollen

 Forest Functional Level, Schema Master und Domain Naming Master auslesen. 

```
Get-ADForest -Identity $domain | select ForestMode, SchemaMaster, DomainNamingMaster
```

## Global Catalogs

 Alle Global Catalogs im Forest auslesen. 

```
Get-ADForest -Identity $domain | select -ExpandProperty GlobalCatalogs
```

## Domain und FSMO-Rollen

 Forestname, Domainname, Domain Functional Level, Infrastructure Master, PDC Emulator und RIS Master auslesen. 

```
Get-ADDomain -Identity $domain | select Forest, DNSRoot,`
DomainMode, InfrastructureMaster, PDCEmulator, RIDMaster
```

## Domain Controllers

 Alle Domain Controllers der Domain auslesen. 

```
Get-ADDomain -Identity $domain | select -ExpandProperty ReplicaDirectoryServers
```

 Alle Domain Controllers mit IP Adresse der Domain auslesen. 

```
Get-ADDomain | select -ExpandProperty ReplicaDirectoryServers | %{
    $dc = $_
    $ip = ([System.Net.Dns]::GetHostAddresses($($_))).IPAddressToString
    "Domain Controller: $($dc) IP Address: $($ip)"
}
```

## Sites im Forest

 Alle Sites im Forest auflisten. 

```
$ret = @()
$configurationNC = ([adsi]"LDAP://rootdse").ConfigurationNamingContext
$rootDSE = [adsi]"LDAP://$configurationNC"
$searcher = New-Object DirectoryServices.DirectorySearcher($rootDSE)
$searcher.Filter = "(objectClass=site)"
$searcher.PageSize = 100
$objects= $searcher.FindAll()
$objects | %{
    $obj = New-Object PSObject
    Add-Member -InputObject $obj -MemberType NoteProperty -Name Name -Value $($_.Properties.Item("Name"))
    Add-Member -InputObject $obj -MemberType NoteProperty -Name Description -Value $($_.Properties.Item("description"))
    Add-Member -InputObject $obj -MemberType NoteProperty -Name Location -Value $($_.Properties.Item("location"))
    $subnets = $($_.Properties.Item("SiteObjectBL"))
    $subnets | %{
        $site = "$($_.split(',')[0]) " + $site
    }
    Add-Member -InputObject $obj -MemberType NoteProperty -Name Subnets -Value $site
    $ret += $obj
}
$ret | Sort-Object Name | ft -AutoSize
```

## Subnets im Forest

 Alle Subnets im Forest auflisten. 

```
$ret = @()
$configurationNC = ([adsi]"LDAP://rootdse").ConfigurationNamingContext
$rootDSE = [adsi]"LDAP://$configurationNC"
$searcher = New-Object DirectoryServices.DirectorySearcher($rootDSE)
$searcher.Filter = "(objectClass=subnet)"
$searcher.PageSize = 100
$objects = $searcher.FindAll()
$objects | %{
    $obj = New-Object PSObject
    Add-Member -InputObject $obj -MemberType NoteProperty -Name Name -Value $($_.Properties.Item(“Name”))
    Add-Member -InputObject $obj -MemberType NoteProperty -Name Description -Value $($_.Properties.Item(“description”))
    try{
        $siteDN = $($_.Properties.Item("siteObject"))
        $site = $siteDN.split(',')[0]
    }
    catch
    {
        $site = "empty"
    }
    Add-Member -InputObject $obj -MemberType NoteProperty -Name Site -Value $site
    $ret += $obj
}
$ret | Sort-Object Name | ft -AutoSize
```

## Site Links im Forest

 Alle Site Links im Forest auflisten. 

```
$ret = @()
$configurationNC = ([adsi]"LDAP://rootdse").ConfigurationNamingContext
$rootDSE = [adsi]"LDAP://$configurationNC"
$searcher = New-Object DirectoryServices.DirectorySearcher($rootDSE)
$searcher.Filter = "(objectClass=siteLink)"
$searcher.PageSize = 100
$objects = $searcher.FindAll()
$objects | %{
    $obj = New-Object PSObject
    Add-Member -InputObject $obj -MemberType NoteProperty -Name Name -Value $($_.Properties.Item(“Name”))
    Add-Member -InputObject $obj -MemberType NoteProperty -Name Description -Value $($_.Properties.Item(“description”))
    Add-Member -InputObject $obj -MemberType NoteProperty -Name Cost -Value $($_.Properties.Item(“cost”))
    Add-Member -InputObject $obj -MemberType NoteProperty -Name Interval -Value $($_.Properties.Item(“replinterval”))         $ret += $obj
} 
$ret | Sort-Object Name | ft -AutoSize
```

## DHCP Server im Forest

 Alle aktivierten DHCP Server im Forest auflisten. 

```
$ret = @()
$configurationNC = ([adsi]"LDAP://rootdse").ConfigurationNamingContext
$rootDSE = [adsi]"LDAP://$configurationNC"
$searcher = New-Object DirectoryServices.DirectorySearcher($rootDSE)
$searcher.Filter = "(&(objectClass=dHCPClass)(dhcpIdentification=DHCP Server object))"
$searcher.PageSize = 100
$objects = $searcher.FindAll()
$objects | %{
    $obj = New-Object PSObject
    Add-Member -InputObject $obj -MemberType NoteProperty -Name Name -Value $($_.Properties.Item(“Name”))
    Add-Member -InputObject $obj -MemberType NoteProperty -Name distinguishedname -Value $($_.Properties.Item(“distinguishedname”))
    $ret += $obj
}
$ret | Sort-Object Name | ft -AutoSize
```