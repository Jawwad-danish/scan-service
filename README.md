# Scan Service
AlphaScale (AS) Backend (BE) Scan Service
A REST API to create and manage scans.

## Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Deployment](#deployment)
- [Application Properties Instructions](#ApplicationPropertiesInstructions)
- [Tests](#tests)


## Features and Entities
The service includes the following features

- **product**   
- **component**  
- **scan types**
- **scan profile**
- **setup scan**

## Prerequisites
- Python 3
- requirement.txt file (included in the repository) must be installed.
- MariaDB
- Docker

## Installation
- Clone the repository
```bash
$ git clone https://github.com/Auxin-io/as-be-scan-svc.git
```

- Edit docker file. Change the following environment variables according to your environment.
```bash

USER_NOTF_API_BASE_URL - base url for the user notification service.
SSO_API_BASE_URL - base url for the sso service.
USER_API_BASE_URL - base url for the user service.
ALPHA_SCALE_DB_USER - mariadb Database username
ALPHA_SCALE_DB_PASSWORD - mariadb Database Password
ALPHA_SCALE_DB_HOST - mariadb Database host address
ALPHA_SCALE_DB_PORT - mariadb Database port (should be 3306 for mariadb)
ALPHA_SCALE_DB_DATABASE - mariadb Database name
ENV DEFECT_DOJO_BASE_URL - defect dojo api base url
ENV DEFECT_DOJO_USERNAME - defect dojo username
ENV DEFECT_DOJO_PASSWORD - defect dojo password
ENV JENKINS_BASE_URL - jenkins base url
ENV JENKINS_USERNAME - jenkins username
ENV JENKINS_PASSWORD - jenkins password

```
- build docker file.
```bash
$ docker build -t {image_name} .
```

- run docker image you created

- Required Databases and specific image version
  Note: Without the correct database the user service won't work.
- Databse version: 20211222
