
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


nx = h5py.File(r'../../data/phant3D_256.h5', "r")
ph = numpy.asarray(nx.get('/dataset1'))

phantom = numpy.asarray(ph[10:250,:,20:240], dtype=numpy.float32)
nangles = 60
angles = numpy.linspace(0,360, nangles, dtype=numpy.float32)

diamond = Diamond()

stack = diamond.doForwardProject(phantom, angles)
print ("stack " ,stack.min(), stack.max())


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

