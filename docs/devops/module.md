# Module

A file with psm1-Extension.

## Functions

````powershell
function PsNetDig {...}

function PsNetTping {...}

function PsNetUping {...}

function PsNetWping {...}
````

## Export-Members

The Members should be exported within a Module manifest, see here [FunctionsToExport](./manifest.md#additional-settings)

````powershell
# Functions to export from this module, for best performance, do not use wildcards and do not delete the entry, use an empty array if there are no functions to export.
Export-ModuleMember -Function PsNetDig, PsNetTping, PsNetUping, PsNetWping
````