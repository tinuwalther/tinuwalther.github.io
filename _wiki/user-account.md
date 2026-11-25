---
title: User Account
date: '2014-11-26T21:36:03+01:00'
author: Tinu
excerpt: ''
categories:
- Active Directory
- PowerShell
tags:
- Accounts
- Active Directory
- PSObject
wordpress_id: 159
layout: post
permalink: /wiki/user-account/
render_with_liquid: false
---

## Alle lokalen Administratoren auflisten

 Ab PowerShell Version 2.0 

```
function CheckLocalUsers{
    <# Check local Users #>
    $function = $($MyInvocation.MyCommand.Name)
    $ret = @()
    try{
        if($psdebug){write-host "Running $($function) ..." -ForegroundColor Yellow}
        $adsi = [ADSI]"WinNT://$env:COMPUTERNAME"
        $adsi.psbase.children | Where-Object {$_.psBase.schemaClassName -eq "User"} | %{
            $obj = New-Object PSObject
            $UserName = $_.Name[0].Trim()
            $FullName = $_.FullName[0].Trim()
            $Description = $_.Description[0].Trim()
            $SID = $_.objectSid
            $obj = New-Object PSObject
        	Add-Member -InputObject $obj -MemberType NoteProperty -Name Name -Value $UserName
        	Add-Member -InputObject $obj -MemberType NoteProperty -Name FullName -Value $FullName
        	Add-Member -InputObject $obj -MemberType NoteProperty -Name Description -Value $Description
            $ret += $obj
        }
    }
    catch [Exception]{
          write-host "$($function): $($_.Exception.Message)" -ForegroundColor Red
          $error.clear()
          $ret += $obj
    }
    return $ret
}
```

## Mitglieder der lokalen Administratoren auflisten

 Ab PowerShell Version 2.0 

```
function CheckLocalAdmins{
    <# Check the Membership in local Admins #>
    $function = $($MyInvocation.MyCommand.Name)
    $ret = @()
    try{
        if($psdebug){write-host "Running $($function) ..." -ForegroundColor Yellow}
        $Computer = [ADSI]"WinNT://$($env:COMPUTERNAME)"
        $Groups = $Computer.psbase.Children | Where {$_.psbase.schemaClassName -eq "group"}
        ForEach ($Group In $Groups){
            if($Group.Name -match 'administrators'){
                $Members = @($Group.psbase.Invoke("Members"))
                ForEach ($Member In $Members){
                    $obj = New-Object PSObject
                    $Class = $Member.GetType().InvokeMember("Class", 'GetProperty', $Null, $Member, $Null)
                    $Name = $Member.GetType().InvokeMember("Name", 'GetProperty', $Null, $Member, $Null)
                    $Path = $Member.GetType().InvokeMember("ADsPath", 'GetProperty', $Null, $Member, $Null)
                    Add-Member -InputObject $obj -MemberType NoteProperty -Name Name -Value $Name
                    Add-Member -InputObject $obj -MemberType NoteProperty -Name Class -Value $Class
                    Add-Member -InputObject $obj -MemberType NoteProperty -Name Path -Value $Path
                    $ret += $obj
                }
            }
        }
    }
    catch [Exception]{
          write-host "$($function): $($_.Exception.Message)" -ForegroundColor Red
          $error.clear()
          $ret += $obj
    }
    return $ret
}
```

## Name to SID

 SID zu einem Namen herausfinden: 

```csharp
function GetSidFromName{
     param(
          [Parameter(Mandatory=$true)][String] $sAMAccountName
     )
     cls
     $objUsr = New-Object System.Security.Principal.NTAccount($sAMAccountName)
     $strSID = $objUsr.Translate([System.Security.Principal.SecurityIdentifier])
     return $strSID.Value
}
GetSidFromName -sAMAccountName (read-host ("Enter sAMAccountName"))

```

## SID to Name

 Name zu einer SID herausfinden: 

```csharp
function GetNameFromSid{
     param(
          [Parameter(Mandatory=$true)][String] $Sid
     )
     cls
     $objSID = New-Object System.Security.Principal.SecurityIdentifier($Sid)
     $objUsr = $objSID.Translate( [System.Security.Principal.NTAccount])
     return $objUsr.Value
}
GetNameFromSid -Sid (read-host ("Enter SID to translate"))

```

## SID to Name with Active Directory

 Will ich mehr Information als nur den Namen, so kann ich diese im Active Directory herausfinden. 

```csharp
function GetNameFromSid{
     param(
          [Parameter(Mandatory=$true)][String] $Sid
     )
     cls
     $objSID = New-Object System.Security.Principal.SecurityIdentifier($Sid)
     $objUsr = $objSID.Translate( [System.Security.Principal.NTAccount])

     #Get User Description from Active Directory
     $objDomainUser = ($objUsr.Value).split('\')
     $objDomain = $objDomainUser[0].replace('-', '.').toLower()
     $sAMAccountName= $objDomainUser[1]

     $root = [ADSI]''
     $searcher = new-object     System.DirectoryServices.DirectorySearcher($root)
     $searcher.filter = "(&(objectClass=user)(sAMAccountName=$sAMAccountName))"
     $aduser = $searcher.findall()
     $aduser | % {
         $dn = $_.Path
     }
     return [ADSI]$dn | select sAMAccountName, Description, MemberOf | ft -auto
}
GetNameFromSid -Sid (read-host ("Enter SID to translate"))

```

## Who is that?

 Ich habe öfters mal das Problem, dass ich mich per RDP auf einen Server anmelden möchte. Doch da sind bereits zwei andere Accounts angemeldet und ich kenne die zugehörenden Namen nicht, denn es wird nur der sAMAccountName angezeigt. Damit ist nun aber Schluss: 

```csharp
#Get User Properties from the current domain
function GetUserProperties{
     param(
          [Parameter(Mandatory=$true)][String] $sAMAccountName
     )
     cls
     "Get User Properties from the current domain:"
     $root = [ADSI]''
     $searcher = new-object System.DirectoryServices.DirectorySearcher($root)
     $searcher.filter = "(&(objectClass=user)(sAMAccountName=$sAMAccountName))"
     $aduser = $searcher.findall()
     $aduser | % {$dn = $_.Path}
     [ADSI]$dn | select sn, givenName, Name, sAMAccountName, userPrincipalName, `
      Description | ft -auto
     $user = [ADSI]$dn
     write-host "Member Of:"
     $user.MemberOf |% {([ADSI]"LDAP://$_") | Select Name, Description}
}
GetUserProperties -sAMAccountName (read-host ("Enter sAMAccountName"))

```

## Active Directory User

 Schnell im AD prüfen ob ein User gesperrt ist: 

```
if(-not(Get-Module -Name ActiveDirectory)){
    Import-Module ActiveDirectory
}
$aduser = 'MyUser'
Get-ADUser -Identity $aduser -Properties LockedOut | Select-Object Name, LockedOut
```

 Prüfen ob mehrere Users gesperrt sind: 

```
Search-ADAccount -Locked | Select-Object Name, LockedOut, LastLogonDate
```

 User entsperren: 

```
Unlock-ADAccount -Identity $aduser
```