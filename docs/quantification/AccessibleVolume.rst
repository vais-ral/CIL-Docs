Accessible Volume
******************

The algorithm takes in a binary 3D image (Usually a scaffold images) and calculates the accessible volume for a range of sphere sizes. The algorithm also takes in input mask which defines the boundary of the volume from where the accessibility is measured. The algorithm is described in Sheng Yue PhD thesis. (http://dx.doi.org/10.1016/j.jmatprotec.2014.05.006)

API
----
.. code-block:: python
   
   AccessibleVolumeInput(voxel_size, origin, input_data, mask_data)
   
   voxel_size: numpy array with sizes along 3 dimensions (x_size,y_size,z_size)
   origin: numpy array with origin of the volume (x_center, y_center, z_center)
   input_data: numpy array 3d volume and has to be an 8bit data.
   mask_data: numpy array 3d mask volume and it has to be an 8bit data.

.. code-block:: python
   
   AccessibleVolume(input_volume, sphere_diameter_range_min_in_log, sphere_diameter_range_max_in_log, number_of_spheres_in_range, input_image_resolution)
   
   input_volume: of type AccessibleVolumeInput
   sphere_diameter_range_min_in_log: logarithmic value of minimum sphere diameter range that need to be used in calculating accessible volume.
   sphere_diameter_range_max_in_log: logarithmic value of maximum sphere diameter range that need to be used in calculating accessible volume.
   number_of_spheres_in_range: the number of spheres diameters that are used in the input sphere diameter range for which accessible volume is calculated.
   input_image_resolution: image resolution usually (1.0).

   returns: AccessibleVolume object
   
   AccessibleVolume.compute()
   
   This method invokes the computation.
   
   AccessibleVolume.getAccessibleVolume()
   
   This method returns a list with sphere diameter and its corresponding accessible volume.
   
Example
--------

To run the example code you need to download the following files :download:`Input Data <../../test/Data128.tif>` and :download:`Mask Data <../../test/DataMask128.tif>`

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
   
.. image:: ../../pics/AccessibleVolume.jpg   