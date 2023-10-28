---
layout: post
title:  "GitLab Pipeline"
author: Tinu
categories: "GitLab"
tags:   PowerShell
permalink: /posts/:title:output_ext
---

# Table of Contents
<!-- TOC -->

- [Table of Contents](#table-of-contents)
- [GitLab Pipeline](#gitlab-pipeline)
    - [Rules](#rules)
    - [Stages](#stages)
    - [Jobs](#jobs)
    - [Extends](#extends)
    - [Includes](#includes)
    - [Script](#script)
    - [Example 1](#example-1)
    - [Troubleshooting](#troubleshooting)
- [See also](#see-also)

<!-- /TOC -->

# GitLab Pipeline

GitLab Pipeline is your friend - UNDER CONSTRUCTION!

A GitLab CI/CD pipeline is the file ````.gitlab-ci.yml```` in the root of your project.

## Rules

````
if: $CI_PIPELINE_SOURCE == 'merge_request_event'
if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
````

## Stages

List of stages for jobs, and their order of execution. If stages is not defined in the ````.gitlab-ci.yml```` file, the default pipeline stages are:

````
.pre
build
test
deploy
.post
````

## Jobs

Hidden Jobs begin with a point in the name ````.cleanup_git````.

````
.cleanup_git:
  stage: .post
  script:
    - echo "Running Job $CI_JOB_NAME, $CI_COMMIT_BRANCH!"
````

Normal Job:

````
test-node-yaml-test:
  rules:
    - if: $CI_COMMIT_TITLE =~ /TEST:.*/
  tags: [auto-deploy-test]
  extends: .test_node_yaml
````

## Tags

````
````

## Extends

Reuse the configuration or Scripts.

````
extends: .test_node_yaml # included script
extends: .deploy_script  # hidden job
````

## Includes

Configurations and Scripts outside of the ````.gitlab-ci.yml````.

````
include: 
  - local: '/CI/init-env.yml'
  - local: '/CI/build-job.yml'
  - local: '/CI/test-job.yml'
  - local: '/CI/deploy-job.yml'
  - local: '/CI/cleanup-runner.yml'
````

## Script

A Script can be either a single Command or a Scriptblock.

Single Command:

````
script:
  - echo "Running Job $CI_JOB_NAME, $CI_COMMIT_BRANCH!"
````

Scriptblock:

````
script: |
  Write-Host "Start Job-ID $($CI_JOB_ID), Job-Name $($CI_JOB_NAME)"
  if(-not(Test-Path D:\Pikett-Scripts)){
    New-Item D:\Pikett-Scripts -ItemType Directory -Force | Select LastWriteTime, Length, Name, Fullname
  }
  Copy-Item "*.ps1" "D:\Pikett-Scripts" -PassThru -Force | Select LastWriteTime, Length, Name, Fullname
  if($LastExitCode -gt 0) { Throw "LastExitCode $($LastExitCode)" }
  Write-Host "End Job-ID $($CI_JOB_ID), Job-Name $($CI_JOB_NAME)"
````

## Example 1

````powershell
# A pipeline is composed of independent jobs that run scripts, grouped into stages.
# Stages run in sequential order, but jobs within stages run in parallel.
# For more information, see: https://docs.gitlab.com/ee/ci/yaml/index.html#stages

workflow:
  name: 'Pipeline for do anything for me'
  rules:
    - if: $CI_PIPELINE_SOURCE == 'merge_request_event'
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

stages:
  - test
  - deploy
  - cleanup

test-job:
  stage: test
  tags: [gitlab-runner-tag]
  script:
    - echo "Running $CI_JOB_NAME, $CI_COMMIT_BRANCH!"

deploy-job:
  stage: deploy
  tags: [gitlab-runner-tag]
  script:
    - echo "Running $CI_JOB_NAME, $CI_COMMIT_BRANCH!"

cleanup-job:
  stage: cleanup
  tags: [gitlab-runner-tag]
  script:
    - echo "Running $CI_JOB_NAME, $CI_COMMIT_BRANCH!"
````

## Troubleshooting

````powershell

````

# See also

[CI/CD pipelines](https://docs.gitlab.com/ee/ci/pipelines/) on GitLab docs
