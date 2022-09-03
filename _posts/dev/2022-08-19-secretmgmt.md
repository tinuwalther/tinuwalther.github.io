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
  - [SecretStore configuration](#secretstore-configuration)
  - [Work with the SecretStore module as a SecretVault](#work-with-the-secretstore-module-as-a-secretvault)
    - [Register Module](#register-module)
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
Install-Module Microsoft.PowerShell.SecretManagement, Microsoft.PowerShell.SecretStore, SecretManagement.KeePass
````

## SecretStore configuration

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

## Work with the SecretStore module as a SecretVault

### Register Module

````powershell
Register-SecretVault -ModuleName Microsoft.PowerShell.SecretStore -Name MyOwnStore
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

````powershell
$Name   = "Token"
$Secret = Get-Secret -Name $Name
[System.Net.NetworkCredential]::new($Name, $Secret.Password).Password | Set-Clipboard
````

# See also

[Microsoft.PowerShell.SecretManagement](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.secretmanagement/?view=ps-modules/) on docs.microsoft.com

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]