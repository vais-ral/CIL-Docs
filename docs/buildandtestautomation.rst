Build and Test Automation
=========================

These CCPi modules are built automatically from Github repository:

* Pre-Processing - https://github.com/vais-ral/CCPi-PreProcessing
* Reconstruction - https://github.com/vais-ral/CCPi-reconstruction
* Astra toolbox wrapper - https://github.com/vais-ral/CCPi-astra
* Framework - https://github.com/vais-ral/CCPi-Framework
* Framework Plugins - https://github.com/vais-ral/CCPi-FrameworkPlugins
* Regularisation Toolkit - https://github.com/vais-ral/CCPi-Regularisation-Toolkit
* [draft] Quantification - https://github.com/vais-ral/CCPi-Quantification

With following limitation:

* every commit to master branch is built and binary is uploaded into anaconda channel `ccpi`.
* every pull request is built, but no binaries are uploaded
* commit to non-master branch is not built
* the result of built and test process is available in on top of the github page

* version is determined from last git tag and number of commits after this tag, e.g. `0.10.3_103` means 103 commits after last tagged version `0.10.3`.
* if number of commits after tagged version is 0, then this built is assumed production
* if number of commits after tagged version is greater than 0, then this built is labeled as `dev` 

Recommended setting in continuous integration
---------------------------------------------

Automatic build process can be triggered by various events. The recommended events ar `push` and `pull-request`. 
A so called "Webhook" can be configured in Github to send a notification about an event to third party application. 
Jenkins (or any other CI tool) can be configured to listen to such notification and launch configured action, i.e. build process.

CCPi modules with source codes at https://github.com/vais-ral/ are configured with proprietar installation of Jenkins at https://anvil.softeng-support.ac.uk/. 
This service is provided for UK academics community. However, the following is recommended to be set in any Jenkins deployment 
for every CCPI-[module]:

Production built for CCPi-[module_name]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To configure build action on `push` event on `master` branch received from Github do following in Jenkins:
  1) Create new project by: ``choose folder``, New Item, Enter Item Name: ``CCPi-[module-name]``, Freestyle project
  2) Enter these values: [x] Github project -> Project URL: ``https://github.com/vais-ral/CCPi-[module_name]/``
  * [x] Restrict where this project can be run -> Label Expression ``sl7``  (choose this to scientific linux, ubuntu or any linux based machine)
  * Source code management -> [x] Git -> 
    - Repositories, Repository URL: ``https://github.com/vais-ral/CCPi-[module_name].git``
    - Branches to build, branch specifier: ``*/master``
    - Additional Behaviours, Check out to specific local branch 
  * Build triggers, [x] Github hook trigger for GITScm polling
  * Execute shell::
  
  .. code::

    module load conda
    #commented version = version will be determined from git tag and number commits
    #export CIL_VERSION=0.10.3
    export CCPI_CONDA_TOKEN=[conda token to upload to ccpi channel]
    #build and upload
    . build/jenkins-build.sh

In Github project -> Settings -> Webhooks
  * Add new Webhook
  * Payload URL: ``https://anvil.softeng-support.ac.uk/jenkins/github-webhook/``
  * Which events would you like to trigger: [x] Just push event.    

Development built for pull request on CCPi-[module_name]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To configure build action on `pull-request` event on any branch received from Github do following in Jenkins:

  1) Create new project by: ``choose folder``, New Item, Enter Item Name: ``CCPi-[module-name]``, Freestyle project
  2) Enter these values: 
  * [x] Github project -> Project URL: ``https://github.com/vais-ral/CCPi-[module_name]/``
  * [x] Restrict where this project can be run -> Label Expression ``sl7``  (choose this to scientific linux, ubuntu or any linux based machine)
  * Source code management -> [x] Git -> 
    - Repositories, Repository URL: ``https://github.com/vais-ral/CCPi-[module_name].git``
    - Advanced:
      + Name: ``origin``
      + Refspec: ``+refs/pull/*:refs/remotes/origin/pr/*``      
    - Branches to build, branch specifier: ``**``
    - Additional Behaviours:
      + Advanced clone behaviours: 
        + Fetch tags [x] 
        + Honor refspec on initial clone [x] 
      + Check out to specific local branch 
  * Build triggers, [x] Poll SCM
  * Execute shell::
  
  .. code::
  
    module load conda
    #commented version = version will be determined from git tag and number commits
    #export CIL_VERSION=0.10.3
    export CCPI_CONDA_TOKEN=[conda token to upload to ccpi channel]
    #build and upload
    . build/jenkins-build.sh

In Github project -> Settings -> Webhooks
  * Add new Webhook
  * Payload URL: ``https://anvil.softeng-support.ac.uk/jenkins/git/notifyCommit?url=http://github.com/vais-ral/CCPi-[module_name].git``
  * Which events would you like to trigger: 
    - [x] Let me select individual events
    - [x] Pull request

