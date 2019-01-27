# Class

A file, could have a psm1-Extension.

````powershell
Class PsNetTools {...}
````

## Properties

````powershell
[string]$message = $null
````

## Constructor

````powershell
PsNetTools(){
    $this.message = "Loading PsNetTools"
}
````

## Methods

````powershell
[object]static dig() {...}

[object]static tping() {...}

[object]static uping() {...}

[object]static wping() {...}
````

## Export-Members

The Function should be exported within a Module manifest, see here [Module](./module.md#export-members)