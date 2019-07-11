Introduction
======================

The CCPi Core Imaging Library (CIL) consists of five main modules. These are part of work flow for the CT based experiments data analysis. The five main modules are :

* Pre-Processing
* Reconstruction
* Segmentation
* Quantification
* Viewer

The pre-processing module provides the methods for modifying the raw data from the instruments before performing the reconstruction, for example: Beam hardening for Lab based instruments (cone beam). 

The Reconstruction module provides the methods for reconstructing the volume using the projection data. Currently this module consists of only iterative methods. there are several FBP based methods in other libraries, which is not provided in CIL.

The Segmentation module provides the methods to extract or segment the reconstruction volume with the regions of interest. Currently there is only a topology based segmentation method available.

The Quantification module provides the methods for quantiying the segmented volume.
