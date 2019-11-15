#!/usr/bin/env python
from __future__ import print_function

import vtk

#Loader for our structured dataset
imageReader = vtk.vtkStructuredPointsReader()
imageReader.SetFileName("/Users/kylestrougo/Documents/GitHub/assignment-4-kylestrougo/data/foot.vtk")
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


#--------

# added function for color transfer
color_transfer = vtk.vtkColorTransferFunction()
color_transfer.AddRGBPoint(0, 0.520, 0.0, 0.0)
color_transfer.AddRGBPoint(120, 1.0, 0.68, 0.30)
color_transfer.AddRGBPoint(255, 1.0, 1.0, 1.0)


# added function for piecewise opacity
opacity = vtk.vtkPiecewiseFunction()
opacity.AddPoint(0,0)
opacity.AddPoint(12.9,0)
opacity.AddPoint(38.89,0.05687)
opacity.AddPoint(255.0,1.0)

# call to functions
volume_transfer = vtk.vtkVolumeProperty()
volume_transfer.SetColor(color_transfer)
volume_transfer.SetScalarOpacity(opacity)
volume_transfer.ShadeOn()

# mapper
ray_map = vtk.vtkGPUVolumeRayCastMapper()
ray_map.SetBlendModeToComposite()
ray_map.SetInputConnection(imageReader.GetOutputPort())

# set mapper and property
volume = vtk.vtkVolume()
volume.SetMapper(ray_map)
volume.SetProperty(volume_transfer)
#-----------

#A renderer that renders our geometry into the render window
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.1, 0.2)
renderer.SetViewport(0,0,1,1);

#Add actor and properties to our renderer
renderer.AddActor( outlineActor);
#TODO add volume

#--
renderer.AddActor(volume)

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

#----------

volume.GetMapper().AddClippingPlane(plane)

PlaneRep = vtk.vtkImplicitPlaneRepresentation()
PlaneRep.SetPlaceFactor(1.25)
PlaneRep.PlaceWidget(outlineActor.GetBounds())

PlaneRep.SetNormal(plane.GetNormal())

#-----------

plane_Wid = vtk.vtkImplicitPlaneWidget2()

plane_Wid.SetInteractor(interactor)
plane_Wid.SetRepresentation(PlaneRep)

plane_Wid.AddObserver("InteractionEvent", planeCallback)

plane_Wid.On()

#----------

interactor.Initialize()
interactor.Start()
