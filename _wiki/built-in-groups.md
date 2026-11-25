---
title: Built in Groups
date: '2015-02-25T08:48:54+01:00'
author: Tinu
excerpt: ''
categories:
- Active Directory
tags:
- Groups
wordpress_id: 795
layout: post
permalink: /wiki/built-in-groups/
render_with_liquid: false
---

## Builtin local Groups

 -&gt; [Technet](https://technet.microsoft.com/en-us/library/cc771990(v=ws.11).aspx) The following table provides descriptions of the default groups that are located in the Groups folder. The table also lists the default user rights for each group. These user rights are assigned in the local security policy. 

### Administrators

 Members of this group have full control of the computer, and they can assign user rights and access control permissions to users as necessary. The Administrator account is a default member of this group. When a computer is joined to a domain, the Domain Admins group is added to this group automatically. **Because this group has full control of the computer, use caution when you add users to it.**

- Access this computer from the network
- Adjust memory quotas for a process
- Allow logon locally
- Allow logon through Remote Desktop Services
- Back up files and directories
- Bypass traverse checking
- Change the system time
- Change the time zone
- Create a page file
- Create global objects
- Create symbolic links
- Debug programs
- Force shutdown from a remote system
- Impersonate a client after authentication
- Increase scheduling priority
- Load and unload device drivers
- Log on as a batch job
- Manage auditing and security log
- Modify firmware environment variables
- Perform volume maintenance tasks
- Profile single process
- Profile system performance
- Remove computer from docking station
- Restore files and directories
- Shut down the system
- Take ownership of files or other objects
 

### Backup Operators

 Members of this group can back up and restore files on a computer, regardless of any permissions that protect those files. This is because the right to perform a backup takes precedence over all file permissions. Members of this group cannot change security settings. 

- Access this computer from the network
- Allow logon locally
- Back up files and directories
- Bypass traverse checking
- Log on as a batch job
- Restore files and directories
- Shut down the system
 

### Cryptographic Operators

 Members of this group are authorized to perform cryptographic operations. 

- No default user rights
 

### Distributed COM Users

 Members of this group are allowed to start, activate, and use DCOM objects on a computer. 

- No default user rights
 

### Guests

 In a computer joined to the domain, members of this group have a temporary profile created at log on, and when the member logs off, the profile is deleted. Profiles in workgroup environments are not deleted. The Guest account (which is disabled by default) is also a default member of this group. 

- No default user rights
 
 Members of this group will have a temporary profile created at log on, and when the member logs off, the profile will be deleted. The Guest account (which is disabled by default) is also a default member of this group. 

### IIS\_IUSRS

 This is a built-in group that is used by Internet Information Services (IIS). 

- No default user rights
 

### Network Configuration Operators

 Members of this group can make changes to TCP/IP settings, and they can renew and release TCP/IP addresses. This group has no default members. • No default user rights 

### Performance Log Users

 Members of this group can manage performance counters, logs, and alerts on a computer — both locally and from remote clients — without being a member of the Administrators group. 

- No default user rights
 

### Performance Monitor Users

 Members of this group can monitor performance counters on a computer — locally and from remote clients — without being a member of the Administrators group or the Performance Log Users groups 

- No default user rights
 

### Power Users

 By default, members of this group have no more user rights or permissions than a standard user account. 

- No default user rights
 
 The Power Users group in previous versions of Windows was designed to give users specific administrator rights and permissions to perform common system tasks. In this version of Windows, standard user accounts inherently have the ability to perform most common configuration tasks, such as changing time zones. For legacy applications that require the same Power User rights and permissions that were present in previous versions of Windows, administrators can apply a security template that enables the Power Users group to assume the same rights and permissions that were present in previous versions of Windows. 

### Remote Desktop Users

 Members of this group can log on to the computer remotely. • Allow logon through Remote Desktop Services 

### Replicator

 This group supports replication functions. The only member of the Replicator group should be a domain user account that is used to log on the Replicator services of a domain controller. Do not add user accounts of actual users to this group. 

- No default user rights
 

### Users

 Members of this group can perform common tasks, such as running applications, using local and network printers, and locking the computer. Members of this group cannot share directories or create local printers. By default, the Domain Users, Authenticated Users, and Interactive groups are members of this group. Therefore, any user account that is created in the domain becomes a member of this group. 

- Access this computer from the network
- Allow logon locally
- Bypass traverse checking
- Change the time zone
- Increase a process working set
- Remove the computer from a docking station
- Shut down the system
 

### Offer Remote Assistance Helpers

 Members of this group can offer Remote Assistance to the users of this computer. 

- No default user rights
 

## Builtin Groups im Active Directory

 -&gt; [Technet](https://technet.microsoft.com/en-us/library/cc756898(v=ws.10).aspx "Default groups: Active Directory")

### Account Operators

- Members of this group can create, modify, and delete accounts for users, groups, and computers located in the Users or Computers containers and organizational units in the domain, except the Domain Controllers organizational unit.
- Members of this group do not have permission to modify the Administrators or the Domain Admins groups, nor do they have permission to modify the accounts for members of those groups.
- Members of this group can log on locally to domain controllers in the domain and shut them down.
- Because this group has significant power in the domain, add users with caution.
- For Cross-forest-membership see [Domain Local Group](/wiki/cross-forest-zugriff/#domain_local_group "Cross-Forest Zugriff")
 

### Administrators

- Members of this group have full control of all domain controllers in the domain.
- By default, the Domain Admins and Enterprise Admins groups are members of the Administrators group.
- The Administrator account is also a default member.
- Because this group has full control in the domain, add users with caution.
- For Cross-forest-membership see [Domain Local Group](/wiki/cross-forest-zugriff/#domain_local_group "Cross-Forest Zugriff")
 

### Backup Operators

- Members of this group can back up and restore all files on domain controllers in the domain, regardless of their own individual permissions on those files.
- Backup Operators can also log on to domain controllers and shut them down.
- This group has no default members.
- Because this group has significant power on domain controllers, add users with caution.
- For Cross-forest-membership see [Domain Local Group](/wiki/cross-forest-zugriff/#domain_local_group "Cross-Forest Zugriff")
 

### DHCP Administrators

- Members of the DHCP Administrators group can view and modify any data at the DHCP server.
- DHCP Administrators can create and delete scopes, add reservations, change option values, create superscopes, or perform any other activity needed to administer the DHCP server, including export or import of the DHCP server configuration and database.
- For Cross-forest-membership see [Domain Local Group](/wiki/cross-forest-zugriff/#domain_local_group "Cross-Forest Zugriff")
 

### DnsAdmins (installed with DNS)

- Members of this group have administrative access to the DNS Server service.
- This group has no default members.
- For Cross-forest-membership see [Domain Local Group](/wiki/cross-forest-zugriff/#domain_local_group "Cross-Forest Zugriff")
 

### Domain Admins

- Members of this group have **full control of the domain** (dc=contoso,dc=com).
- By default, this group is a member of the Administrators group on all domain controllers, all domain workstations, and all domain member servers at the time they are joined to the domain.
- By default, the Administrator account is a member of this group.
- Because the group has full control in the domain, add users with caution.
- For Cross-forest-membership see [Global Group](/wiki/cross-forest-zugriff/#global_group "Cross-Forest Zugriff")
 

### Enterprise Admins

- Administration aller Objekte im Naming-Kontext, z.B. Exchange, Sites and Services, etc.
- Members of this group have **full control of all domains in the forest** (cn=Configuration,dc=contoso,dc=com).
- By default, this group is a member of the Administrators group on all domain controllers in the forest.
- By default, the Administrator account is a member of this group.
- Because this group has full control of the forest, add users with caution.
- For Cross-forest-membership see [Universal Group](/wiki/cross-forest-zugriff/#universal_group "Cross-Forest Zugriff")
 

### Group Policy Creator Owners

- Members of this group can **modify Group Policy** in the domain.
- By default, the Administrator account is a member of this group.
- Because this group has significant power in the domain, add users with caution.
- For Cross-forest-membership see [Global Group](/wiki/cross-forest-zugriff/#global_group "Cross-Forest Zugriff")
 

### Remote Desktop Users

- Members of this group can remotely log on to **domain controllers** in the domain.
- This group has no default members.
- For Cross-forest-membership see [Domain Local Group](/wiki/cross-forest-zugriff/#domain_local_group "Cross-Forest Zugriff")
 

### Schema Admins

- Members of this group can modify the **Active Directory schema** (cn=Schema,cn=Configuration,dc=contoso,dc=com).
- By default, the Administrator account is a member of this group.
- Because this group has significant power in the forest, add users with caution.
- For Cross-forest-membership see [Universal Group](/wiki/cross-forest-zugriff/#universal_group "Cross-Forest Zugriff")
 

### Server Operators

- **On domain controllers**, members of this group can log on interactively, create and delete shared resources, start and stop some services, back up and restore files, format the hard disk, and shut down the computer.
- This group has no default members.
- Because this group has significant power on domain controllers, add users with caution.
- For Cross-forest-membership see [Domain Local Group](/wiki/cross-forest-zugriff/#domain_local_group "Cross-Forest Zugriff")