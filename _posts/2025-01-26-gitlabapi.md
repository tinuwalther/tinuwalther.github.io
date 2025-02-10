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
- [PowerShell](#powershell)
- [GitLab CLI](#gitlab-cli)
- [See also](#see-also)

## Using GitLab with API

To use GitLab with its API, follow these steps:

## Generate a Personal Access Token

First, you need to generate a personal access token (PAT) from your GitLab account or GitLab project:

1. Navigate to your GitLab profile or GitLab project settings.
2. Go to the "Access Tokens" section.
3. Create a new token with the required scopes (e.g., `api`).

## Make API Requests

You can make API requests by writing scripts in PowerShell.

## Common API Endpoints

- **List Projects**: `/projects`
- **Get a Single Project**: `/projects/:id`
- **Create a New Project**: `/projects`
- **List Issues**: `/projects/:id/issues`
- **Create an Issue**: `/projects/:id/issues`

[ [Top](#table-of-contents) ]

## Handling Responses

PowerShell provides two cmdlets for making HTTP requests: `Invoke-WebRequest` and `Invoke-RestMethod`.
Both cmdlets can be used to interact with REST APIs, but they have some differences in their usage and output.

### Invoke-WebRequest

`Invoke-WebRequest` is a versatile cmdlet that can be used to make HTTP requests and retrieve web content.
It returns a detailed response object that includes the status code, headers, and the content of the response.

Use `Invoke-WebRequest` when you need detailed information about the HTTP response or when working with non-JSON content.

### Invoke-RestMethod

`Invoke-RestMethod` is specifically designed for interacting with REST APIs.
It automatically parses the JSON response and returns a PowerShell object, making it easier to work with the data.

Use `Invoke-RestMethod` when interacting with REST APIs that return JSON data.

[ [Top](#table-of-contents) ]

## Error Handling

`Invoke-WebRequest` and `Invoke-RestMethod` can return various HTTP status codes depending on the outcome of the request. Here are some common HTTP status codes you might encounter:

| Status Code | Status Message | Description                                                                 |
|---|---|---|
| **200** | OK | The request was successful, and the server returned the requested data.     |
| **201** | Created | The request was successful, and a new resource was created.             |
| **204** | No Conten | The request was successful, but there is no content to return.       |
| **400** | Bad Request | The server could not understand the request due to invalid syntax.  |
| **401** | Unauthorized | Authentication is required, and it has failed or has not yet been provided. |
| **403** | Forbidden | The server understood the request, but it refuses to authorize it.    |
| **404** | Not Found | The requested resource could not be found on the server.              |
| **500** | Internal Server Error | The server encountered an unexpected condition that prevented it from fulfilling the request. |
| **502** | Bad Gateway | The server was acting as a gateway or proxy and received an invalid response from the upstream server. |
| **503** | Service Unavailable | The server is not ready to handle the request, usually due to maintenance or overload. |

To handle these status codes effectively in your PowerShell script, you can use try-catch blocks to catch exceptions and inspect the status code. Here is an example:

```powershell
try {
    $response = Invoke-RestMethod -Uri "https://api.example.com/resource" -Method Get
    Write-Output "Request succeeded with status code: $($response.StatusCode)"
} catch {
    if ($_.Exception.Response.StatusCode -eq 400) {
        Write-Output "Bad Request: Check your request syntax."
    } elseif ($_.Exception.Response.StatusCode -eq 401) {
        Write-Output "Unauthorized: Check your authentication token."
    } elseif ($_.Exception.Response.StatusCode -eq 404) {
        Write-Output "Not Found: The requested resource does not exist."
    } else {
        Write-Output "An error occurred: $($_.Exception.Message)"
    }
}
```

This example demonstrates how to handle different HTTP status codes returned by `Invoke-RestMethod`. The same code can be used for `Invoke-WebRequest`.

[ [Top](#table-of-contents) ]

## PowerShell

PowerShell functions for upload and download a file from a GitLab project.

### Download a file from your GitLab project

Summary:

The `Invoke-DownloadFileFromGitLab` function downloads a file from a specified GitLab repository.
It takes parameters for the repository URL, file path, branch name, and destination path.
The function constructs the appropriate GitLab API URL, sends a request to download the file,
and saves the file to the specified destination on the local machine.

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
        # We use EscapeDataString to ensure that any special characters in the variables are encoded for use in a URL
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
        $ApiUrl = "$($GitLabBaseUrl)/api/v4/projects/$($GitLabProjectID)/repository/files/$($EncodedFilePath)/raw?ref=$($EncodedBranch)"
        try {
            $null = Invoke-RestMethod -Uri $ApiUrl -Headers $Headers -OutFile $LocalFilePath -Proxy $Proxy -ProxyUseDefaultCredentials
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

## Upload a file to your GitLab project

Summary:

The `Invoke-UploadFileToGitLab` function uploads a file to a specified GitLab repository.
It takes parameters for the repository URL, file path, branch name, and local file path.
The function constructs the appropriate GitLab API URL, checks if the file already exists,
and either updates the existing file or creates a new file in the specified branch of the repository.

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
        # We use EscapeDataString to ensure that any special characters in the variables are encoded for use in a URL
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

The functions above are written for Windows PowerShell and GitLab behind a Proxy with a little help from GitHub Copilot.

## GitLab CLI

Old school GitLab CLI with PowerShell and PAT.

```powershell
function Invoke-IXPushToGitLab{
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$GitLabToken,

        [Parameter(Mandatory=$false)]
        [string]$GitLabBaseUrl = 'gitlab.company.ch',

        [ValidateNotNullOrEmpty()]
        [Parameter(Mandatory=$true)]
        [string]$GitLabProject,

        [ValidateNotNullOrEmpty()]
        [Parameter(Mandatory=$true)]
        [string]$GitLabBranch,

        [ValidateNotNullOrEmpty()]
        [Parameter(Mandatory=$true)]
        [string]$FileToPush,

        [ValidateNotNullOrEmpty()]
        [Parameter(Mandatory=$true)]
        [string]$LocalFilePath
        )

    $GitLabRepo = "https://oauth2:$($GitLabToken)@$($GitLabBaseUrl)/$($GitLabProject).git"
    # git remote set-url origin $GitLabRepo
    $clone = git clone $GitLabRepo 2>"gitout.txt"

    Set-Location $LocalFilePath

    $pull = git pull $GitLabRepo $GitLabBranch 2>"gitout.txt"

    git add $FileToPush
    git commit -m "Automatic Update on $($FileToPush) at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git push $GitLabRepo $GitLabBranch 2>"gitout.txt"
    Remove-Item "gitout.txt" -confirm:$false -force
}
```

---

[ [Top](#table-of-contents) ]

## See also

[GitLab API Documentation](https://docs.gitlab.com/ee/api/)
