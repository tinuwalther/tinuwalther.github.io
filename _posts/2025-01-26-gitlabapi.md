---
layout: post
title:  "API GitLab"
author: Tinu
categories: "GitLab"
tags:   PowerShell News
permalink: /posts/:title:output_ext
---

## Table of Contents

- [Using GitLab with API](#using-gitlab-with-api)
  - [Generate a Personal Access Token](#generate-a-personal-access-token)
  - [Make API Requests](#make-api-requests)
  - [Common API Endpoints](#common-api-endpoints)
  - [Handling Responses](#handling-responses)
  - [Error Handling](#error-handling)
  - [Example using PowerShell](#example-using-powershell)
- [See also](#see-also)

## Using GitLab with API

To use GitLab with its API, follow these steps:

### Generate a Personal Access Token

First, you need to generate a personal access token (PAT) from your GitLab account or GitLab project:

1. Navigate to your GitLab profile or GitLab project settings.
2. Go to the "Access Tokens" section.
3. Create a new token with the required scopes (e.g., `api`).

### Make API Requests

You can make API requests by writing scripts in PowerShell.

### Common API Endpoints

- **List Projects**: `/projects`
- **Get a Single Project**: `/projects/:id`
- **Create a New Project**: `/projects`
- **List Issues**: `/projects/:id/issues`
- **Create an Issue**: `/projects/:id/issues`

[ [Top](#table-of-contents) ]

### Handling Responses

The API responses are typically in JSON format. Ensure you handle the responses appropriately in your application or script.

### Error Handling

Check for common HTTP status codes like `200 OK`, `201 Created`, `400 Bad Request`, `401 Unauthorized`, etc., to handle errors effectively.

[ [Top](#table-of-contents) ]

### Example using PowerShell

Download a file from your GitLab project:

```powershell
function Invoke-DownloadFileFromGitLab {
    [CmdletBinding()]
    param (
        # The Url and Port of the proxy server
        [ValidateNotNullOrEmpty()]
        [Parameter(Mandatory=$true)][string]$Proxy,

        # The Gitlab token to use for authentication
        [ValidateNotNullOrEmpty()]
        [Parameter(Mandatory=$true)][string]$GitLabToken,

        # The base url of the GitLab server, for example https://gitlab.com
        [ValidateNotNullOrEmpty()]
        [Parameter(Mandatory=$true)][string]$GitLabBaseUrl,

        # The name of the GitLab project, for example myproject
        [ValidateNotNullOrEmpty()]
        [Parameter(Mandatory=$true)][string]$GitLabProject,

        # The name of the GitLab branch, for example master
        [ValidateNotNullOrEmpty()]
        [Parameter(Mandatory=$true)][string]$GitLabBranch,

        # The path to the file in the GitLab repository, for example myfolder/myfile.md
        [ValidateNotNullOrEmpty()]
        [Parameter(Mandatory=$true)][string]$GitLabFilePath,

        # The local path to save the file to, for example C:\temp\myfile.md
        [ValidateNotNullOrEmpty()]
        [Parameter(Mandatory=$true)][string]$LocalFilePath
    )
    
    process{
        $EncodedBranch   = [uri]::EscapeDataString($GitLabBranch)
        $EncodedProject  = [uri]::EscapeDataString($GitLabProject)
        $EncodedFilePath = [uri]::EscapeDataString($GitLabFilePath)
        $ProjectUrl      = "$($GitLabBaseUrl)/api/v4/projects/$EncodedProject"

        $Headers = @{
            "PRIVATE-TOKEN" = $GitLabToken
        }

        #region Get GitLabProjectID
        try {
            $Response = Invoke-RestMethod -Uri $ProjectUrl -Headers $Headers -Proxy $Proxy -ProxyUseDefaultCredentials
            $GitLabProjectID = $($Response.id)
            Write-Verbose "$($ProjectUrl), $($GitLabProjectID)"
        } catch {
            Write-Warning "ProjectID - Failure: $($_)"
            $Error.Clear()
        }
        #endregion

        #region Download file from gitlab
        $FileDownloadUrl = "$($GitLabBaseUrl)/api/v4/projects/$($GitLabProjectID)/repository/files/$($EncodedFilePath)/raw?ref=$($EncodedBranch)"
        try {
            $null = Invoke-RestMethod -Uri $FileDownloadUrl -Headers $Headers -OutFile $LocalFilePath -Proxy $Proxy -ProxyUseDefaultCredentials
            Write-Host " - File downloaded to $($LocalFilePath)" -ForegroundColor Green
            $true
        } catch {
            Write-Warning "Download - Failure: $($_)"
            $Error.Clear()
            $false
        }            
        #endregion
    }
}
```

[ [Top](#table-of-contents) ]

Upload a file to your GitLab project:

```powershell
function Invoke-UploadFileToGitLab {
    [CmdletBinding()]
    param (
        # The Url and Port of the proxy server
        [ValidateNotNullOrEmpty()]
        [Parameter(Mandatory=$true)][string]$Proxy,

        # The Gitlab token to use for authentication
        [ValidateNotNullOrEmpty()]
        [Parameter(Mandatory=$true)][string]$GitLabToken,

        # The base url of the GitLab server, for example https://gitlab.com
        [ValidateNotNullOrEmpty()]
        [Parameter(Mandatory=$true)][string]$GitLabBaseUrl,

        # The name of the GitLab project, for example myproject
        [ValidateNotNullOrEmpty()]
        [Parameter(Mandatory=$true)][string]$GitLabProject,

        # The name of the GitLab branch, for example master
        [ValidateNotNullOrEmpty()]
        [Parameter(Mandatory=$true)][string]$GitLabBranch,

        # The path to the file in the GitLab repository, for example myfolder/myfile.md
        [ValidateNotNullOrEmpty()]
        [Parameter(Mandatory=$true)][string]$GitLabFilePath,

        # The local path to save the file to, for example C:\temp\myfile.md
        [ValidateNotNullOrEmpty()]
        [Parameter(Mandatory=$true)][string]$LocalFilePath
    )

    process{
        $EncodedBranch   = [uri]::EscapeDataString($GitLabBranch)
        $EncodedProject  = [uri]::EscapeDataString($GitLabProject)
        $EncodedFilePath = [uri]::EscapeDataString($GitLabFilePath)
        $ProjectUrl      = "$($GitLabBaseUrl)/api/v4/projects/$EncodedProject"

        $Headers = @{
            "PRIVATE-TOKEN" = $GitLabToken
        }

        #region Get GitLabProjectID
        try {
            $Response = Invoke-RestMethod -Uri $ProjectUrl -Headers $Headers -Proxy $Proxy -ProxyUseDefaultCredentials
            $GitLabProjectID = $($Response.id)
            Write-Verbose "$($ProjectUrl), $($GitLabProjectID)"
        } catch {
            Write-Warning "ProjectID - Failure: $($_)"
            $Error.Clear()
        }
        #endregion

        #region Check if branch exists
        if($GitLabProjectID){
            $BranchUrl = "$($GitLabBaseUrl)/api/v4/projects/$GitLabProjectID/repository/branches/$EncodedBranch"
            try {
                $Response = Invoke-RestMethod -Uri $BranchUrl -Headers $Headers -Proxy $Proxy -ProxyUseDefaultCredentials
                $BranchExists = $true
                Write-Verbose "$($BranchUrl), $($Response.name)"
            } catch {
                Write-Warning "BranchExists - Failure: $($_)"
                $Error.Clear()
            }
        }
        #endregion

        #region Check if file exists on gitlab
        if($BranchExists){
            $FileCheckUrl = "$($GitLabBaseUrl)/api/v4/projects/$GitLabProjectID/repository/files/$($EncodedFilePath)?ref=$($EncodedBranch)"
            try {
                $Response = Invoke-RestMethod -Uri $FileCheckUrl -Headers $Headers -Proxy $Proxy -ProxyUseDefaultCredentials
                $FileExists = $true
                Write-Verbose "$($FileCheckUrl), $($Response.name)"
            } catch {
                $Error.Clear()
                $FileExists = $false
            }
        }
        #endregion

        #region Read file content from local file
        try {
            $FileContent = [System.IO.File]::ReadAllText($LocalFilePath, [System.Text.Encoding]::UTF8)
            Write-Verbose "$($LocalFilePath), $($FileContent.length)"
        } catch {
            Write-Warning "ReadFileContent - Failure: $($_)"
            return $false
        }
        #endregion

        #region API-Body
        $Body = @{
            branch         = $GitLabBranch
            content        = $FileContent
            commit_message = "Automatic Update on $($GitLabFilePath) at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
        } | ConvertTo-Json -Depth 10
        Write-Verbose "Body: $($Body.length)"
        #endregion

        #region Upload or vreate the file on gitlab
        $ApiUrl = "$($GitLabBaseUrl)/api/v4/projects/$GitLabProjectID/repository/files/$EncodedFilePath"

        try {
            if($FileExists){
                $null = Invoke-RestMethod -Uri $ApiUrl -Method Put -Headers $Headers -Body $Body -ContentType "application/json" -Proxy $Proxy -ProxyUseDefaultCredentials
                Write-Host " - File $($GitLabBranch)/$($GitLabFilePath) updated!" -ForegroundColor Green
            }else{
                $null = Invoke-RestMethod -Uri $ApiUrl -Method Post -Headers $Headers -Body $Body -ContentType "application/json" -Proxy $Proxy -ProxyUseDefaultCredentials
                Write-Host " - File $($GitLabBranch)/$($GitLabFilePath) created!" -ForegroundColor Green
            }
        } catch {
            Write-Warning "Upload - Failure: $($_)"
        }
        #endregion
    }
}
```

The functions above are written for Windows PowerShell with a Proxy with a little help from GitHub Copilot.

[ [Top](#table-of-contents) ]

## See also

[GitLab API Documentation](https://docs.gitlab.com/ee/api/)
