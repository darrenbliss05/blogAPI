# blogapi

#### Table of Contents

1. [Description](#description)
1. [Setup - The basics of getting started with blogapi](#setup)
    * [What blogapi affects](#what-blogapi-affects)
    * [Setup requirements](#setup-requirements)
    * [Beginning with blogapi](#beginning-with-blogapi)
1. [Usage - Configuration options and additional functionality](#usage)
1. [Reference - An under-the-hood peek at what the module is doing and how](#reference)
1. [Limitations - OS compatibility, etc.](#limitations)
1. [Development - Guide for contributing to the module](#development)

## Description

This module installs a blogapi service that runs on linux. This was created in 
response to a blog post assignment from NWEA.

The api runs on port 8080 and support posting a blog entry and getting all of 
the blog entries. The goal of the application is to provide an interface for 
other applications.

The installation can either be done with puppet (this repository is a puppet 
module) or this can be installed manually. For manual installation refer to the 
file manualinstall in this repository. The rest of this document will discribe
how to install using puppet. 

## Setup

### What blogapi affects **OPTIONAL**

Dependencies: This module automatically installs the python packages:
    daemonize, flask, flask_sqlalchemy, sqlalchemy, flask_marshmallow, 
    marshmallow-sqlalchemy 

### Setup Requirements **OPTIONAL**


1. This module requires the pip installer to install the required python 
packages.  The installation of pip is outside the scope of this module.

This module will fail if pip is not installed. You should already have a puppet
module in place to install and manage pip. If you do not have pip installed 
you can run the following commands on the system that will run blogapi to 
install pip. 

     % cd /tmp
     % wget https://bootstrap.pypa.io/get-pip.py
     %  python get-pip.py

2. This module requiries a user account to run the daemon. The default is to 
   run it as root but that is not advised. It is beyond the scope of this
   module to create user accounts. The next section explains how to 
   configure the module for a specific user account.


### Beginning with blogapi

The very basic steps needed to get the module up and running. 
1. Download this repository from github into your modules area. If you are using
   r10k then you can just add this to the Puppetfile.
2. Application Puppet and hiera confguration settings. Adjust these to meet 
    your site requirements. 

     blogapi::install_path :: This is the installation and run area for the 
             application. blogapi will look for the database file and 
             configure file in this directory. 
       Default: /opt/blogapi

     blogapi::logfile_path  :: Defines the location for the application logfile.
       Default: /opt/blogapi

     blogapi::pidfile_path :: This defines the location for the pidfile. The
             pidfile holds the pid of the active daemon. This is also used by
             the application to shutdown the daemon. 
       Default: /opt/blogapi

     blogapi::database_file :: This is the name of the database file. 
       Default: blog.db

     blogapi::user :: For the module this defines the ownership of the 
              installation area and all of the files within.
       Default: root

     blogapi::group :: For the module this defines the group ownership of the
              installation area and all of the files within. 
       Default: root

3. Adjust your hiera configuration for the system you will be running blogapi 
   on.  Once puppet has installed this module you will need to manually 
   start the daemon. 

## Usage

The useage for blogapi is simple. 

To start the daemon (assuming path /opt/blogapi)
   As the user account run

   % /opt/blogapi/blogapi.py 

   This starts the process up as a daemon. The blogapi.py.pid contains the 
   pid of the process.

To shutdown the daemon use the following command

   % /opt/blogapi/blogapi.py stop 
   
   NOTE: This has a dependancy on the pid file.

To run the process in non-daemon mode use the command below. This is only 
recommended for debugging.

   % /opt/blogapi/blogapi.py --debug

For testing the tcsh script testbasicapi provides examples on how to use
curl to test both PUT and GET functionality. If you run the script as is it
 will perform a GET and then 2 PUTs.

## Reference


## Limitations

This was designed on Centos 7 and only tested for Redhat based systems. This 
module will only install the application on a Redhat based system. Time did not
allow for testing on other version of linux so this version is limited to 
Redhat based systems.   

The manifests/params.pp file is controlling which platforms/OSes this module
will install onto. To install this on a untested OS update manifests/params.pp
to include your OS.
 
## Development

This is a As is module. There are currently no plans to release any updates to
this module.
## Release Notes/Contributors/Etc. **Optional**
