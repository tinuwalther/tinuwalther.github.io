---
title: MariaDB
date: '2016-12-21T20:07:31+01:00'
author: Tinu
excerpt: MariaDB auf Linux installieren.
categories:
- Datenbank
tags:
- Open Source
wordpress_id: 1875
layout: post
permalink: /wiki/mariadb/
render_with_liquid: false
---

## Installation phpMyAdmin

### Install from EPEL

```
# yum --enablerepo=epel -y install phpMyAdmin php-mysql php-mcrypt
```

### Configure Access

```
# vim /usw/httpd/conf.d/phpMyAdmin.conf
# line 15: IP address you permit to access
Require ip 127.0.0.1 10.0.0.0/24
# line 32: IP address you permit to access
Require ip 127.0.0.1 10.0.0.0/24
```

### Restart Apache

```
# systemctl restart httpd
```

## Login

 http://localhost/phpmyadmin as root