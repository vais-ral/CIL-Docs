Developer's guide
#################


CORE (C/C++) built as library
	C/C++ API
Wrappers:
	Python
	Avizo
	Paraview
	Tomviz 

	

Essential Tools
***************

The development cycle of the CIL requires the usage of a few common tools:

  1. git and GitHub
  2. CMake
  3. Anaconda and conda build
  
These tools are meant to simplify the development cycle, but the developer is required to have some confidence in the use of them. Mostly, one would be modifying existing files, but you never know.

Directory structure
===================

Each CIL repository (public or private) is organized in subdirectories as follows:

::

  project_name/
    CMake/
    CMakeLists.txt
    License.txt
    Core/
    recipes/
    Wrappers/
        Python/
        Avizo/
        Paraview/
        Tomviz/

Git and GitHub
==============		
Code development is done via git on (public or private) repositories. The master branch should contain only the latest development stable code. Each new feature should be implemented on a separate branch. Merging of new features on the ``master`` branch is done via Pull Requests (PR).

We strongly encourage the use of issues, milestones and projects on GitHub to keep track of the development cycle.

Typical Workflow:

1) Use your branch for big and small changes
2) Pull from master frequently to reduce the amount of work needed when merging
3) Use pull requests (PR) to add features in the master, even if you merge them yourself. The best way is to branch from master, make the patch and issue a PR
4) Use issues for bugs, proposals and discussions in general. You can assign issues to someone to require their attention.
5) Close issues when possible. Use “closes #N” with N issue number in messages of commits when your commit fixes an issue. https://help.github.com/articles/closing-issues-using-keywords/
 
Some git commands
-----------------

.. code-block :: text
 
  git status
  git diff filename
  git add filename
  git commit
  git commit –m “message”
  git pull origin <branch>
  git push origin <branch>
  git rebase –i HEAD~4     # rebases interactively the last 3 commits: read the screen
  git checkout <branch>    # to change the actual local branch
  git checkout –b <branch> # to create and checkout a new local branch
  git branch -d <branch>   # to delete a local branch

 
**On conflict read what git says**. Modify the files that git says need attention. You will find in those files some lines like these:

.. code-block :: text

  <<<<<<< HEAD
    <link type="text/css" rel="stylesheet" media="all" href="style.css" />
  =======
    <!-- no style -->
  >>>>>>> master

**your branch** is between HEAD and =====, master is between ===== and master. Once removed that 
``git commit``


CMake
=====

Building of the CIL modules is done with CMake, and each module will contain the appropriate ``CMakeList.txt`` files. Although one could build the Core with CMake alone, we often use conda to build the Core library.

Anaconda
========

Install Anaconda or Miniconda. 
``conda`` is a package manager system and virtual environment manager, possibly `more <https://www.anaconda.com/what-is-anaconda/>`_
. 

Managing environments
-----------------------


With conda you can install multiple python versions and use them at the same time without messing around with your system python installation. 

The first thing to do is to create an environment. This is achieved by:

.. code-block ::

  conda create --name <environment_name> python=3.5 <other packages>
  
Basically this instructs conda to create an environment named ``<environment_name>`` with python 3.5. You can also specify a list of other packages you want to install in your enviroment at creation time. 

You can delete an environment by:

.. code-block ::
  
  conda remove --name <environment_name> --all
  
Refer to the `main conda docs <https://conda.io/docs/user-guide/tasks/manage-environments.html>`_ for further information.

Installing packages
-------------------

The basic install command is 

``conda install <package-name>=<version>``

``conda`` searches and installs packages from its main source ``anaconda.com``.  It is possible to add sources (channels) of packages from ``anaconda.org`` which is a community driven repository. This can be forced on ``conda`` by 

``conda install <package-name>=<version> -c <channel-name>``

One may add a number of channels and they should be searched in the order in which you provide them. I find it easier to use the ``.condarc`` file to specify the channels:

.. code-block :: text

  channels:
    - ccpi
    - conda-forge
    - defaults
  anaconda_upload: false

This instructs conda to search with higher priority the ccpi channel, followed by conda-forge and last default. Notice that any package which may reside on a different channel cannot be installed unless the channel is passed to conda. 
  
Building with Conda
*******************

