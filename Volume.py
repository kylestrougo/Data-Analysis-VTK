#!/usr/bin/env python
from __future__ import print_function

import vtk

#Loader for our structured dataset
imageReader = vtk.vtkStructuredPointsReader()
imageReader.SetFileName("./data/tooth.vtk")
imageReader.Update()

#Print dimensions and range of the 3d image
dims = imageReader.GetOutput().GetDimensions()
print("Dimensions of image: " + str(dims[0]) + " x "
      + str(dims[1]) + " x " + str(dims[2]))
range = imageReader.GetOutput().GetScalarRange();
print("Range of image: " + str(range[0]) + " to " +  str(range[1]))

#create an outline that shows the bounds of our dataset
outline = vtk.vtkOutlineFilter();
outline.SetInputConnection(imageReader.GetOutputPort());
#mapper to push the outline geometry to the graphics library
outlineMapper = vtk.vtkPolyDataMapper();
outlineMapper.SetInputConnection(outline.GetOutputPort());
#actor for the outline to add to our renderer
outlineActor = vtk.vtkActor();
outlineActor.SetMapper(outlineMapper);
outlineActor.GetProperty().SetLineWidth(2.0);

#used for clipping plane
plane = vtk.vtkPlane();


#TODO Part 1 and Part 2


#A renderer that renders our geometry into the render window
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.1, 0.2)
renderer.SetViewport(0,0,1,1);

#Add actor and properties to our renderer
renderer.AddActor( outlineActor);
#TODO add volume


#The render window
renwin = vtk.vtkRenderWindow()
renwin.AddRenderer(renderer)
renwin.SetSize( 512, 512)

#Move camera
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(-70);
renderer.ResetCameraClippingRange();
renwin.Render()

#Interactor to handle mouse and keyboard events
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renwin)

# A Callback function
def planeCallback(object, event):
  global plane
  object.GetRepresentation().GetPlane(plane)

#TODO Part 2


interactor.Initialize()
interactor.Start()
