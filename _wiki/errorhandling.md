---
title: Errorhandling
date: '2018-03-01T23:47:49+01:00'
author: Tinu
excerpt: Es gibt zwei Arten von Errors, Terminating Errors und Non-Terminating Errors.
categories:
- PowerShell
tags:
- Error
image: /assets/wiki/powershell-1.png
wordpress_id: 2461
layout: post
permalink: /wiki/errorhandling/
render_with_liquid: false
---

Es gibt zwei Arten von Errors, Terminating Errors und Non-Terminating Errors.

## Terminating Error

- Command-/Script wird abgebrochen - try{}catch{}finaly{}-Statement einsetzbar - ErroAction und ErrorActionPreference nicht einsetzbar 

```
try{ 
    throw 'There is something wrong in paradiese!' 
} 
catch{ 
    $_ | gm 
    "CategoryInfo: $($_.CategoryInfo.GetMessage())" 
    "Exception : $($_.Exception)" 
    $error.Clear() 
}
finally{
    Write-Host 'Terminating Error' -ForegroundColor Yellow
}
```

## Non-Terminating Error

- Command-/Script fortsetzen - ErrorAction und ErrorActionPreference einsetzbar - SilentlyContinue -&gt; zeigt den Fehler nicht an und setzt Command-/Script fort - Ignore -&gt; Error wird nicht in Error-Array aufgenommen - Continue -&gt; Standardverhalten, wenn nichts definiert wird - Stop -&gt; Verhalten eines Terminating Errors setzen - Inquire -&gt; Benutzer fragen wie weiter 

```
Set-DnsClientServerAddress 'Ein Test' -ErrorAction SilentlyContinue
Write-host 'Non-Terminating Error' -ForegroundColor Yellow
$Error | % { $_ | Select CategoryInfo, Exception | fl }
$Error.Clear()
```

### Non-Terminating Error zu Terminating Error machen

Mit diesem Vorgehen kann das try-catch-Statement eingesetzt und auf die Error-Properties **CategoryInfo** und **Exception** zugegriffen werden. 

```
try{   
    Set-DnsClientServerAddress 'Ein Test' -ErrorAction <strong>Stop  </strong> 
}   
catch{   
    $_ | gm   
    $error.Clear()   
}   
```

**Output**

```
TypeName: System.Management.Automation.<strong>ErrorRecord  </strong> 

Name                  MemberType     Definition                                                                                                                                      
----                  ----------     ----------                                                                                                                                      
Equals                Method         bool Equals(System.Object obj)                                                                                                                  
GetHashCode           Method         int GetHashCode()                                                                                                                               
GetObjectData         Method         void GetObjectData(System.Runtime.Serialization.SerializationInfo info, System.Runtime.Serialization.StreamingContext context), void ISeriali...
GetType               Method         type GetType()                                                                                                                                  
ToString              Method         string ToString()                                                                                                                               
<strong>CategoryInfo</strong>          Property       System.Management.Automation.ErrorCategoryInfo CategoryInfo {get;}                                                                             
ErrorDetails          Property       System.Management.Automation.ErrorDetails ErrorDetails {get;set;}                                                                               
<strong>Exception</strong>             Property       System.Exception Exception {get;}                                                                                                              
FullyQualifiedErrorId Property       string FullyQualifiedErrorId {get;}                                                                                                             
InvocationInfo        Property       System.Management.Automation.InvocationInfo InvocationInfo {get;}                                                                               
PipelineIterationInfo Property       System.Collections.ObjectModel.ReadOnlyCollection[int] PipelineIterationInfo {get;}                                                             
ScriptStackTrace      Property       string ScriptStackTrace {get;}                                                                                                                  
TargetObject          Property       System.Object TargetObject {get;}                                                                                                               
PSMessageDetails      ScriptProperty System.Object PSMessageDetails {get=& { Set-StrictMode -Version 1; $this.Exception.InnerException.PSMessageDetails };}                          
```

Wird hingegen ein **Non-Terminating** Error mit dem vermeintlichen ErrorAction-Verhalten ohne try-catch-Statement ergänzt, endet dies in einem **zusätzlichen Terminating Error** und der Command bricht ab. So sind am Ende **zwei** statt nur **ein Error** im Error-Array. 

```
Set-DnsClientServerAddress 'Ein Test' -ErrorAction Stop   
  
$error.count()  

for ($i = 0; $i -lt $error.Count; $i++){   
    $error[$i] | gm   
}   
$error.clear()   
```

