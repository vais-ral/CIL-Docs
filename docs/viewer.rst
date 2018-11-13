Viewer
======

A simple Viewer for 3D data built with VTK and Python.

The interactive viewer CILViewer2D provides:

- Orthoslicer (slice in x/y/z direction)
- keyboard interaction
    - 'x' slices on the YZ plane
    - 'y' slices on the XZ plane
    - 'z' slices on the XY
    - 'a' auto window/level to accomodate all values
    - 's' save render to PNG (current_render.png)
- slice up/down: mouse scroll (10 x pressing SHIFT)
- Window/Level: ALT + Right Mouse Button + drag.
    Horizontal motion modifies the window, vertical motion modifies the level.
- Pan: CTRL + Right Mouse Button + drag
- Zoom: SHIFT + Right Mouse Button + drag (up: zoom in, down: zoom out)
- Pick: Left Mouse Click
- ROI (square):
    This is implemented as a 3D object. Any slices in front of the ROI will hide the box. Any slices
    located behind the ROI will still show the ROI as they are behind a transparent 3D object. Switching between the
    orientations should make it clear which region is being selected.

    The histogram is displayed based on the current 2D slice which has its boundaries within the 2D extent of the ROI.

    Mouse/Keyboard Interactions:
    
    - Create ROI: CTRL + Left Mouse Button 
    - Resize ROI: Left Mouse Button on one of the hotspots + drag
    - Translate ROI: Middle Mouse Button within ROI
    - Delete ROI: ALT + Left Mouse Button



Usage
-----

.. code-block:: python

    import vtk
    import os
    from ccpi.viewer.CILViewer2D import CILViewer2D

    fn = "./data/head.mha"

    reader = vtk.vtkMetaImageReader()
    reader.SetFileName(fn)
    reader.Update()

    v = CILViewer2D()
    v.style.debug = True
    v.setInput3DData(reader.GetOutput())
    v.startRenderLoop()

Screenshots
-----------

View along X-axis:

.. image:: https://github.com/vais-ral/CILViewer/raw/master/pics/sliceXPick.png

Window/Level Adjust:

.. image:: https://github.com/vais-ral/CILViewer/raw/master/pics/windowLevel.png

Region of Interest (ROI):

.. image:: https://github.com/vais-ral/CILViewer/raw/master/pics/ROI.png

Line Profiler:

.. image:: https://github.com/vais-ral/CILViewer/raw/master/pics/line.png

Zoom:

.. image:: https://github.com/vais-ral/CILViewer/raw/master/pics/zoom.png
