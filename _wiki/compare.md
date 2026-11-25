---
title: Compare-Object
date: '2014-11-26T21:08:06+01:00'
author: Tinu
excerpt: ''
categories:
- PowerShell
tags:
- Compare
- PSObject
wordpress_id: 155
layout: post
permalink: /wiki/compare/
render_with_liquid: false
---

## Syntax

```csharp
Compare-Object [-ReferenceObject] <PSObject[]> [-DifferenceObject] <PSObject[]>
[-CaseSensitive []] [-Culture ] [-ExcludeDifferent []] [-IncludeEqual []]
[-PassThru ]] [-Property <Object[]>] [-SyncWindow ] []

```

## Output

 Compare mit -PassThru listet als Output das formatierte Object auf. 

```csharp
Compare-Object -ReferenceObject $sourcecol -DifferenceObject $targetcol -PassThru

Name          : ICT-System-Engineer-Senior 65-3.pdf
Fullname      : /Volumes/DATEN1/Test/Child1/ICT-System-Engineer-Senior 65-3.pdf
LastWriteTime : 24.10.13 20:21:20
Length        : 1739576
SideIndicator : <=

```

 Compare ohne -PassThru listet als Output das Object auf. 

```csharp
Compare-Object -ReferenceObject $sourcecol -DifferenceObject $targetcol

InputObject                                                                                                                                                                              SideIndicator
-----------                                                                                                                                                                              -------------
@{Name=ICT-System-Engineer-Senior 65-3.pdf; Fullname=/Volumes/DATEN1/Test/Child1/ICT-System-Engineer-Senior 65-3.pdf; LastWriteTime=24.10.13 20:21:20; Length=1739576; SideIndicator=<=} <=           

```

### SideIndicator

 SideIndicator : &lt;= bezieht sich auf das ReferenceObject (Source) SideIndicator : =&gt; bezieht sich auf das DifferenceObject (Target) 

## Zwei Array vergleichen

 Zwei Array können folgenderweise miteinander verglichen werden: 

```
$src = @('A','B','C')
$dst = @('B','D','E')

#Show only differents
Compare-Object $($src) $($dst) | % { $_.InputObject }

#Show only equals
Compare-Object $($src) $($dst) -IncludeEqual | % {
    if($($_.SideIndicator) -eq "=="){
        $true
    }
    else{
        $false
    }
}
```

## Folder oder Files vergleichen

 Die Unterschiede sind die Methoden für den Zugriff: 

- mit **gci** **(Get-ChildItem)** wird auf Folder zugegriffen
- mit **gc** (**Get-Content)** wird auf Fileinhalte zugegriffen
- das Argument **-recurse** wird bei Foldervergleichen mitgegeben
 

### Zwei Folder miteinander vergleichen

 Zwei Folder rekursive miteinander vergleichen und die unterschiedlichen auflisten 

```csharp
$src = "C:\temp\src"
$dst = "C:\temp\dst"
$compare = Compare-Object $(gci -recurse $src) $(gci -recurse $dst)
$compare | %{
    if($($_.SideIndicator) -eq "<="){
        "Newer <= $($src):`t$($_.InputObject)"
    }
    elseif($($_.SideIndicator) -eq "=>"){
        "Newer => $($dst):`t$($_.InputObject)"
    }
}

```

 Zwei Folder miteinander vergleichen und die identischen auflisten 

```csharp
$src = "C:\temp\src"
$dst = "C:\temp\dst"
$compare = Compare-Object $(gci $src) $(gci $dst) -includeequal
$compare | %{
    if($($_.SideIndicator) -eq "=="){
        "== $($src):`t$($_.InputObject)"
    }
}

```

 Eine andere Variante ist mit Robocopy zwei Folder zu vergleichen: 

```csharp
$src = "C:\temp\src"
$dst = "C:\temp\dst"
robocopy "$($src)" "$($dst)" /E /R:0 /W:0 /NJH /L
```

 Output: 

```csharp
	                   2	C:\temp\079\
	  *EXTRA File 		      60	file1
	  *EXTRA File 		      37	file2
	    Older     		    5575	localconf - Copy.php

------------------------------------------------------------------------------

               Total    Copied   Skipped  Mismatch    FAILED    Extras
    Dirs :         1         0         1         0         0         0
   Files :         2         1         1         0         0         2
   Bytes :    10.8 k     5.4 k     5.4 k         0         0        97
   Times :   0:00:00   0:00:00                       0:00:00   0:00:00

   Ended : Wed Oct 15 11:33:43 2014

```

### Inhalt von zwei Files miteinander vergleichen

```csharp
$src = "C:\temp\file1"
$dst = "C:\temp\file2"
$compare = Compare-Object $(gc $src) $(gc $dst)
$compare | %{
    if($($_.SideIndicator) -eq "<="){
        "<= $($src):`t$($_.InputObject)"
    }
     elseif($($_.SideIndicator) -eq "=>"){
        "=> $($dst):`t$($_.InputObject)"
    }
}

```

## Zwei Objekte vergleichen