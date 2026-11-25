---
title: Active Directory konfigurieren
date: '2014-11-30T11:22:09+01:00'
author: Tinu
excerpt: ''
categories:
- Active Directory
tags:
- Active Directory
wordpress_id: 296
layout: post
permalink: /wiki/active-directory-konfigurieren/
render_with_liquid: false
---

Ist der Forest/Domain erstellt, wird als nächstes die OU-Struktur aufgebaut und danach die notwendigen Domain Admins erstellt. Im Anschluss wird dann der BuiltIn Administrator umbenannt und mit einem sehr langen und komplexen Passwort versehen, welches unter Verschluss aufbewahrt werden sollte.

## Organizational Units aufbauen

 Die OU-Struktur kann in etwa folgenderweise aussehen: 

```
Domain
-<FA>_Computers
---Windows_Servers
---Linux_Servers
---Special_Servers
---Windows_Clients
---Special_Clients
-<FA>_Accounts
---Admin_Users
---Technical_Users
---Domain_Users
---Special_Users
-<FA>_Groups
---Roles
---Groups
-<FA>_Mail
---Distribution_Groups
---Mailboxes_Accounts
```

 Diese OUs werden mit folgender Function erstellt: 

```
function CreateOrganizationalUnits{
    <#
    .SYNOPSIS
        Create CreateOrganizationalUnits
    #>
    param(
		[Parameter(Mandatory=$true)][String] $OuName,
		[Parameter(Mandatory=$true)][String] $OuDescription,
		[Parameter(Mandatory=$true)][String] $DistinguishedName
    )
    $function = $($MyInvocation.MyCommand.Name)
    if ($psdebug){LogInfo -Function $function -Message "..." -info}
    try{
		#Create Organizational Unit
		$NewOU = New-ADOrganizationalUnit -Name $OuName -DisplayName $OuName -Description $OuDescription -Path $DistinguishedName`
		-ProtectedFromAccidentalDeletion $false -PassThru
		LogInfo -Function $function -Message "$($function) $($NewOU)" -info
	}
	catch{
		LogInfo -Function $function -Message "$($_.Exception.Message)" -error -print
		$error.clear()
	}
}
```

## Admin Account erstellen

 Damit nicht weiterhin mit dem BuiltIn Administrator gearbeitet wird, sollte mindestens ein neuer Domain Admin erstellt werden. 

```
function CreateAdminAccount{
    <#
    .SYNOPSIS
        Create Admin Users
    #>
    param (
		[Parameter(Mandatory=$true)][String] $Username,
		[Parameter(Mandatory=$true)][String] $UserGivenName,
		[Parameter(Mandatory=$true)][String] $UserSurname,
		[Parameter(Mandatory=$true)][String] $secpwd
    )
    $function = $($MyInvocation.MyCommand.Name)
    if ($psdebug){LogInfo -Function $function -Message "..." -info}
	try{
		$UserDisplayname = "$($UserSurname) $($UserGivenName)"
		$usrPrincipalName = "$($Username)@$($DnsDomainName)"
		$usrDescription = "Admin: $($UserDisplayname)"
		$usrPath = Get-ADOrganizationalUnit -Filter 'Name -like "Admin_Users"'
		$usrMemberOf = Get-ADGroup -Identity "Domain Admins"
		
		$ret = New-ADUser -Name $Username -SamAccountName $Username -UserPrincipalName $usrPrincipalName`
		-GivenName $UserGivenName -Surname $UserSurname -DisplayName $UserDisplayname -Description $usrDescription`
		-Path $usrPath -PasswordNeverExpires $true -EmailAddress $usrPrincipalName`
		-AccountPassword $secpwd -Enabled $true -PassThru
		LogInfo -Function $function -Message $ret -info
		
		Add-ADPrincipalGroupMembership -Identity:$ret -MemberOf:$usrMemberOf
	}
	catch{
		LogInfo -Function $function -Message "$($_.Exception.Message)" -error -print
		$error.clear()
	}
}
```