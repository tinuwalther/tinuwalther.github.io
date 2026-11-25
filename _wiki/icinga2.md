---
title: Icinga2
date: '2016-12-17T18:23:55+01:00'
author: Tinu
excerpt: ''
categories:
- Monitoring
tags:
- Open Source
wordpress_id: 1830
layout: post
permalink: /wiki/icinga2/
render_with_liquid: false
---

Mein Provider lässt etc nicht zu, also ersetze usw mit etc.

## Pre Requisites

### DNS Eintrag

 Icinga in hosts-file oder DNS hinzufügen. 

```
# sudo vim /usw/hosts
# 127.0.0.1 icinga localhost localhost.localdomain localhost4 localhost4.localdomain4
```

###  Firewall Rule

```
# firewall-cmd --state
running

# firewall-cmd --get-active-zones
public

# firewall-cmd --permanent --zone=public --add-service=http
# firewall-cmd --permanent --zone=public --add-service=https
# firewall-cmd --permanent --zone=public --add-port=2888/tcp 
# firewall-cmd --permanent --zone=public --add-port=3888/tcp 
# firewall-cmd --reload
# firewall-cmd --list-all
```

### SELINUX disablen

```
# cat /usw/selinux/config | grep SELINUX=
# SELINUX= can take one of these three values:
SELINUX=enforcing
# sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /usw/selinux/config
# cat /usw/selinux/config | grep SELINUX=
# SELINUX= can take one of these three values:
SELINUX=disabled
```

 After that you will have to restart the server. 

### Install php-ldap

```
# yum install php-ldap
```

### Configure Timezone

```
# vim /usw/php.ini
[Date]
date.timezone = Europe/Zurich
```

## Install Icinga repository

### EPEL Repository

 The packages for RHEL/CentOS depend on other packages which are distributed as part of the EPEL repository. 

```
# yum install epel-release
```

### Icinga Repository RHEL/CentOS 7

```
# rpm -i http://packages.icinga.org/epel/7/release/noarch/icinga-rpm-release-7-1.el7.centos.noarch.rpm
```

### Install Icinga2

```
# yum install icinga2
```

### Start Icinga2

 Run the following commands to Enable, Start and check the the status of Icinga 2 service on Centos 7 

```
# systemctl enable icinga2
# systemctl start icinga2
# systemctl status icinga2
```

### Configuration Syntax Highlighting using Vim

```
# yum install vim-icinga2
```

### Configuring DB IDO MySQL

```
# yum install mariadb-server mariadb
# systemctl enable mariadb
# systemctl start mariadb
# mysql_secure_installation
...
Leave Password blank to set a new Password!
...
Set root password? [Y/n] Y
...
Remove anonymous users? [Y/n] Y
...
Disallow root login remotely? [Y/n] Y
...
Remove test database and access to it? [Y/n] Y
...
Reload privilege tables now? [Y/n] Y
```

### Installing the IDO modules for MySQL

```
# yum install icinga2-ido-mysql
```

### Setting up the MySQL database

```
# mysql -u root -p
Enter password: 
Welcome to the MariaDB monitor. Commands end with ; or \g.
MariaDB [(none)]> 
MariaDB [(none)]> CREATE DATABASE icinga;
Query OK, 1 row affected (0.03 sec)
MariaDB [(none)]> GRANT SELECT, INSERT, UPDATE, DELETE, DROP, CREATE VIEW, INDEX, EXECUTE ON icinga.* TO 'icinga'@'localhost' IDENTIFIED BY 'icinga';
Query OK, 0 rows affected (0.04 sec)
MariaDB [(none)]> quit
Bye
```

### Import the Icinga 2 IDO schema

```
# mysql -u root -p icinga < /usr/share/icinga2-ido-mysql/schema/mysql.sql 
Enter password:
```

### Enabling the IDO MySQL module

```
# icinga2 feature enable ido-mysql
# systemctl restart icinga2
```

## Install Webserver

 RHEL/CentOS 7/Fedora: 

```
# yum install httpd
# systemctl enable httpd
# systemctl start httpd
```

 The following example installs Apache2 as web server, MySQL as RDBMS and uses the PHP adapter for MySQL. Adopt the package requirements to your needs (e.g. adding ldap for authentication) and distribution. 

