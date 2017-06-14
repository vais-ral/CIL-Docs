Beam Hardening Correction based on sample imaging
=================================================

This python code is based on a IDL package written by Anthony Evershed at QMUL.
The purpose is to take a set of X-ray images obtained under the same conditions
and at the same time as the sample that is being imaged on the X-ray CT machine.
By fitting a model of the energy dependent response of the system to the observed
attenuation of a set of well characterised flat plates it is them possible to
generate a correction function that maps from observed attenuation of the
polychromatic beam to the expected attenuation of a monochromatic beam at a specified
energy.
Using this correction function as a pre-processing step before CT reconstruction then
helps to minimise beam hardening artifacts in single material samples.

A user guide is included in the software to help set up the description of the crown
or carousel device that is needed to measure the attenuation. The software offers a
simple interactive command line interface, or can be run with predefined script files.

The software consists of two main source files and a post-processing file:

* ``runCarouselFit.py``
  This is the main program to run which acts as a simple command line iterpreter.
  A set of commands read the necessary data files, sets parameters and then solves
  the least squares problem. Plotting of the input data and the output results is
  supported to allow evaluation of the fit.

* ``carouselUtils.py`` 
  This file defines a few class objects which read and fit the data. Use is made of
  scipy module for least squares fitting. This file is imported by ``runCarouselFit``.

* ``applyTransform.py``
  This is a support program to apply the fitted correction transform to images for the
  reconstruction. It is run independently to the above program after that has produced
  correction polynomials.
