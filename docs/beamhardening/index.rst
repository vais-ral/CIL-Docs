.. bhc documentation master file, created by
   sphinx-quickstart on Tue Feb 21 17:34:52 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to BHC CarouselFit documentation
========================================

This is a brief outline of the software package for fitting carousel or
crown image data to a model of the energy dependent reponse function
of the X-ray system (source, filters, detector).
Using this fit a correction curve can be defined to map observed attenuation
to expected monochromatic attenuation for a given material at a defined energy.
This mapping function can then be used in either pre-processing the X-ray
projections or as an input to the reconstruction software.

Requirements:

This software is written in Python 2.
Non-standard python modules needed are:

* ``scipy``
* ``matplotlib``
* ``tifffile``

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   project
   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
