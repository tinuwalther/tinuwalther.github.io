---
layout: post
title:  "Microsoft Secret Management"
author: Tinu
categories: "PowerShell-Basic"
tags:   PowerShell News
permalink: /posts/:title:output_ext
---

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Secret Management](#secret-management)
  - [Install the modules](#install-the-modules)
  - [Work with the SecretStore module as a SecretVault](#work-with-the-secretstore-module-as-a-secretvault)
    - [Register Module](#register-module)
    - [SecretStore configuration](#secretstore-configuration)
    - [Get SecretVault](#get-secretvault)
    - [Adding and retrieving secrets](#adding-and-retrieving-secrets)
    - [Retrieve a secret and use it as PSCredential-Object](#retrieve-a-secret-and-use-it-as-pscredential-object)
    - [Remove SecretVault](#remove-secretvault)
    - [Unregister SecretVault](#unregister-secretvault)
  - [Work with the Keepass module as a SecretVault](#work-with-the-keepass-module-as-a-secretvault)
    - [Register Module](#register-module-1)
    - [Get SecretVault](#get-secretvault-1)
    - [Set KeePass as DefaultVault](#set-keepass-as-defaultvault)
    - [Unlock SecretVault](#unlock-secretvault)
    - [Retrieving SecretInfo](#retrieving-secretinfo)
    - [Retrieve a secret and use it as PSCredential-Object](#retrieve-a-secret-and-use-it-as-pscredential-object-1)
    - [Retrieve a secret and use it as PlainText](#retrieve-a-secret-and-use-it-as-plaintext)
- [See also](#see-also)

# Secret Management

Use [Microsoft.PowerShell.SecretManagement](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.secretmanagement/?view=ps-modules) and do not store passwords in files!

This module provides a convenient way for a user to store and retrieve secrets. The secrets are stored in registered extension vaults. An extension vault can store secrets locally or remotely. SecretManagement coordinates access to the secrets through the registered vaults.

SecretManagement extension vaults:

- Microsoft.PowerShell.SecretStore
- SecretManagement.CyberArk (needs [psPAS](https://github.com/pspete/psPAS))
- SecretManagement.KeePass
- and more

## Install the modules

````powershell
Install-Module Microsoft.PowerShell.SecretManagement, Microsoft.PowerShell.SecretStore, SecretManagement.KeePass -Verbose
````

## Work with the SecretStore module as a SecretVault

### Register Module

````powershell
Register-SecretVault -ModuleName Microsoft.PowerShell.SecretStore -Name MyOwnStore
````


### SecretStore configuration

List the configuration:

````powershell
Get-SecretStoreConfiguration

Vault Microsoft.PowerShell.SecretStore requires a password.
Enter password:
****

      Scope Authentication PasswordTimeout Interaction
      ----- -------------- --------------- -----------
CurrentUser       Password             900      Prompt
````

Change the password-timeout to 1 hour:

````powershell
Set-SecretStoreConfiguration -Scope CurrentUser -Authentication Password -PasswordTimeout 3600 -Interaction Prompt
````

### Get SecretVault

````powershell
Get-SecretVault

Name          ModuleName                       IsDefaultVault
----          ----------                       --------------
MyOwnStore    Microsoft.PowerShell.SecretStore True
````

### Adding and retrieving secrets

````powershell
$cred = Get-Credential
Set-Secret -Name $cred.UserName -SecureStringSecret $cred.Password -Metadata @{ URL = 'https://gmx.net' } 

PowerShell credential request
Enter your credentials.
User: tinu@gmx.net
Password for user tinu@gmx.net: ********

Vault MyOwnStore requires a password.
Enter password:
****
````

````powershell
Get-Secret -Name tinu@gmx.net -AsPlainText

1234@gmx
````

````powershell
Get-Secretinfo -Name tinu*

Name           Type         VaultName
----           ----         ---------
tinu@gmx.net   SecureString MyOwnStore
tinu@hotmail   SecureString MyOwnStore
tinu@microsoft SecureString MyOwnStore
````

````powershell
Get-Secretinfo -Name tinu* | % { @{$_.Name=Get-Secret -Name $Name -AsPlainText} }

Name                           Value
----                           -----
tinu@gmx.net                   1234@gmx
tinu@hotmail                   1234@gmx
tinu@microsoft                 1234@gmx
````

````powershell
Get-SecretInfo -Name tinu@gmx.net | fl *

Name      : tinu@gmx.net
Type      : SecureString
VaultName : MyOwnStore
Metadata  : {[URL, https://gmx.net]}
````

````powershell
Get-SecretInfo -Name tinu@gmx.net | Select-Object -ExpandProperty Metadata

Key         Value
---         -----
ExpireAfter 2022-06-24 20:00:00
Url         https://gmx.net
````

### Retrieve a secret and use it as PSCredential-Object

First, unlock the secret-store:

````powershell
Unlock-SecretStore
````

In each scripts, put the following code to get the credentials of the given user (secret):

````powershell
$SecretName = "tinu@gmx.net"
[PSCredential] $creds = New-Object System.Management.Automation.PSCredential $SecretName , (Get-Secret -Name $SecretName)
$creds

UserName                         Password
--------                         --------
tinu@gmx.net System.Security.SecureString
````

### Remove SecretVault

Un-registers an extension vault from SecretManagement for the current user.

````powershell
Get-SecretInfo -Vault MyOwnStore
Remove-Secret -Vault MyOwnStore -Name tinu@gmx.net

Vault MyOwnStore requires a password.
Enter password:
****
````

### Unregister SecretVault

Un-registers an extension vault from SecretManagement for the current user.

````powershell
Get-SecretVault
Unregister-SecretVault MyOwnStore
````

## Work with the Keepass module as a SecretVault

### Register Module

````powershell
Register-SecretVault -Name "KeePassDB" -ModuleName "SecretManagement.Keepass" -VaultParameters @{
	Path = "$($env:USERPROFILE)\Documents\KeePassDB.kdbx"
	UseMasterPassword = $true
  DefaultVault = $true
}
````

### Get SecretVault

````powershell
Get-SecretVault

Name        ModuleName                       IsDefaultVault
----        ----------                       --------------
KeePassDB   SecretManagement.Keepass         False
````

### Set KeePass as DefaultVault

Sets the provided vault name as the default vault for the current user.

````powershell
Set-SecretVaultDefault -Name KeePassDB
````

### Unlock SecretVault

First, unlock the secret-vault:

````powershell
Unlock-SecretVault -Name KeePassDB
````

### Retrieving SecretInfo

````powershell
Get-SecretInfo -Vault KeePassDB
Get-SecretInfo -Vault KeePassDB -Name *Token*
````

### Retrieve a secret and use it as PSCredential-Object

````powershell
Get-Secret -Name "Token"

UserName                     Password
--------                     --------
tinu     System.Security.SecureString
````

### Retrieve a secret and use it as PlainText

Retrieve the password of a specified Name and use it as PlainText form the Clipboard:

````powershell
$Name   = "Token"
$Secret = Get-Secret -Name $Name
[System.Net.NetworkCredential]::new($Name, $Secret.Password).Password | Set-Clipboard
````

List all Secrets with the Tag 'Business', and retrieve the password of a specified Name and use it as PlainText form the Clipboard:

````powershell
Write-Host "Get Secret from KeePassDB" -ForegroundColor Green 
if(-not(Test-SecretVault -Name KeePassDB)){
    Unlock-SecretVault -Name KeePassDB
}

$SecretInfo = Get-SecretInfo -Vault KeePassDB -WarningAction SilentlyContinue
$Properties = (
    'Name',
    @{
            N='Accessed'
            E={
                foreach($item in $_.Metadata.keys){
                    if($item -match 'Accessed'){$($_.Metadata[$item])}
                }
            }
        },
    @{
            N='Tags'
            E={
                foreach($item in $_.Metadata.keys){
                    if($item -match 'Tags'){$($_.Metadata[$item])}
                }
            }
        }
)
$SecretInfo | Select $Properties | Where Tags -match 'Business' | Out-String

$Name   = Read-Host "Paste the FullName to search"
$Secret = Get-Secret -Vault PrivatKdbx -Name $Name
[System.Net.NetworkCredential]::new($Name, $Secret.Password).Password | Set-Clipboard
Write-Host "Set the password to the Clipboard. " -ForegroundColor Green -NoNewline
Read-Host -Prompt "Press any key to exit"
````

````
Get Secret from KeePassDB

Keepass Master Password
Enter the Keepass Master password for: C:\Users\Secret\Documents\KeePassDB.kdbx
Password for user Keepass Master Password: ********


Name                Accessed            Tags
----                --------            ----
Test for any access 03.09.2022 10:56:46 Business


Enter the FullName to search: Test for any access
Set the password to the Clipboard. Press any key to exit:
````

# See also

[Microsoft.PowerShell.SecretManagement](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.secretmanagement/?view=ps-modules/) on docs.microsoft.com

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]