---
title: HyperV Basisimage
date: '2014-11-27T09:18:46+01:00'
author: Tinu
excerpt: Basisimage auf Hyper-V einrichten.
categories:
- Virtualisierung
- Windows Server
tags:
- Hyper-V
- Staging
image: /assets/wiki/hyperv-icon.png
wordpress_id: 189
layout: post
permalink: /wiki/basisimage/
render_with_liquid: false
---

Das Basisimage wird folgenderweise eingerichtet:

# 1. Einrichten einer neuen VM unter Hyper-V

 Installation von Windows Server 2012 R2 und aller Windows Updates sowie Tools (Sysinternals) oder hinzufügen von Dateien welche Sie auf jedem Image benötigen. 

# 2. Windows generalisieren

 Damit wird sichergestellt, dass jedes System eine neue SID erhält und es im weiteren Betrieb zu keinen Problemen kommt. Starten Sie unter %windir%\\system32\\sysprep\\sysprep.exe und wählen Sie die Option *Generalize* und als Option für das Herunterfahren *Shutdown* oder führen Sie folgenden PowerShell-Command aus: 

```csharp
$($env:windir)\system32\sysprep\sysprep.exe /generalize /oobe /shutdown
```

### 3. VHD-Datei schützen

 Nachdem die virtuelle Maschine heruntergefahren wurde, starten Sie den Assistenten Datenträger bearbeiten aus der Hyper-V-Managementkonsole und komprimieren Sie den Datenträger. Nun wechseln Sie in den Windows Explorer und versehen die .vhd-Datei des Basisimages mit einem Schreibschutz. Diese .vhd-Datei darf nicht verändert werden. Sollte dies dennoch geschehen, werden alle virtuellen Computer welche auf diesem Image basieren unbrauchbar. Daher versehen Sie das Basisimage unbedingt mit einem Schreibschutz, Sie dürfen diese .vhd-Datei nie mehr verändern. PowerShell-Command: 

```csharp
$file = Get-Item $FullFilepath
if ($file.Attributes -notmatch 'ReadOnly') {
    #wenn die Datei das ReadOnly-Flag nicht gesetzt hat wird es gesetzt
    $file.Attributes = $file.Attributes -bxor [System.IO.FileAttributes]::ReadOnly
}
```

 Nachdem das Basisimage angelegt ist, können neue [virtuelle Computer](/wiki/virtuelle-computer/ "Virtuelle Computer") auf dieser Basis erstellt werden.