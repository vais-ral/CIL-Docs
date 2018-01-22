
# coding: utf-8

# In[3]:


import numpy
import matplotlib.pyplot as plt
from ccpi.instrument import Diamond
from ccpi.reconstruction.experiment import TomographyExperiment
import vtk

from ccpi.viewer.CILViewer2D import CILViewer2D, Converter
from ccpi.viewer.CILViewer import CILViewer




#%%




# 1 create a Tomography Experiment
experiment = TomographyExperiment()
experiment.debug = False



#%%


# 1 go to the instrument 
instrument = Diamond()
instrument.debug = False



#%%



experiment.setParameter(instrument=instrument)



#%%



#and make data acquisition
if False:
    ## load a NeXus file 
    filename = r"../../data/24737_fd.nxs"
    instrument.loadNexus(filename)





else:
    # load Phantom
    stack = numpy.load(r'../../data/projections_PhantomSpheres_256_3.npy')
    angles= numpy.load(r'../../data/angles_PhantomSpheres_256_3.npy')
    instrument.setParameter(normalized_projections = stack, angles = angles)




#%%



experiment.printAvailableReconstructionAlgorithms()


#%%


# create a reconstructor helper
experiment.createReconstructor('cgls_tv', debug=True)
experiment.getParameter('reconstructor').setParameter(iterations=50, 
                       regularization_parameter=3e-4,
                       threads=4)

#%%

#reconstruct

vol = experiment.reconstruct(iterations=5)
#vol = experiment.reconstruct()


#%%


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

if False:
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
else:
    viewer = CILViewer2D()
    viewer.setInputAsNumpy(vol)
    viewer.startRenderLoop()
