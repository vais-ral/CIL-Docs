
# coding: utf-8

# ## Core Imaging Library 0.9.1
# 
# ### Training 1: Iterative Reconstruction
# 
# #### Installing
# The Core Imaging Library is available as conda packages. We are going to install the reconstruction package.
# 
# ```conda install ccpi-reconstruction=0.9.1```
# 
# ### Usage
# 
# There are a number of steps to do to perform a reconstruction:
# 
# 1. load the data
# 2. find the center of rotation 
# 3. pass the relevant data to the reconstruction algorithm
# 
# We will introduce 2 helper classes which are meant to ease this process:
# 
# 1. The `TomographyExperiment` class
# 2. The `Instrument` class
# 
# #### Instrument class

# In[6]:


from ccpi.instrument import Diamond
import h5py
import numpy
import matplotlib.pyplot as plt
from ccpi.viewer.CILViewer2D import CILViewer2D, Converter



#nx = h5py.File(r'../../data/phant3D_256.h5', "r")
#ph = numpy.asarray(nx.get('/dataset1'))
#phantom = numpy.asarray(ph[10:250,:,20:240], dtype=numpy.float32)
#
phantom = numpy.load(r'../../data/PhantomSpheres_256_3.npy')
print ("phantom " ,phantom.min(), phantom.max())
#%%

clip = lambda x,m: x if x < 0.7 else m
clipper = numpy.frompyfunc(clip,2,1)
#phantom2 = clipper(phantom,0)
phantom2= phantom.copy()
phantom2 [numpy.where(phantom2>0.70)] = 1e-3
print ("phantom2 " ,phantom2.min(), phantom2.max())
#%%
nangles = 91
angles = numpy.linspace(-90,90, nangles, dtype=numpy.float32)

diamond = Diamond()
#
stack = diamond.doForwardProject(phantom, angles, negative=True , normalized=True)
# the cgls doesn't like 0's and more the 1s	
stack [numpy.where(stack<=0)] = 1e-3
stack [numpy.where(stack>1)] = 1 - 1e-3

#
## clip negative values and normalize
#clip = lambda x,v,m: x if x < m else v
#clipper = numpy.frompyfunc(clip,3,1)
#norm = clipper(stack,0.001,0.001)
#print ("norm " ,norm.min(), norm.max())
#norm = norm/norm.max()
### absorption is from 0 to 1 where 0 is max density
#norm = 1 - norm
#print ("stack " ,norm.min(), norm.max())
#norm = clipper(norm,0.001, 0.001)
#print ("stack " ,norm.min(), norm.max())
##stack = numpy.transpose(stack, axes=[0,2,1]).copy()
#
numpy.save(r'../../data/projections_PhantomSpheres_256_3.npy', stack)
numpy.save(r'../../data/angles_PhantomSpheres_256_3.npy', angles)


back = diamond.doBackwardProject()
center_of_rotation = diamond.getParameter('center_of_rotation')
print ("Center Of Rotation: {0}".format(center_of_rotation))


cols = 2
rows = 1
current = 0
fig = plt.figure()

current = current + 1
if cols >= current:
	a=fig.add_subplot(rows,cols,current)
	a.set_title('forward projections')
	imgplot = plt.imshow(stack[20])
	current = current + 1

if cols >= current:
	a=fig.add_subplot(rows,cols,current)
	a.set_title('back projections')
	imgplot = plt.imshow(back[20])
	current = current + 1


plt.show()

viewer = CILViewer2D()
viewer.setInputAsNumpy(phantom)
viewer.startRenderLoop()

