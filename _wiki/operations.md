---
title: Windows Operating
date: '2016-06-02T08:45:46+02:00'
author: Tinu
excerpt: ''
categories:
- Betrieb
tags:
- Operating
wordpress_id: 1451
layout: post
permalink: /wiki/operations/
render_with_liquid: false
---

Was ist eigentlich für den Windows Betrieb notwendig?

# Betrieb einer Plattform

Ist eine Plattform einmal zu Ende entwickelt, wird diese dem Betrieb übergeben. Doch was muss so eine neue Plattform eigentlich erfüllen, um vom Betrieb übernommen zu werden? Das ist scheinbar eine Frage die sich niemand stellt - ist ja eh alles klar. 

## Planung, Dokumentation und Automatisation

Planung, Dokumentation und Automatisation sind wichtige Elemente in der Informatik und sollten weder vergessen noch verdrängt/verschoben werden. Später macht man es dann doch nicht mehr, sei es weil man gar nicht mehr weiss was man wie gemacht hat oder weil man sowieso keine Zeit dafür hat. 

### Wiki

Die Dokumentationen sollen nur so viel wie nötig enthalten und nicht künstlich aufgebläht werden. Ein Wiki ist immer gut, wenn man es auch aktuell hält. 

| Beschreibung | Bild |
|---|---|
|
| Eine zweispaltige Tabelle passt immer und hilft den Teamkollegen, wenn sie etwas zum ersten Mal oder nur sporadisch durchführen müssen. | [![](/assets/wiki/environmental-management-system.png)](/assets/wiki/environmental-management-system.png) |

## Kurze einfache Zugriffe

Muss der Betrieb eingreifen, so ist ein schneller, kurzer Zugriffsweg auf das betroffene System unabdingbar. Remote Desktop Session und PowerShell Remoting sind Standardtools, welche auf jedes System offen sein sollte. 

## Ein zentrales Management

Das allerwichtigste für einen funktionierenden Betrieb ist ein **zentrales Management** der Kundensysteme. **PowerShell Remoting** ist in der heutigen Zeit ein Muss und die WinRM-Ports gehören einfach in die Port-Matrix aufgenommen. Bei VMware muss **PowerCLI** auf alle seine Guests zugreifen können, darüber kann z.B. eine Diskvergrösserung auf allen Systemen vorgenommen werden ohne das man sich über RDP am Server anmelden muss. 

## Monitoring

Ein einheitliches und zentrales Monitoring und Alarming für alle Plattformen ist ein absolutes MUSS-Kriterium für das Betreiben einer Plattform. **Ohne Monitoring und Alarming kein Betrieb**, sie fliegen ja auch kein Flugzeug ohne Instrumente im Cockpit. Alle Server werden von einem Monitoring Tool überwacht und an eine **zentrale Konsole** weitergeleitet, damit der Betrieb auf einen Blick sehen kann wo Probleme entstehen. 

## Alarming

Tritt ein Fehler auf der Plattform auf, muss die richtige Stelle umgehend informiert werden. Dies geschieht über das Monitoring, welches den Fehler an das Alarming weiterleitet. 

## Capacity Management

Zu wenig Diskspace, zu wenig Memory und zu wenig CPU. Damit dies in Zukunft nicht mehr so oft vorkommen kann, muss der Betrieb über ein Tool verfügen mit dem auf diese Werte über einen grösseren Zeitraum (mind. 1 Jahr) zurück geblickt werden kann. Aus diesem Blick zurück kann der Betrieb dann eine Trend-Analyse für die Zukunft erstellen. 

## Windows Updates

Wenn der Kunde nicht selber für das Patching seiner Server verantwortlich ist, muss der Betrieb über ein **zentrales Tool** verfügen mit dem er das Patchen auf alle betroffenen Server automatisiert steuern kann. **WSUS** stellt die Updates nur zur Verfügung, für die Installation auf den Servern aber sorgt der WSUS nicht. Das wird oftmals verwechselt und sorgt für Missverständnisse. 

## Lifecycle

Eine Plattform ist nur so gut wie sie aktuell gehalten wird. Windows Server 2008 und älter gehört nun wirklich nicht mehr auf eine aktuelle Plattform und sollten schnellstmöglich aktualisiert werden. Genau gleich verhält es sich mit allen installierten Tools und Applikationen. Was passieren kann wenn der Lifecycle vernachlässigt wird, zeigt sich immer wieder mit erfolgreichen Attacken wie dem NotPetya- und Ransomeware Angriffen. 

## Backup/Restore

Das ein funktionierendes Backup- und Restoreverfahren getestet und dokumentiert vorhanden ist, ist ja klar. 

## Service Level Agreement

Welche Systeme müssen innerhalb welcher Frist wieder hergestellt werden können... 

## Kontaktperson

An wen kann sich der Betrieb wenden, wenn eine Disk vergrössert werden muss, eine Applikation nicht mehr reagiert, ein System ausserordentlich gebootet werden muss, usw. Sind all diese Punkte geklärt, steht dem ordentlichen Betrieb nichts mehr im Weg.