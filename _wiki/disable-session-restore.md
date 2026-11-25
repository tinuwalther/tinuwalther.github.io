---
title: Disable Session Restore
date: '2022-04-03T11:28:37+02:00'
author: Tinu
excerpt: 'Beim Starten von VS Code werden automatisch die Sessions von den letzten
  Benutzungen wiederhergestellt. In diesem Beitrag zeige ich, wie dieses Feature ausgeschaltet
  werden kann. '
categories:
- PowerShell
tags:
- VSCode
image: /assets/wiki/vscode.png
wordpress_id: 3617
layout: post
permalink: /wiki/disable-session-restore/
render_with_liquid: false
---

Beim Starten von VS Code werden automatisch jedesmal die Sessions von den letzten Benutzungen wiederhergestellt.

[![](/assets/wiki/SessionRestored-1024x221.png)](/assets/wiki/SessionRestored.png)## Disable Session Restore

Settings öffnen mit Ctrl + ,

Search String: terminal.integrated.persistentSessionReviveProcess eingeben und im Dropdown auf **never** einstellen.

[![](/assets/wiki/persistentSessionReviveProcess-1024x322.png)](/assets/wiki/persistentSessionReviveProcess.png)Search String: terminal.integrated.enablePersistentSessions eingeben und deaktivieren.

[![](/assets/wiki/enablePersistentSessions-1024x215.png)](/assets/wiki/enablePersistentSessions.png)VS Code neu starten - Fertig, die Sessions werden nicht mehr wiederhergestellt und VSCode startet schneller.

## References

[Visual Studio Code Wiki](https://github.com/microsoft/vscode/wiki/)

