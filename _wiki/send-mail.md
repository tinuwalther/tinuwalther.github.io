---
title: E-Mail versenden
date: '2015-10-05T19:07:45+02:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Email
wordpress_id: 1389
layout: post
permalink: /wiki/send-mail/
render_with_liquid: false
---

## E-Mail per PowerShell versenden

```
#region SendMail
$MailServer = "mailrelay.company.ch"
$MailFrom = "postmaster@company.ch"
$MailTo = "support@company.ch"

$Subject = "Testmessage"

$Body = "Hello Support`n`n"
$Body += "This is a test message for you.`n`n"
$Body += "Kind regards`n`n"
$Body += "Postmaster"

$FullFileName = "C:\Company\Output\Report.htm"

Send-MailMessage -From $MailFrom -To $MailTo -Subject $Subject `
-Body $Body -SmtpServer $MailServer -Attachments $FullFileName
#endregion
```