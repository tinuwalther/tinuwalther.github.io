---
title: Remote reboot
date: '2015-02-16T18:14:11+01:00'
author: Tinu
excerpt: ''
categories:
- Windows Server
tags:
- Reboot
wordpress_id: 667
layout: post
permalink: /wiki/remote-reboot/
render_with_liquid: false
---

Restart mit PowerShell

```csharp
Restart-Computer 'Server' -credentials 'Domain\administrator'
```

 Restart über GUI Start, Run, **shutdown /i** gewünschten Computer eingeben... Restart über die Befehlszeile 

```
shutdown /r /m \\Server /c "Kommentar" /d [u|p] <xx>:<yy> /t 5 /force
```

 xx = 0 bis 255 (Hauptgrundnummer) yy = 0 bis 65'535 (Nebengrundnummer)