**Output**Im Error Type **ActionPreferenceStopException** kann nicht direkt auf die Error-Properties CategoryInfo und Exception zugegriffen werden, hier könnte der Umweg über das Property **ErrorRecord** gemacht werden. 

```
TypeName: System.Management.Automation.<strong>ActionPreferenceStopException</strong> 

Name                        MemberType Definition                                                                                                                                    
----                        ---------- ----------                                                                                                                                    
Equals                      Method     bool Equals(System.Object obj), bool _Exception.Equals(System.Object obj)                                                                     
GetBaseException            Method     System.Exception GetBaseException(), System.Exception _Exception.GetBaseException()                                                           
GetHashCode                 Method     int GetHashCode(), int _Exception.GetHashCode()                                                                                               
GetObjectData               Method     void GetObjectData(System.Runtime.Serialization.SerializationInfo info, System.Runtime.Serialization.StreamingContext context), void ISeria...
GetType                     Method     type GetType(), type _Exception.GetType()                                                                                                     
ToString                    Method     string ToString(), string _Exception.ToString()                                                                                               
Data                        Property   System.Collections.IDictionary Data {get;}                                                                                                    
ErrorRecord                 Property   System.Management.Automation.ErrorRecord ErrorRecord {get;}                                                                                   
HelpLink                    Property   string HelpLink {get;set;}                                                                                                                    
HResult                     Property   int HResult {get;set;}                                                                                                                        
InnerException              Property   System.Exception InnerException {get;}                                                                                                        
Message                     Property   string Message {get;}                                                                                                                         
Source                      Property   string Source {get;set;}                                                                                                                      
StackTrace                  Property   string StackTrace {get;}                                                                                                                      
TargetSite                  Property   System.Reflection.MethodBase TargetSite {get;}                                                                                                
WasThrownFromThrowStatement Property   bool WasThrownFromThrowStatement {get;set;}                                                                                                   

```

Beim Error Type **RemotingErrorRecord** wiederum kann direkt auf die Propetries **CategoryInfo** und **Exception** zugegriffen werden. 

```
TypeName: System.Management.Automation.Runspaces.<strong>RemotingErrorRecord</strong> 

Name                  MemberType     Definition                                                                                                                                      
----                  ----------     ----------                                                                                                                                      
Equals                Method         bool Equals(System.Object obj)                                                                                                                  
GetHashCode           Method         int GetHashCode()                                                                                                                               
GetObjectData         Method         void GetObjectData(System.Runtime.Serialization.SerializationInfo info, System.Runtime.Serialization.StreamingContext context), void ISeriali...
GetType               Method         type GetType()                                                                                                                                  
ToString              Method         string ToString()                                                                                                                               
<strong>CategoryInfo         </strong> Property       System.Management.Automation.ErrorCategoryInfo CategoryInfo {get;}                                                                            
ErrorDetails          Property       System.Management.Automation.ErrorDetails ErrorDetails {get;set;}                                                                               
<strong>Exception            </strong> Property       System.Exception Exception {get;}                                                                                                            
FullyQualifiedErrorId Property       string FullyQualifiedErrorId {get;}                                                                                                             
InvocationInfo        Property       System.Management.Automation.InvocationInfo InvocationInfo {get;}                                                                               
OriginInfo            Property       System.Management.Automation.Remoting.OriginInfo OriginInfo {get;}                                                                              
PipelineIterationInfo Property       System.Collections.ObjectModel.ReadOnlyCollection[int] PipelineIterationInfo {get;}                                                             
ScriptStackTrace      Property       string ScriptStackTrace {get;}                                                                                                                  
TargetObject          Property       System.Object TargetObject {get;}                                                                                                               
PSMessageDetails      ScriptProperty System.Object PSMessageDetails {get=& { Set-StrictMode -Version 1; $this.Exception.InnerException.PSMessageDetails };}                          
```

## Fazit

Dein Script/Function sollte keinen Fehler auslösen, wenn doch dan setze wenn immer möglich auf Terminating Error und try-catch-Statement. 

## References

[4sysops](https://4sysops.com/archives/trycatchfinally-blocks-in-powershell-for-better-error-handling/), [docs.microsoft.com](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally?view=powershell-6), [PlayWithErrors.ps1](https://github.com/tinuwalther/Errorhandling/blob/master/PlayWithErrors.ps1)