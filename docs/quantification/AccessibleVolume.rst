Accessible Volume
******************

The algorithm takes in a binary 3D image (Usually a scaffold images) and calculates the accessible volume for a range of sphere sizes. The algorithm also takes in input mask which defines the boundary of the volume from where the accessibility is measured. The algorithm is described in Sheng Yue PhD thesis. (http://dx.doi.org/10.1016/j.jmatprotec.2014.05.006)

API
----
.. code-block:: python
   
   AccessibleVolumeInput(voxel_size, origin, input_data, mask_data)

.. code-block:: python
   
   AccessibleVolume(input_volume, sphere_diameter_range_min_in_log, sphere_diameter_range_max_in_log, number_of_spheres_in_range, input_image_resolution)

Example
--------

.. code-block:: python

   from ccpi.quantification import AccessibleVolumeInput, AccessibleVolume
   import numpy as np
   import math
   from tifffile import TiffFile    
   #input 3d data volume, has to be binary volume.
   data = TiffFile('test/Data128.tif')
   #input 3d mask
   mask = TiffFile('test/DataMask128.tif')
   #voxel size
   voxel_size = np.ones(3,dtype=float)
   #voxel origin
   origin = np.zeros(3,dtype=int)
   #Create an input structure to be passed to the accessible algorithm
   input = AccessibleVolumeInput(voxel_size, origin, data.asarray(), mask.asarray())
   #Invoke the Accessible volume algorithm
   av = AccessibleVolume(input, math.log(80.0), math.log(600.0), 11, 9.0)
   av.compute() #do the computation, this can be a lengthly process.
   
   #get the accessible volume for each sphere diameter
   output = av.getAccessibleVolume()
   print(output)
   data.close()
   mask.close() 