While building with conda, conda creates an environment for the purpose, copies all the relevant data, issues cmake and packages everything. It's pretty neat but it must be configured. This configuration is called conda recipe.

We will cover the building with conda in 2 steps: 

1) building with a conda recipe that exist and works
2) creating a conda recipe

During the development cycle you will be faced with building your software again and again. The suggestion here is to continue to use a conda build as it keeps things organized. Therefore you will be faced more often with case 1), i.e. building with a pre-existing and working conda recipe. When a new package is created, a new conda recipe must be written. This will happen with less frequency, and I will cover it later.

Building with existing conda recipe
===================================

In the CIL there are basically 3 kinds of packages:
  1. Shared libraries
  2. Python wrappers (or other)
  3. Pure Python packages


To compile a shared library:
  1. start in the main repository directory
  2. ``export CIL_VERSION=someversion``
  3. ``conda build recipes/library --numpy 1.12 --python 3.5`` (adjust the python version)
  4. ``conda install cil_libraryname=someversion  --use-local --force``

To compile a Python wrapper to a shared library or a pure Python package:
  1. in the Wrappers/Python directory
  2. ``conda build conda-recipe --numpy 1.12 --python 3.5``
  3. ``conda install ccpi-pythonpackagename=someversion --use-local --force``

When launching the build you may have activated an environment or not. I suggest to activate an environment with most of the needed packages as the conda build will be quicker. **It is fundamental to have an environment activated when installing**.
Notice that there isn't any dependency check when installing local packages. 
Notice that you will have to force installation whenever the version of the package doesn't change.

When builds end prematurely (on errors), conda will not remove the build tree. Every now and again issue a 

``conda build purge``

to clean your hard drive.


Writing a conda recipe
======================

The conda build requires the presence of the so-called `conda recipe <https://conda.io/docs/user-guide/tasks/build-packages/recipe.html>`_
. A recipe lives in a directory where there are 2 or 3 files.

.. code-block :: text
  
  recipe/
    meta.yaml
    bld.bat
    build.sh

The ``meta.yaml`` file contains informations about the package that will be created, its dependency at run time and at build time. The ``bld.bat`` and ``build.sh`` are files invoked by ``conda`` during the build process and are dependent on the system: windows or unix.

In the following a ``meta.yaml`` for one of the ccpi packages. It should be self evident that one describes the package, its dependencies at runtime and build-time.

.. code-block :: yaml

  package:
    name: cil_regularizer
    version: {{ environ['CIL_VERSION'] }}

  build:
    preserve_egg_dir: False
    script_env: 
      - CIL_VERSION

  requirements:
    build:
      - boost ==1.64.0	
      - boost-cpp ==1.64.0 
      - python 3.5 # [py35]
      - python 2.7 # [py27]
      - cmake >=3.1
      - vc 14 # [win and py35] 
      - vc 9  # [win and py27]
      - numpy

    run:
      - boost ==1.64.0
      - vc 14 # [win and py35]
      - vc 9  # [win and py27]
      - python 3.5 # [py35]
      - python 2.7 # [py27]
      - numpy

  about:
    home: http://www.ccpi.ac.uk
    license: Apache v2.0
    summary: Regularizer package from CCPi

In the ``build.sh`` one specifies how to build the package. 

.. code-block :: text

  #!/usr/bin/env bash

  mkdir build
  cd build

  #configure
  BUILD_CONFIG=Release
  echo `pwd`
  cmake .. -G "Ninja" \
      -Wno-dev \
      -DCMAKE_BUILD_TYPE=$BUILD_CONFIG \
      -DCMAKE_PREFIX_PATH:PATH="${PREFIX}" \
      -DCMAKE_INSTALL_PREFIX:PATH="${PREFIX}" \
      -DCMAKE_INSTALL_RPATH:PATH="${PREFIX}/lib"

  # compile & install
  ninja install

There are a number of `environment variables <https://conda.io/docs/user-guide/tasks/build-packages/environment-variables.html>`_  that are set by conda, like ``${PREFIX}``. 



Building Core with conda

1) Clone the git repository git clone https://github.com/vais-ral/CCPi-FISTA_Reconstruction.git
2) Create a directory for the builds outside of the source directory
3) conda create –name cil –python=3.5 –numpy=1.12
4) module load python/anaconda (optional, depends on the actual machine installation)
5) source activate cil