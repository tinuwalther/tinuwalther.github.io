---
title: Userinteraktion
date: '2014-11-26T21:47:23+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Userinteraktion
wordpress_id: 171
layout: post
permalink: /wiki/userinteraktion/
render_with_liquid: false
---

# Benutzereingabe

Abfrage auf der Commandline: 

```csharp
$name = read-host ('Enter your name')
```

Abfrage des Passwortes auf der Commandline: 

```csharp
read-host -AsSecureString 'Enter the password'
```

Umwandeln des SecureStrings in Cleartext: 

```csharp
$spwd = read-host -AsSecureString "Enter the password for $($userid)"
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($spwd)
$cpwd = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
```

Save credentials to a file 

```csharp
$savecreds = Get-Credential
$savecreds.GetType()
$savecreds | Export-CliXml 'C:\Temp\user.xml'

```

Read credentials from a file 

```csharp
$readcreds = Import-Clixml 'C:\Temp\user.xml'
$readcreds.GetType()
$readcreds.UserName.GetType()
$readcreds.Password.GetType()

```

Note that the secret used to encrypt and decrypt the data is composed of your identity and your machine identity, so the encrypted text can only be read by you, and only on the machine where it was originally encrypted. 


# Benutzerausgabe

Normale Ausgabe: 

```csharp
write-host $name

```

Ausgabe in gelber Schrift: 

```csharp
write-host $name -ForegroundColor Yellow
```