# HandlingDeploymentFailure_AutomatedWay_GCP_CICD
Handling GCP CICD Depolyment failure automated way
# Infra-Build-Notification-RUN
Terraform to build required infra to support Handling Build Failure in Automated way
## **Contents**
1. [Scope](#Scope)
2. [Overview](#Overview)
3. [Prerequisites ?](#Prerequisites?)
    * [Git_Personal_Access_token ](#Git_Personal_Access_token)
    * [repo_name](#repo_name)
    * [branch_name](#branch_name)
    * [trigger_name](#trigger_name)

## Scope <a name="Scope"></a>
>The Solution has two components -
1. Create Required Infra in GCP to support the automation in handling cloud build Failures
2. Web Application (Flask) hosted on Cloud Run
This document explains the neccessary steps required to create Web Application (Flask) hosted on Cloud Run. Please refer [Infra required for build notification](https://github.com/addy3352/Infra-Build-Notification-RUN/edit/main/README.md).
## Overview <a name="Overview"></a>
The Solution will direct Build notifications to go to Pub-SUB topic where subscription will be created to push “Failure notification” to flask application (web application) hosted on Cloud Run. The web application will extract build_id from the failure notification and then extract trigger name and last successful commit_id for the trigger. Based on the trigger name , the web application will revert respective git branches to the extracted commit_id. The Changes in git branches will subsequently trigger build to roll back all changes to previous successful version. As shown above, system is restored to last successful version which is commit:2.

Flask application will get the trigger name and last successful commit id from the build history. Based on the trigger name , respective git repositories need to be cloned and checked out to commit id extracted and pushed to the last successful commit.
## Prerequisites <a name="Prerequisites"></a>
1. Git personal token access — This needs to be added in the code. Can be found Setting > Developer Settings >Personal access tokens
2. Git branch name
3. Git Repo Name
4. trigger name
