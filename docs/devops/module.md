# Module

A file with psm1-Extension.

## Functions

````powershell
function Import-LocalStorage {...}

function Export-LocalStorage {...}

function Get-LocalStoragePath {...}
````

## Export-Members

The Members should be exported within a Module manifest (New-ModuleManifest).

````powershell
# Functions to export from this module, for best performance, do not use wildcards and do not delete the entry, use an empty array if there are no functions to export.
Export-ModuleMember -Function Import-LocalStorage, Export-LocalStorage, Get-LocalStoragePath
````