```
# yum install httpd mysql-server
# yum install php php-gd php-intl php-ZendFramework php-ZendFramework-Db-Adapter-Pdo-Mysql
```

### Firewall Rules

```
# firewall-cmd --add-service=http
# firewall-cmd --permanent --add-service=http
```

### Setting up Check Plugins

```
# yum install nagios-plugins-all
```

### Setting Up External Command Pipe

```
# icinga2 feature enable command
 Enabling feature command. Make sure to restart Icinga 2 for these changes to take effect.
 # systemctl restart icinga2

# usermod -a -G icingacmd apache
 # id apache
 uid=48(apache) gid=48(apache) groups=48(apache),980(icingacmd)
```

### Icinga Web 2 Installation

```
# yum install icingaweb2 icingacli
# systemctl restart httpd
```

### Configuring the Web Server

 Use icingacli to generate web server configuration for Apache 

```
# icingacli setup config webserver apache --document-root /usr/share/icingaweb2/public
```

 Save the output as new file in your webserver's configuration directory. 

```
# icingacli setup config webserver apache --document-root /usr/share/icingaweb2/public > /usw/httpd/conf.d/icingaweb2.conf
```

 Restart the Webserver 

```
# systemctl restart httpd
```

## Preparing Icinga Web 2 Setup

 Log into Icinga Web http://icinga/icingaweb2/setup 

### Generating a New Setup Token

 If you've got the IcingaCLI installed you can do the following: 

```
# icingacli setup config directory --group icingaweb2; icingacli setup token create;
```

### Modules

 The following modules were found in your Icinga Web 2 installation. To enable and configure a module, just tick it and click "Next". 

- Doc
- Monitoring
- Translation
 

### Icinga Web 2

 Requirements werden geprüft. 

### Authentication

- Database
- LDAP
- External
 

### Database Resource

 Now please configure the database resource where to store users and user groups. Note that the database itself does not need to exist at this time as it is going to be created once the wizard is about to be finished. *Resource Name \* icingaweb\_db* The unique name of this resource Upon its value changing, this field issues an automatic update of this page. *Database Type \* MySQL* The type of SQL database *Host \* localhost* The hostname of the database. For using unix domain sockets, specify localhost *Port* The port to use *Database Name \* icinga\_res* The name of the database to use *Username \* icinga* The user name to use for authentication *Password Password* The password to use for authentication *Character Set* The character set for the database *Persistent* Check this box for persistent database connections. Persistent connections are not closed at the end of a request, but are cached and re-used. This is experimental Upon its value changing, this field issues an automatic update of this page. *Use SSL*

### Database Setup

 It seems that either the database you defined earlier does not yet exist and cannot be created using the provided access credentials, the database does not have the required schema to be operated by Icinga Web 2 or the provided access credentials do not have the sufficient permissions to access the database. Please provide appropriate access credentials to solve this. *Username \* root aus Configuring DB IDO MySQL*  A user which is able to create databases and/or touch the database schema *Password Password*

### Authentication Backend

 As you've chosen to use a database for authentication all you need to do now is defining a name for your first authentication backend. *Backend Name icingaweb2*

### Administration

 Now it's time to configure your first administrative account or group for Icinga Web 2. *Username \* admin* Enter the username to be used when creating an initial administrative account. *Password \** Enter the password to assign to the newly created account. *Repeat password \**

### Application Configuration

 Now please adjust all application and logging related configuration options to fit your needs. Note that choosing "Database" as preference storage causes Icinga Web 2 to use the same database as for authentication. *Show Stacktraces True*  Set whether to show an exception's stacktrace by default. This can also be set in a user's preferences with the appropriate permission. Upon its value changing, this field issues an automatic update of this page. *User Preference Storage Type \* Database*  Upon its value changing, this field issues an automatic update of this page. *Logging Type \* Syslog* The type of logging to utilize. *Logging Level \* Error*  The maximum logging level to emit. *Application Prefix \* icingaweb2*  The name of the application by which to prefix syslog messages. The application prefix must not contain whitespace. *Facility \* User* 

### Welcome to the configuration of the monitoring module for Icinga Web 2!

 This is the core module for Icinga Web 2. It offers various status and reporting views with powerful filter capabilities that allow you to keep track of the most important events in your monitoring environment. 

