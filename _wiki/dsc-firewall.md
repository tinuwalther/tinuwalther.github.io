---
title: DSC Firewall
date: '2016-08-15T13:30:06+02:00'
author: Tinu
excerpt: Die Windows Firewall mit DSC konfigurieren.
categories:
- Desired State
tags:
- Desired State
- PowerShell
image: /assets/wiki/DSC_Logo_300p.png
wordpress_id: 1530
layout: post
permalink: /wiki/dsc-firewall/
render_with_liquid: false
---

## Firewall Konfiguration mit DSC

Windows Firewall mit DSC konfigurieren.

```
<#
 Get-DscResource -Name Service -Syntax 
#>
configuration AdvancedFirewallSettings
{
    Node 'localhost'
    {
        Service EnableService
        {
            Name        = 'MpsSvc'
            StartupType = 'Automatic'
            State       = 'Running'
        }

        Script EnableProfiles           
        {            
            # Must return a hashtable with at least one key            
            # named 'Result' of type String            
            GetScript = {     
                $ret = $null       
                Get-NetFirewallProfile | select Name,Enabled | %{
                    $ret = "$($_.Name)=$($_.Enabled) $ret"
                }   
                Return @{            
                    Result = $ret
                }            
            } 
            # Must return a boolean: $true or $false            
            TestScript = {   
                if((Get-NetFirewallProfile).Enabled -like 'false')
                {
                    Write-Verbose "One or more firewall profiles are off"            
                    Return $false            
                } 
                else
                {
                    Write-Verbose "All firewall profiles are on"            
                    Return $true            
                }
            } 
            # Returns nothing            
            SetScript = {            
                Write-Verbose "Setting all firewall profiles to on"            
                Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True          
            }
            DependsOn = "[Service]EnableService"            
        }            
    }
}

$workingdir = 'C:\DSC\MOF'
# Create MOF
AdvancedFirewallSettings -OutputPath $workingdir

# Apply Configuration
Start-DscConfiguration -ComputerName 'localhost' -wait -force -verbose -path $workingdir

```

## DSC Konfiguration testen

```
Test-DscConfiguration -Verbose

VERBOSE: Perform operation 'Invoke CimMethod' with following parameters, ''methodName' = TestConfiguration,'className' = MSFT_DSCLocal
ConfigurationManager,'namespaceName' = root/Microsoft/Windows/DesiredStateConfiguration'.
VERBOSE: An LCM method call arrived from computer W2K12R2-SRV1 with user sid.
VERBOSE: [W2K12R2-SRV1]: LCM:  [ Start  Test     ]
VERBOSE: [W2K12R2-SRV1]: LCM:  [ Start  Resource ]  [[Service]EnableService]
VERBOSE: [W2K12R2-SRV1]: LCM:  [ Start  Test     ]  [[Service]EnableService]
VERBOSE: [W2K12R2-SRV1]:                            [[Service]EnableService] Perform operation 'Query CimInstances' with following par
ameters, ''queryExpression' = SELECT * FROM Win32_Service WHERE Name='MpsSvc','queryDialect' = WQL,'namespaceName' = root\cimv2'.
VERBOSE: [W2K12R2-SRV1]:                            [[Service]EnableService] Operation 'Query CimInstances' complete.
VERBOSE: [W2K12R2-SRV1]: LCM:  [ End    Test     ]  [[Service]EnableService] True in 0.2970 seconds.
VERBOSE: [W2K12R2-SRV1]: LCM:  [ End    Resource ]  [[Service]EnableService]
VERBOSE: [W2K12R2-SRV1]: LCM:  [ Start  Resource ]  [[Script]EnableProfiles]
VERBOSE: [W2K12R2-SRV1]: LCM:  [ Start  Test     ]  [[Script]EnableProfiles]
VERBOSE: [W2K12R2-SRV1]:                            [[Script]EnableProfiles] All firewall profiles are on
VERBOSE: [W2K12R2-SRV1]: LCM:  [ End    Test     ]  [[Script]EnableProfiles] True in 0.0470 seconds.
VERBOSE: [W2K12R2-SRV1]: LCM:  [ End    Resource ]  [[Script]EnableProfiles]
VERBOSE: [W2K12R2-SRV1]: LCM:  [ End    Test     ]     Completed processing test operation. The operation returned True.
VERBOSE: [W2K12R2-SRV1]: LCM:  [ End    Test     ]    in  0.5780 seconds.
VERBOSE: Operation 'Invoke CimMethod' complete.
True
VERBOSE: Time taken for configuration job to complete is 0.789 seconds
```