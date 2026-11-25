---
title: Domain Admins
date: '2015-03-18T21:58:47+01:00'
author: Tinu
excerpt: ''
categories:
- Active Directory
tags:
- Accounts
- Active Directory
wordpress_id: 1001
layout: post
permalink: /wiki/domain-admins/
render_with_liquid: false
---

Alle Domain Admins einer Domain auflisten

```
$domainDnsName = read-host "Enter the DNS Domain Name to connect to"
$accountName = 'Domain Admins'
$searcher = New-Object DirectoryServices.DirectorySearcher
$searcher.Filter = "(sAMAccountName=$accountName)"
$searcher.SearchRoot = "LDAP://$domainDnsName"
$searcher.PageSize = 100
$ret = $searcher.FindOne()
#LDAP-Path to the 'Domain Admins'
$members = $ret.GetDirectoryEntry().Member
$members | %{
    #Bind to the User-Object and return the given properties
    [adsi] "LDAP://$($_)" | Select sAMAccountName, DisplayName, Description
}
```