---
title: JSON mit JavaScript
date: '2023-08-01T17:22:54+02:00'
author: Tinu
excerpt: ''
categories:
- JavaScript
tags:
- JavaScript
- JSON
image: /assets/wiki/app-json-icon.png
wordpress_id: 3795
layout: post
permalink: /wiki/json-mit-javascript/
render_with_liquid: false
---

Ein Postman Request gibt normalerweise einen JSON-String zurück. Ein JSON-String besteht aus einem oder mehreren Objekten und Arrays. Die geschweiften Klammern "{}" enthalten ein Objekt, während die eckigen Klammern "\[\]" ein Array enthalten.



```javascript
// JSON string from REST => Object
var jsonContent = {
    "result": [
        {
            "os"          : "almalinux",
            "version"     : "9",
            "ram"         : "4",
            "cpu"         : "2",
            "disks" : [
                { 
                    "scsi" : "0:0",
                    "size" : 60, 
                },
                { 
                    "scsi" : "0:1",
                    "size" : 40, 
                },
            ],
            "hostname"    : "asterix",
            "customer"    : "Gallier",
            "sla"         : "5x8",
            "owner"       : "tinu",
            "action"      : "newVm"
        }
    ]
}
console.log(jsonContent)

```

## JSON Object

Mit `console.log(jsonContent)` wird ein JSON Object in die Konsole ausgegeben:

```
{"result":[{"os":"almalinux","version":"9","ram":"4","cpu":"2","disks":[{"scsi":"0:0","size":60},
{"scsi":"0:1","size":40}],"hostname":"asterix","customer":"Gallier","sla":"5x8","owner":"tinu",
"action":"newVm"}]}

```

Aus diesem Object können die einzelnen Properties mittels Schleifen abgefragt werden.

## For-Schleife

Mit einer Zählerschliefe ein Array durchgehen:



```javascript
// Get a property of each object
var vm = jsonContent.result
for (var i = 0; i < vm.length; i++) {
    console.log("Property of object from Element " + [i] + ": Name: " + vm[i].hostname)
}

```

Mit der oben aufgeführten Schleife wird durch das Array iteriert und das Property **hostname** in die Konsole ausgegeben.

```text
Property of object from Element 0: Name: asterix

```

## ForEach-Schleife

Mit einer ForEach-Schleife (Schleife ohne Zähler) ein Array durchgehen:



```javascript
// Get properties of each object
jsonContent.result.forEach(vm => {
    console.log("Name: " + vm.hostname)
})

```

Mit der oben aufgeführten Schleife wird durch das Array iteriert und das Property **hostname** in die Konsole ausgegeben.

```text
Name: asterix

```

## Kombinierte ForEach- und For-Schleife

Und nun kombiniere ich die ForEach- mit einer For-Schleife:



```javascript
// Combination of forEach- and for-Loop
jsonContent.result.forEach(vm => {
    console.log("VMName: " + vm.hostname)
    // vm.disks is an array of objects
    for (var i = 0; i < vm.disks.length; i++) {
        console.log("Disk: " + [i] + ", SCIS: " + vm.disks[i].scsi + ", SizeGB: " + vm.disks[i].size)
    }
})

```

Mit der oben aufgeführten Kombination wird durch das Array iteriert und das Property **hostname** in die Konsole ausgegeben. Danach wird mit einer Zählerschleife durch das Disk-Array iteriert und die Werte zu den Properties **SCSI** und **Size** in die Konsole ausgegeben. Hier muss explizit der Name des Property angegeben werden, damit der Wert dazu ausgelesen werden kann.

```text
VMName: asterix
Disk: 0, SCIS: 0:0, SizeGB: 60
Disk: 1, SCIS: 0:1, SizeGB: 40

```

### Noch eine andere Schleifen-Kombination

```javascript
jsonContent.result.forEach(vm => {
    // get explicit one property
    console.log("VMName: " + vm.hostname)
    // Loop through the vm.disks-array
    vm.disks.forEach(disk=> {
        // get the key and value of each object
        for (const [key, val] of Object.entries(disk)) {
            console.log("Key: '" + key + "', Value: '" + val + "'");
        }
    })
})

```

Mit der oben aufgeführten Kombination wird durch das Array iteriert und das Property **hostname** in die Konsole ausgegeben. Danach wird mit einer Zählerschleife durch das Disk-Array iteriert und die Werte zu den Properties **SCSI** und **Size** in die Konsole ausgegeben. Hier muss der Name des Property **nicht** angegeben werden, damit der Wert dazu ausgelesen werden kann.

```text
VMName: asterix
Key: 'scsi', Value: '0:0'
Key: 'size', Value: '60'
Key: 'scsi', Value: '0:1'
Key: 'size', Value: '40'

```

### Switch

```javascript
jsonContent.result.forEach(vm => {
    // get explicit one property
    console.log("VMName: " + vm.hostname)
    // Loop through the vm.disks-array
    vm.disks.forEach(disk => {
        // get the key and value of each object
        for (const [key, val] of Object.entries(disk)) {
            // console.log("Key: '" + key + "', Value: '" + val + "'");
            switch(key){
                case "scsi":
                    if(val == "0:0"){
                        console.log("System disk: '" + key + "':'" + val + "'");
                    }else{
                        console.log("Additional disk: '" + key + "':'" + val + "'");
                    }
                    break
                default:
                    console.log("-> Key: '" + key + "', Value: '" + val + "'");
                    break
            }
        }
    })
})

```

Output

```text
VMName: asterix
System disk: 'scsi':'0:0'
-> Key: 'size', Value: '60'
Additional disk: 'scsi':'0:1'
-> Key: 'size', Value: '40'

```

