---
title: Home
date: '2014-11-21T19:24:52+01:00'
author: Tinu
excerpt: ''
wordpress_id: 9
layout: post
permalink: /wiki/about/
render_with_liquid: false
---

Informatik dient in erster Linie dazu den Nutzer in seiner täglichen Arbeit zu unterstützen. Es gilt aber auch die IT-Mitarbeitende vor Einsätzen zu Unzeiten im Büro zu bewahren. In der heutigen Zeit ist es mit der aktuellen Technologie möglich von zu Hause aus dem «Home Office» zu arbeiten. Die Infrastruktur dazu ist bei den meisten Firmen (Remote Access Services, Citrix XenApp, ...) und bei allen Informatikern vorhanden (Internetzugang zu Hause, VPN, …). Vom Kader wird dazu nur ein bisschen Vertrauen in die Mitarbeitenden verlangt und die arbeiten in der Regel gerne. Die Mitarbeitenden bedanken sich für das entgegengebrachte Vertrauen in sie mit Selbstdisziplin und guter Arbeit aus dem «Home Office». So ergibt sich eine Win-Win-Situation für beide Parteien - was will man mehr?

## KISS-Strategie

 **K**eep **I**t **S**imple and **S**tupid, komplex und umständlich erhöht nur den Aufwand bei der Implementation und im Betrieb und schlussendlich die Kosten für den Kunden. Selbstherrliches «Gärtchendenken» ist in einer gut funktionierenden IT nicht gefragt. 

## Planung, Dokumentation und Automatisation

 Planung, Dokumentation und Automatisation sind wichtige Elemente in der Informatik und sollten weder vergessen noch verdrängt/verschoben werden. Später macht man es dann doch nicht mehr, sei es weil man gar nicht mehr weiss was man wie gemacht hat oder weil man sowieso keine Zeit dafür hat. Die Dokumentationen sollen nur so viel wie nötig enthalten und nicht künstlich aufgebläht werden. Ein Wiki ist immer gut, wenn man es auch aktuell hält. 

## Betrieb einer Plattform

 Ist eine Plattform einmal zu Ende entwickelt, wird diese dem Betrieb übergeben. Doch was muss so eine neue Plattform eigentlich erfüllen, um vom Betrieb übernommen zu werden? Das ist scheinbar eine Frage die sich niemand stellt - ist ja eh alles klar. 

### Monitoring/Alarming

 Ein einheitliches und zentrales Monitoring und Alarming für alle Plattformen ist ein absolutes MUSS-Kriterium für das Betreiben einer Plattform. Ohne Monitoring und Alarming kein Betrieb, sie fliegen ja auch kein Flugzeug ohne Instrumente im Cockpit. 

### Kurze einfache Zugriffe

 Muss der Betrieb eingreifen, so ist ein schneller, kurzer Zugriffsweg auf das betroffene System unabdingbar. Remote Desktop Session und PowerShell Remoting sind Standardtools, welche auf jedes System offen sein sollte. 

### Security Patching

 Ein automatisiertes zentrales Patching für die Plattform gehört aus Sicherheitsgründen ebenfalls zu einem funktionierenden Betrieb. 

### Backup/Restore

 Das ein funktionierendes Backup- und Restoreverfahren getestet und dokumentiert vorhanden ist, ist ja klar. 

### Capacity Management

 Wie ist geregelt, wie mit Kapazitäten umgegangen werden soll... 

### Lifecycle

 Eine Plattform ist nur so gut wie sie aktuell gehalten wird. Windows Server 2008 und älter gehört nun wirklich nicht mehr auf eine aktuelle Plattform und sollten schnellstmöglich aktualisiert werden. 

### Service Level Agreement

 Welche Systeme müssen innerhalb welcher Frist wieder hergestellt werden können... 

### Kontaktperson

 An wen kann sich der Betrieb wenden, wenn eine Disk vergrössert werden muss, eine Applikation nicht mehr reagiert, ein System ausserordentlich gebootet werden muss, usw. Sind all diese Punkte geklärt, steht dem ordentlichen Betrieb nichts mehr im Weg. 

---

 Ich hoffe mit meinen Beiträgen etwas zur KISS-Strategie beizutragen zu können und wünsche interessante Entdeckungen auf meinen Seiten.