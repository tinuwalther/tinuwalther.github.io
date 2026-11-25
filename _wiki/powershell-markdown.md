---
title: PowerShell Markdown
date: '2026-01-07T11:20:25+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Markdown
- PSObject
image: /assets/wiki/cropped-favicon.png
wordpress_id: 4286
layout: post
permalink: /wiki/powershell-markdown/
render_with_liquid: false
---

Ich arbeite gerne mit Markdown Tabellen. Wenn ich eine grosse Markdown Tabelle habe und ich Massenmutationen vornehmen will, ist die beste Variante, die Markdown Tabelle in ein PSCustomObject zu konvertieren, die Mutationen vorzunehmen und das PSCustomObject zurück in eine Markdown Tabelle zu konvertieren.

### ConvertFrom-MarkdownTable

Eine Markdown Tabelle in ein PSCustomObject umwandel. 

```powershell
function ConvertFrom-MarkdownTable {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory, ValueFromPipeline)]
        [string[]]$Markdown
    )

    begin {
        # Initialize empty Array
        $lines = @()
    }

    process {
        # Add the Markdown to the Array
        $lines += $Markdown
    }

    end {
        # Remove empty lines
        $lines = $lines | Where-Object { $_.Trim() -ne '' }

        if ($lines.Count -lt 2) {
            throw "Invalid Markdown table"
        }

        # Extract header - trim each header
        $headers = ($lines[0].Trim('|') -split '\s*\|\s*') | ForEach-Object { $_.Trim() }

        # Data rows (skip header + separator)
        $dataLines = $lines | Select-Object -Skip 2

        foreach ($line in $dataLines) {
            # Trim each field
            $values = ($line.Trim('|') -split '\s*\|\s*') | ForEach-Object { $_.Trim() }

            if ($values.Count -ne $headers.Count) {
                throw "Number of columns does not match: $line"
            }

            $obj = [ordered]@{}
            for ($i = 0; $i -lt $headers.Count; $i++) {
                $obj[$headers[$i]] = $values[$i]
            }

            [PSCustomObject]$obj
        }
    }
}
```

### Add-ColumnToMarkdownTable

Eine neue Spalte mit leerem Wert in eine Markdown Tabelle hinzufügen. 

```powershell
function Add-ColumnToMarkdownTable {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory, ValueFromPipeline)]
        [string[]]$Markdown,

        [Parameter(Mandatory)]
        [string]$InsertAfterHeader,

        [Parameter(Mandatory)]
        [string]$NewColumnName
    )

    begin {
        # Initialize empty Array
        $lines = @()
    }

    process {
        # Add the Markdown to the Array
        $lines += $Markdown
    }

    end {
        $lines = $lines | Where-Object { $_.Trim() -ne '' }

        if ($lines.Count -lt 2) {
            throw "Ungültige Markdown-Tabelle"
        }

        # Extract header - trim each header
        $headers = ($lines[0].Trim('|') -split '\s*\|\s*') | ForEach-Object { $_.Trim() }

        # Insert new column after header
        $index = $headers.IndexOf($InsertAfterHeader)
        if ($index -lt 0) {
            throw "Header '$InsertAfterHeader' nicht gefunden"
        }

        # Expand header
        $headers = @(
            $headers[0..$index] +
            $NewColumnName +
            $headers[($index + 1)..($headers.Count - 1)]
        )

        # Data rows
        $dataLines = $lines | Select-Object -Skip 2

        foreach ($line in $dataLines) {

            # Trim values cleanly
            $values = ($line.Trim('|') -split '\s*\|\s*') | ForEach-Object { $_.Trim() }

            # Insert empty value for new column
            $values = @(
                $values[0..$index] +
                '' +
                $values[($index + 1)..($values.Count - 1)]
            )

            $obj = [ordered]@{}
            for ($i = 0; $i -lt $headers.Count; $i++) {
                $obj[$headers[$i]] = $values[$i]
            }

            [PSCustomObject]$obj
        }
    }
}
```

### ConvertTo-MarkdownTable

Eine Markdown Tabelle von einem PSCustomObject in eine Markdown Tabelle umwandel. 

```powershell
function ConvertTo-MarkdownTable {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory, ValueFromPipeline)]
        [PSCustomObject[]]$InputObject
    )

    begin {
        # Initialize empty Array
        $rows = @()
    }

    process {
        # Add the PSCustomObject to the Array
        $rows += $InputObject
    }

    end {
        if (-not $rows) {
            return ''
        }

        # Header (property order remains unchanged)
        $headers = $rows[0].PSObject.Properties |
                   Where-Object { $_.MemberType -eq 'NoteProperty' } |
                   Select-Object -ExpandProperty Name

        # Header line
        $headerLine = '| ' + ($headers -join ' | ') + ' |'

        # Markdown separator
        $separatorLine = '| ' + (($headers | ForEach-Object { '---' }) -join ' | ') + ' |'

        # Data rows
        $dataLines = foreach ($row in $rows) {
            $values = foreach ($header in $headers) {
                $value = $row.$header
                if ($null -eq $value) { '' }
                else { $value.ToString().Trim() }
            }
            '| ' + ($values -join ' | ') + ' |'
        }

        # A string (Markdown-compatible)
        @(
            $headerLine
            $separatorLine
            $dataLines
        ) -join "`n"
    }
}
```