### Monitoring Backend

 Please configure below how Icinga Web 2 should retrieve monitoring information. *Backend Name \* icinga\_backend* The identifier of this backend *Backend Type \* IDO*

### Monitoring IDO Resource

 Please fill out the connection details below to access the IDO database of your monitoring environment. *Resource Name \* icinga\_ido* The unique name of this resource Upon its value changing, this field issues an automatic update of this page. *Database Type \* MySQL* The type of SQL database *Host \* localhost* The hostname of the database. For using unix domain sockets, specify localhost *Port* The port to use *Database Name \* icinga* The name of the database to use *Username \* icinga* The user name to use for authentication *Password* The password to use for authentication *Character Set* The character set for the database *Persistent* Check this box for persistent database connections. Persistent connections are not closed at the end of a request, but are cached and re-used. This is experimental Upon its value changing, this field issues an automatic update of this page. *Use SSL* Whether to encrypt the connection or to authenticate using certificates 

### Command Transport

 Please define below how you want to send commands to your monitoring instance. *Transport Name \* icinga2* The name of this command transport that is used to differentiate it from others Upon its value changing, this field issues an automatic update of this page. *Transport Type \**

- *Local Command File*
- *Remote Command File*
- *Icinga 2 API*
 
 *Command File \* /var/run/icinga2/cmd/icinga2.cmd* 

### Monitoring Security

 To protect your monitoring environment against prying eyes please fill out the settings below. *Protected Custom Variables \*pw\*,\*pass\*,community*  Comma separated case insensitive list of protected custom variables. Use \* as a placeholder for zero or more wildcard characters. Existance of those custom variables will be shown, but their values will be masked. 

### Congratulations! Icinga Web 2 has been successfully set up.

 Creating new database "icinga\_res"... Creating database schema... Creating login "icingaweb2"... Granting required privileges to login "icingaweb2"... The database has been fully set up! General configuration has been successfully written to: /usw/icingaweb2/config.ini Authentication configuration has been successfully written to: /usw/icingaweb2/authentication.ini Account "admin" has been successfully created. Account "admin" has been successfully defined as initial administrator. User Group Backend configuration has been successfully written to: /usw/icingaweb2/groups.ini User Group "Administrators" has been successfully created. Account "admin" has been successfully added as member to user group "Administrators". Resource configuration has been successfully written to: /usw/icingaweb2/resources.ini Monitoring backend configuration has been successfully written to: /usw/icingaweb2/modules/monitoring/backends.ini Resource configuration has been successfully updated: /usw/icingaweb2/resources.ini Command transport configuration has been successfully created: /usw/icingaweb2/modules/monitoring/commandtransports.ini Monitoring security configuration has been successfully created: /usw/icingaweb2/modules/monitoring/config.ini Module "doc" has been successfully enabled. Module "monitoring" has been successfully enabled. 

## Icinga 2 konfigurieren

ls /usw/icinga2/conf.d

### Hosts

 Linux Hosts: 

```
# mkdir /usw/icinga2/conf.d/hosts/tux
# vim /usw/icinga2/conf.d/hosts/tux/linux.conf
object Host "<hostname>" {

 import "generic-host"
 check_command = "hostalive"

 address = "<w.x.y.z>"
 vars.Owner = "owner@company.com"
 vars.os = "Linux"
 vars.Servie_Level = "24x7"

 vars.notification["mail"] = {
 groups = [ "icingaadmins" ]
 }
}
```

 Windows Hosts: 

```
# mkdir /usw/icinga2/conf.d/hosts/win
# vim /usw/icinga2/conf.d/hosts/tux/windows.conf
object Host "<hostname>" {

 import "generic-host"
 check_command = "hostalive"

 address = "<w.x.y.z>"
 vars.Owner = "owner@company.com"
 vars.os = "Windows"
 vars.Servie_Level = "24x7"

 vars.notification["mail"] = {
 groups = [ "icingaadmins" ]
 }
}
```

 Restart Icinga2 Service 

```
# service icinga2 reload
# systemctl reload icinga2.service
```

## Weitere Dokumentation

 [icinga.com](https://docs.icinga.com/icinga2/latest/doc/module/icinga2/toc)

### Video von A George S Pulinattu

 [Installationsanleitung](https://admin-docs.com/monitoring/icinga/install-icinga2/) https://www.youtube.com/watch?v=Nz0OxWzJWiY