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
  - [Register the SecretStore module as a SecretVault](#register-the-secretstore-module-as-a-secretvault)
  - [Adding and retrieving secrets](#adding-and-retrieving-secrets)
  - [Retrieve a secret and use it as PSCredential-Object](#retrieve-a-secret-and-use-it-as-pscredential-object)
- [See also](#see-also)

# Secret Management

Use [Microsoft.PowerShell.SecretManagement](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.secretmanagement/?view=ps-modules) and do not store passwords in files!

This module provides a convenient way for a user to store and retrieve secrets. The secrets are stored in registered extension vaults. An extension vault can store secrets locally or remotely. SecretManagement coordinates access to the secrets through the registered vaults.

SecretManagement extension vaults:

- Microsoft.PowerShell.SecretStore
- SecretManagement.CyberArk (needs [psPAS](https://github.com/pspete/psPAS)) -> **Innovation Day!**
- SecretManagement.KeePass
- and more

## Install the modules

````powershell
Install-Module Microsoft.PowerShell.SecretManagement, Microsoft.PowerShell.SecretStore
````

## SecretStore configuration

````powershell
Get-SecretStoreConfiguration

Vault Microsoft.PowerShell.SecretStore requires a password.
Enter password:
****

      Scope Authentication PasswordTimeout Interaction
      ----- -------------- --------------- -----------
CurrentUser       Password             900      Prompt
````

## Register the SecretStore module as a SecretVault

````powershell
Register-SecretVault -ModuleName Microsoft.PowerShell.SecretStore -Name MyOwnStore

Get-SecretVault

Name          ModuleName                       IsDefaultVault
----          ----------                       --------------
MyOwnStore Microsoft.PowerShell.SecretStore True
````

## Adding and retrieving secrets

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

````powershell
Remove-Secret -Vault MyOwnStore -Name tinu@gmx.net

Vault MyOwnStore requires a password.
Enter password:
****
````

## Retrieve a secret and use it as PSCredential-Object

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

# See also

[Microsoft.PowerShell.SecretManagement](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.secretmanagement/?view=ps-modules/) on docs.microsoft.com

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]