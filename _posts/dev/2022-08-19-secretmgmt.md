---
layout: post
title:  "Microsoft Secret Management"
author: Tinu
categories: "PowerShell-Basic"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Secret Management](#secret-management)
  - [Work with the SecretStore module as a SecretVault](#work-with-the-secretstore-module-as-a-secretvault)
    - [Install the modules for SecretStore](#install-the-modules-for-secretstore)
    - [Register Module](#register-module)
    - [SecretStore configuration](#secretstore-configuration)
    - [Get SecretVault](#get-secretvault)
    - [Adding and retrieving secrets](#adding-and-retrieving-secrets)
    - [Retrieve a secret and use it as PSCredential-Object](#retrieve-a-secret-and-use-it-as-pscredential-object)
    - [Remove SecretVault](#remove-secretvault)
    - [Unregister SecretVault](#unregister-secretvault)
  - [Work with the Keepass module as a SecretVault](#work-with-the-keepass-module-as-a-secretvault)
    - [Install the modules for KeePass](#install-the-modules-for-keepass)
    - [Register Module](#register-module-1)
    - [Get SecretVault](#get-secretvault-1)
    - [Set KeePass as DefaultVault](#set-keepass-as-defaultvault)
    - [Unlock SecretVault](#unlock-secretvault)
    - [Retrieving SecretInfo](#retrieving-secretinfo)
    - [Retrieve a secret and use it as PSCredential-Object](#retrieve-a-secret-and-use-it-as-pscredential-object-1)
    - [Retrieve a secret and use it as PlainText](#retrieve-a-secret-and-use-it-as-plaintext)
  - [Full Example on AlmaLinux](#full-example-on-almalinux)
    - [Create Docker Container](#create-docker-container)
    - [Install and configure KeePass](#install-and-configure-keepass)
    - [Install and configure SecretManagement for KeePass](#install-and-configure-secretmanagement-for-keepass)
    - [Adding and retrieving secrets from KeePass](#adding-and-retrieving-secrets-from-keepass)
- [See also](#see-also)

# Secret Management

Use [Microsoft.PowerShell.SecretManagement](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.secretmanagement/?view=ps-modules) and do not store passwords in files!

This module provides a convenient way for a user to store and retrieve secrets. The secrets are stored in registered extension vaults. An extension vault can store secrets locally or remotely. SecretManagement coordinates access to the secrets through the registered vaults.

SecretManagement extension vaults:

- Microsoft.PowerShell.SecretStore
- SecretManagement.CyberArk (needs [psPAS](https://www.powershellgallery.com/packages/psPAS))
- SecretManagement.KeePass
- and more

## Work with the SecretStore module as a SecretVault

### Install the modules for SecretStore

````powershell
Install-Module Microsoft.PowerShell.SecretManagement, Microsoft.PowerShell.SecretStore -Verbose
````

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

[ [Top](#table-of-contents) ] 

## Work with the Keepass module as a SecretVault

### Install the modules for KeePass

````powershell
Install-Module Microsoft.PowerShell.SecretManagement, SecretManagement.KeePass -Verbose
````

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

[ [Top](#table-of-contents) ] 

## Full Example on AlmaLinux

For this full example with AlmaLinux, you can use my Project [PSAutoMic](https://github.com/tinuwalther/PSAutoMic) to create the Docker-Container.

### Create Docker Container

Create a Docker-Image and Docker-Container with installed PowerShell and start the container:

````bash
docker start alma_container
docker exec -it alma_container pwsh
````

````bash
sh-5.1# pwsh
PowerShell 7.3.4
Get-OsInfo

DistName      : AlmaLinux
DistVersion   : 9.2 (Turquoise Kodkod)
SupportURL    : https://almalinux.org/
OS            : GNU/Linux
KernelRelease : 5.15.90.1-microsoft-standard-WSL2
OSInstallDate : 2023-06-02
````

### Install and configure KeePass

Install config-manager, EPEL-repository, and keepassxc:

````bash
dnf install 'dnf-command(config-manager)'
dnf config-manager --set-enabled crb
dnf install epel-release
dnf install keepassxc
````

Create a KeePassDB-file:

````bash
Usage: keepassxc-cli db-create [options] database
Create a new database.

Options:
  -q, --quiet                   Silence password prompt and other secondary outputs.
  --set-key-file <path>         Set the key file for the database.
  -p, --set-password            Set a password for the database.
  -t, --decryption-time <time>  Target decryption time in MS for the database.
  -h, --help                    Display this help.

Arguments:
  database                      Path of the database.
````

I use a master-password for the database and it should be located at the home directory. You can use any volume for the location of the database to share it.

````bash
keepassxc-cli db-create --set-password /home/KeePassDB.kdbx

Couldn't load translations.
Enter password to encrypt database (optional): <your master-password>
Repeat password: <your master-password>
Successfully created new database.
````

### Install and configure SecretManagement for KeePass

Install the SecretManagement.Keepass and all dependencies:

````powershell
Install-Module SecretManagement.Keepass -Verbose
...
VERBOSE: InstallPackage' - name='Microsoft.PowerShell.SecretManagement', version='1.1.2',destination='/tmp/311771630'  
VERBOSE: InstallPackage' - name='PSFramework', version='1.7.270',destination='/tmp/311771630'                           
VERBOSE: InstallPackage' - name='SecretManagement.KeePass', version='0.9.2',destination='/tmp/311771630'                
...
VERBOSE: Module 'SecretManagement.KeePass' was installed successfully to path '/root/.local/share/powershell/Modules/SecretManagement.KeePass/0.9.2'.
````

Register the SecretVault, and set it to the default vault, and activate the master-password option:

````powershell
cd home
Register-SecretVault -Name "KeePassDB" -ModuleName "SecretManagement.Keepass" -VaultParameters @{
    Path = "/home/KeePassDB.kdbx"
    UseMasterPassword = $true
    DefaultVault = $true
}
````

````powershell
Get-SecretVault

Name      ModuleName               IsDefaultVault
----      ----------               --------------
KeePassDB SecretManagement.KeePass True
````

### Adding and retrieving secrets from KeePass

Unlock the KeePassDB:

````powershell
Unlock-SecretVault -Name KeePassDB

cmdlet Unlock-SecretVault at command pipeline position 1
Supply values for the following parameters:
Password: <your master-password>
````

Adding a secret:

````powershell
$cred = Get-Credential

PowerShell credential request
Enter your credentials.
User: Tinu
Password for user Tinu: ***********

Set-Secret -Name $cred.UserName -SecureStringSecret $cred.Password
````

Retrieving secrets:

````powershell
Get-SecretInfo -Vault KeePassDB

Name Type         VaultName
---- ----         ---------
Tinu PSCredential KeePassDB
````

````powershell
$SecretName = "Tinu"
$creds = New-Object System.Management.Automation.PSCredential $SecretName , (Get-Secret -Name $SecretName)

$creds | Format-List

UserName : Tinu
Password : System.Security.SecureString
````

# See also

[Microsoft.PowerShell.SecretManagement](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.secretmanagement/?view=ps-modules/) on docs.microsoft.com, [KeePassXC: User Guide](https://keepassxc.org/docs/KeePassXC_UserGuide#_creating_your_first_database)

[ [Top](#table-of-contents) ] [ [Blog](../categories.html) ]