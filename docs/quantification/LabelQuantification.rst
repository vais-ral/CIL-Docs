Label Quantification
*********************

This algorithm takes in a labelled image and calculates several characteristics for each label. Below are some of the characteristics 

* Volume by voxel counts
* Equivalent sphere diameter by voxel counts
* Bounding box diagonal
* Principal Component Analysis (PCA)
* Ellipsoid fitting by PCA
* Equivalent circle diameter by PCA
* Isosurface by marching cude.
* Surface area
* Surface Volume
* Equivalent sphere diameter from surface volume
* Sphercity
* Normalised surface area to volume ratio (Radius*Sa/Vol)

The details of this algorithm are given in Evaluation of 3D bioactive glass scaffolds dissolution in a perfusion flow system with X-ray microtomography. Yue S, Lee PD, Poologasundarampillai G, Jones JR. DOI: 10.1016/j.actbio.2011.02.009

API
----

.. code-block:: python
	LabelQuantificationUShort(input_3d_volume, origin, voxel_size, min_data_value, max_data_value, minimum_feature_size)
	

Example
--------

.. code-block:: python
  
    # Imports
    from ccpi.quantification import LabelQuantificationUShort
    import numpy as np
    import math
    from tifffile import TiffFile        
	
	#Read the input volume
    img = TiffFile('test/FoamData.tif')        
    data = img.asarray()
	
	#voxel size
    voxel_size = np.ones(3,dtype=float)
	#origin
    origin = np.zeros(3,dtype=int)
	
	#computes the 3d quantification
    lqs = LabelQuantificationUShort(data, origin, voxel_size, float(np.amin(data)), float(np.amax(data)), 100.0)
    lqs.compute()
	
	#returns the quantified values
    output = lqs.getOutput()
	
    print(output)
    img.close()