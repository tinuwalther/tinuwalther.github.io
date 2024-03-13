---
layout: post
title:  "Group Membership"
author: Tinu
categories: "PowerShell-Active-Directory"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [GroupMembership](#groupmembership)
- [See also](#see-also)

## GroupMembership

The Get-ADPrincipalGroupMembership cmdlet gets the Active Directory groups that have a specified user, computer, group, or service account as a member. This cmdlet requires a global catalog to perform the group search. If the forest that contains the user, computer, or group does not have a global catalog, the cmdlet returns a non-terminating error.

````powershell
@{$($env:USERNAME)=(Get-ADPrincipalGroupMembership -Identity $env:USERNAME | Select -ExpandProperty Name)}

Name            Value
----            -----
MyAccount       {Domain Users, Remote Desktop Users}
````

## See also

[Get-ADPrincipalGroupMembership](https://docs.microsoft.com/en-us/powershell/module/addsadministration/get-adprincipalgroupmembership?view=win10-ps) on Microsoft Docs.

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]
