
# coding: utf-8

# In[3]:


import numpy
import matplotlib.pyplot as plt
from ccpi.instrument import Diamond
from ccpi.reconstruction.experiment import TomographyExperiment
import vtk

# 1 create a Tomography Experiment
experiment = TomographyExperiment()
experiment.debug = False
# 1 go to the instrument 
instrument = Diamond()
instrument.debug = False

experiment.setParameter(instrument=instrument)

#and make data acquisition
## load a NeXus file 
filename = r"../../data/24737_fd.nxs"
instrument.loadNexus(filename)

experiment.printAvailableReconstructionAlgorithms()
# create a reconstructor helper
experiment.createReconstructor('cgls', debug=False)
experiment.getParameter('reconstructor').setParameter(iterations=20)



#reconstruct

vol = experiment.reconstruct(iterations=10)
#vol = experiment.reconstruct()

norm = instrument.getParameter('normalized_projections')

print ("input data (sinogram) dimensions ")
print ( "X Y Z: {0}".format(numpy.shape(norm)) )
print ("X = angle projection {0}".format(numpy.shape(norm)[0]))
print ("Y = vertical {0}".format(numpy.shape(norm)[1]))
print ("Z = horizontal {0}".format(numpy.shape(norm)[2]))

print ("Ouput data dimensions")
print ( "X Y Z: {0}".format(numpy.shape(vol)) )
print ("X = horizontal X {0}".format(numpy.shape(vol)[0]))
print ("Y = horizontal Y {0}".format(numpy.shape(vol)[1]))
print ("Z = vertical {0}".format(numpy.shape(vol)[2]))

no=60

na, nver, nhor = numpy.shape(norm)
vh1, vh2, vvert = numpy.shape(vol)

cols = 2
rows = 1
current = 1
fig = plt.figure()
# projections row
a=fig.add_subplot(rows,cols,current)
a.set_title('exp projections\n {0}\nangles {1} \nvertical {2}\nhorizontal {3}'.format(numpy.shape(norm),
                                                                                      na, nver, nhor))
imgplot = plt.imshow(norm[no])

current = current + 1
a=fig.add_subplot(rows,cols,current)
a.set_title('reconstructed volume slice \n{0}\nhorizontalX {1}\n horizontalY {2}\n vertical {3}'.format(numpy.shape(vol),
                                                                                                      vh1,vh2,vvert))
imgplot = plt.imshow(vol[80])


plt.show()
from ccpi.segmentation.SimpleflexSegmentor import SimpleflexSegmentor
from ccpi.viewer.CILViewer2D import CILViewer2D, Converter
from ccpi.viewer.CILViewer import CILViewer


segmentor = SimpleflexSegmentor()
segmentor.setInputData(vol)
segmentor.calculateContourTree()
segmentor.setIsoValue(6000.)
print ('construct isosurfaces')
#segmentor.constructIsoSurfaces()
segmentor.updateTreeFromLogTreeSize(0.4)
print ('construct isosurfaces done')
surf_list = segmentor.getSurfaces()

#mask = segmentor.getSurfaceAsMask(0, labelIso=1, labelHigh=2, labelLow=0)
#print ("Volume of iso %d" % segmentor.isoVolume)
#print ("Volume of lower %d" % segmentor.lowVolume)
#print ("Volume of higher %d" % segmentor.highVolume)
## reshape the mask as the original data
#mask = numpy.reshape(mask, numpy.shape(vol))

def surf2PolyData(surf_list, limit):
    ########################################################################
    # 7. Display isosurfaces in 3D
    # with the retrieved data we construct polydata actors to be displayed
    # with VTK. Notice that this part is VTK specific. However, it shows how to
    # process the data returned by the algorithm.
    
    # Create the VTK output
    # Points coordinates structure
    triangle_vertices = vtk.vtkPoints()
    #associate the points to triangles
    triangle = vtk.vtkTriangle()
    # put all triangles in an array
    triangles = vtk.vtkCellArray()
    isTriangle = 0
    nTriangle = 0
    
    surface = 0
    # associate each coordinate with a point: 3 coordinates are needed for a point
    # in 3D. Additionally we perform a shift from image coordinates (pixel) which
    # is the default of the Contour Tree Algorithm to the World Coordinates.
    
    #origin = reader.GetOutput().GetOrigin()
    #spacing = reader.GetOutput().GetSpacing()
    origin = [0,0,0]
    spacing = [1,1,1]
    
    # augmented matrix for affine transformations
    mScaling = numpy.asarray([spacing[0], 0,0,0,
                                                  0,spacing[1],0,0,
                                                  0,0,spacing[2],0,
                                                  0,0,0,1]).reshape((4,4))
    mShift = numpy.asarray([1,0,0,origin[0],
                                                0,1,0,origin[1],
                                                0,0,1,origin[2],
                                                0,0,0,1]).reshape((4,4))
    
    mTransform = numpy.dot(mScaling, mShift)
    point_count = 0
    surf_count = 0
    #for surf in surf_list:
    while (surf_count < limit and surf_count < len(surf_list) ):
        surf = surf_list[surf_count]
        print("Image-to-world coordinate trasformation ... %d" % surface)
        for point in surf:
            world_coord = numpy.dot(mTransform, point)
            xCoord = world_coord[0]
            yCoord = world_coord[1]
            zCoord = world_coord[2]
            triangle_vertices.InsertNextPoint(xCoord, yCoord, zCoord);
    
    
            # The id of the vertex of the triangle (0,1,2) is linked to
            # the id of the points in the list, so in facts we just link id-to-id
            triangle.GetPointIds().SetId(isTriangle, point_count)
            isTriangle += 1
            point_count += 1
    
            if (isTriangle == 3) :
                isTriangle = 0;
                # insert the current triangle in the triangles array
                triangles.InsertNextCell(triangle);
    
        surface += 1
    
        # polydata object
        trianglePolyData = vtk.vtkPolyData()
        trianglePolyData.SetPoints( triangle_vertices )
        trianglePolyData.SetPolys(  triangles  )
        
        surf_count += 1

    return trianglePolyData
###############################################################################

trianglePolyData = surf2PolyData(surf_list, 2)

viewer = CILViewer()
viewer.setInputAsNumpy(vol)
viewer.displaySliceActor(42)
viewer.displayPolyData(trianglePolyData)
viewer.startRenderLoop()

if True:
    
    viewer = CILViewer2D()
    viewer.setInputAsNumpy(vol)
    viewer.startRenderLoop()

