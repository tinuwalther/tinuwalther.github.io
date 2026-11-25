---
title: Kerberos Token
date: '2024-08-14T10:20:43+02:00'
author: Tinu
excerpt: Kerberos - ein bösartiger dreiköpfiger Hund, der den Eingang zu den Applikationen
  bewacht. Probleme mit dem Kerberos Token treten auf, wenn ein Benutzer in zu vielen
  Gruppen Mitglied ist.
categories:
- Active Directory
tags:
- Authentication
- Kerberos
image: /assets/wiki/erstelle-ein-image-von-einem-kerberos-hund-in-blau-und.png
wordpress_id: 4172
layout: post
permalink: /wiki/kerberos-token/
render_with_liquid: false
---

# -DRAFT-

Probleme mit dem Kerberos Token treten auf, wenn ein Benutzer in zu vielen Gruppen Mitglied ist, oder wenn ein altes Betriebssystem/Applikation eingesetzt wird, welches weniger als 48'000 Bytes als MaxTokenSize konfiguriert hat.

Die Auswirkung einer Überschreitung des Tokens führt dazu, dass nicht alle Gruppen in der PAC (Privilege Account Certificate) abgebildet werden können und daher fehlen.

## Symptome

Wenn ein Benutzer versucht, sich mit einem Domänenbenutzerkonto bei einem Computer/System anzumelden, kann die Anmeldeanforderung fehlschlagen. Sie erhalten dann eine der folgenden Fehlermeldungen:

*The system cannot log you on due to the following error: During a logon attempt, the user's security context accumulated too many security IDs. Please try again or consult your system administrator.*

*HTTP 400 - Bad Request (Request Header too long)*

Applications and the security event log ID 4625 may display this error code:

```
0xc000015a
```

The error is STATUS\_TOO\_MANY\_CONTEXT\_IDS

## Limiten in Windows

MaxTokenSize in Windows Server 2012 und höher: 48.000 Byte

Hard Limit von Gruppen in Windows: 1010 Gruppen

## Tokensize Berechnung

TokenSize = 1200 + 40d + 8s

- **1200**. The estimated **overhead** value for a Kerberos ticket. This value can vary, depending on factors such as the length of the DNS domain name and the length of the client name.
- **d**. The sum of the following values:
    - The number of memberships in universal groups that are **outside** the user's account domain.
    - The number of SIDs stored in the account's sIDHistory attribute. This value counts group memberships and user SIDs.
- **s**. The sum of the following values:
    - The number of memberships in universal groups that are **inside** the user's account domain.
    - The number of memberships in domain-local groups.
    - The number of memberships in global groups

## PowerShell Script



```powershell
# Get current user context
$token = [System.Security.Principal.WindowsIdentity]::GetCurrent()
$groupName = foreach($sid in $token.Groups) {
    try {
        ($sid).Translate([System.Security.Principal.NTAccount])
    } catch {
        "Could not translate $($sid.Value). Reason: $($_.Exception.Message)"
        $Error.Clear()
    }
}

[PSCustomObject]@{
    Authenication = $token.AuthenticationType
    Name = $token.Name
    Token = $token.Token
    Groups = $token.Groups.Count
    SID = $token.Groups
    MemberOf = $groupName
}

```

## Hints

Trusted for Delegation (alle Angaben ausser dem Overhead müssen mit dem doppelten Wert gerechnet werden)

SIDHistory (remove the SIDHistory attribute from these accounts)

WellKnown SIDs (Everyone, BUILTIN\\Users, Domain\\Domain Users, etc)

SID Compression (nicht alle Applikationen/Systeme können damit umgehen)

## Lösungen

Anzahl Gruppen verkleinern, SID Compression konfigurieren, ...

### Rollen Konzept überarbeiten

Abweichen vom Microsoft Grundprinzip A-G-D-L-P (Accounts, Global Groups, Domain Local Groups, Permissions). Damit kann die Gruppenmitgliedschaft eines Accounts oft halbiert werden.

Anstelle von **User -&gt; Domain Global Group -&gt; Domain Local Group -&gt; Applikation-/System interne Security Group** (darauf wird die Permission vergeben) nur **User -&gt; Domain Global Group -&gt; Applikation-/System interne Security Group** oder wenn Permissions direkt auf Domain Groups vergeben werden **User -&gt; Domain Local Group -&gt; Permission** vergeben.

Die Rolle wird in einem **IAM-Tool** (Identity &amp; Access Management) mit eigener Datenbank gebildet und enthält die Rolle, z.B. **Virtualization Admin** welche die Berechtigungen (Active Directory Gruppen) **VMware Admin**, **Hyper-V Admin** und alles was die Mitarbeitenden vom Team Virtualization zum Arbeiten benötigen enthält.



| User (AD) | Team | IAM-Rolle | Berechtigungen (Gruppen im AD) |
|---|---|---|---|
| account@company.local | Cloud &amp; Virtualization | Cloud Virtualization Admins | VMware Admins, Hyper-V Admins, Jira User, CyberArk Virtualization, Cloud Portal Admins, M365-Users |

<div class="wp-block-wp-mermaid-block mermaid">--- title: Entity Relationship Diagrams --- erDiagram User &#124;&#124;--&#124;{ TeamVirtualizationAndCloud : memberOf User { string Name key TeamId } TeamVirtualizationAndCloud { string Manager key IAMRoleId } TeamVirtualizationAndCloud &#124;&#124;--&#124;{ IAMRoleCloudVirtualizationAdmins: has IAMRoleCloudVirtualizationAdmins { key IAMRoleId group VMwareAdmins group HyperVAdmins group JiraUsers group CyberArkVirtuaization group CloudPortalAdmins group M365Users } </div>## Links

[Problems with Kerberos authentication when a user belongs to many groups](https://learn.microsoft.com/en-us/troubleshoot/windows-server/windows-security/kerberos-authentication-problems-if-user-belongs-to-groups)

[Logging on a user account that is a member of more than 1,010 groups may fail on a Windows Server-based computer](https://learn.microsoft.com/en-us/troubleshoot/windows-server/windows-security/logging-on-user-account-fails)