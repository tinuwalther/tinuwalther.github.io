# Function

A function which returns an object, either if an error occure or not.

````powershell
<#
.SYNOPSIS
Short description

.DESCRIPTION
Long description

.EXAMPLE
An example

.NOTES
General notes
#>
function Get-Something{
    [CmdletBinding()]
    param(
        [ValidateSet("Medium","Hot","Extra Hot")]
        [Parameter(Mandatory=$true)]
        [String] $Spice,

        [Parameter(Mandatory=$true)]
        [Int] $Timeout,

        [Parameter(Mandatory=$true)]
        [Switch] $Fire
    )
    $function = $($MyInvocation.MyCommand.Name)
    Write-Verbose "Running $function"

    $ret = @()
    try{
        $obj = [PSCustomObject]@{
            Spice   = $Spice
            Timeout = $Timeout
            Fire    = $Fire
        }
        $ret += $obj
    }
    catch [Exception]{
        Write-Verbose "-> Catch block reached"
        $obj = [PSCustomObject]@{
            Function  = $function
            Exception = $($_.Exception.GetType().FullName)
            Message   = $($_.Exception.Message)
        }
        $ret += $obj
        $error.clear()
    }
    finally{
        Write-Verbose "-> Finally block reached"
    }
    return $ret
}
````