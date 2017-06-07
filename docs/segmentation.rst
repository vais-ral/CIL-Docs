Segmentation Module
======================
=================================
Simpleflex Segmentation Algorithm
=================================

The CIL provides the Segmentation Algorithm described by Carr et al. [Carr2003]_ based on the calculation of the contour tree. 
The algorithm is developed in C++ and it is fully wrapped in Python. 

Segmentation is the process from which, given a 3 dimensional dataset (volume), surfaces in the volume are found at a 
specific value. Such surfaces are also called isosurfaces.

The algorithm expects to receive a 3D numpy array as input, and outputs a numpy array with the location of 
the points of the isosurfaces in space. 
It must be pointed out that there are at least 2 reference system of the points
of an image: 

- Image Coordinate: the actual pixel number in each dimension
- World Coordinate: the location in the *real world*
  
World coordinates are generally linear transformation of the image coordinate. For example, the size of the pixel 
may not be uniform in the 3 dimensions resulting in a stretched image in some direction. 

The algorithm itself has no clue about the World coordinate and its output is in image coordinate. The user is required to apply
the appropriate transformations to translate image coordinates to world coordinates. In the example that follows we will make a 
image-to-world transformation. 

------------
Installation
------------

A binary installation is available from the ccpi conda channel:

::
   conda install -c ccpi ccpi-segmentation=0.1 

-----
Usage
-----
The Python wrapper for the CIL uses numpy arrays as medium to pass data to and from each algorithm. 
3D image data should be passed to the simpleflex algorithm in form of 3D numpy arrays. 

The algorithm outputs numpy arrays.

The wrapper is written following an Object Oriented paradigm


.. [Carr2003] Carr, H., Snoeyink, J., & Axen, U. (2003). Computing contour trees in all dimensions.
              Computational Geometry: Theory and Applications, 
              24(2), 75–94. https://doi.org/10.1016/S0925-7721(02)00093-7
