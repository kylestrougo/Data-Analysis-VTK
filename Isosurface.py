#!/usr/bin/env python
from __future__ import print_function

import vtk

#Interactor style that handles mouse and keyboard events
class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self,parent=None):
        self.parent = vtk.vtkRenderWindowInteractor()
        if(parent is not None):
          self.parent = parent
        self.AddObserver("KeyPressEvent",self.keyPress)

    def keyPress(self,obj,event):
      key = self.parent.GetKeySym()
      
      if(key == "Up"):
        #TODO: have this increase the isovalue
        print("Down")
        value = hydrogen.GetValue(0) + 0.03
        if value < 1.00:
            #update value
            hydrogen.SetValue(0, value)
            iso_actor.GetProperty().SetColor(color_change.GetColor(value))
            # print new value
            iso_txt.SetInput('Isovalue: ' + str(value))

            renwin.Render()

        print("Up")


      if(key == "Down"):
        #TODO: have this decrease the isovalue
        print("Down")
        value = hydrogen.GetValue(0) - 0.03
        if value > 0:
          #update value
          hydrogen.SetValue(0, value)
          iso_actor.GetProperty().SetColor(color_change.GetColor(value))
          # print new value
          iso_txt.SetInput('isovalue: ' + str(value))

          renwin.Render()



#Loader for our structured dataset
imageReader = vtk.vtkStructuredPointsReader()
#Paraview application

# local hydrogen location
imageReader.SetFileName("/Users/kylestrougo/Documents/GitHub/assignment-4-kylestrougo/data/hydrogen.vtk")

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

#TODO:
#
#Insert isosurfacing, scalebar, and text code here
#isosurfacing :

hydrogen = vtk.vtkMarchingCubes();
hydrogen.SetInputConnection(imageReader.GetOutputPort());
hydrogen.SetValue(0, 0.10)
hydrogen.Update()


iso_mapper = vtk.vtkPolyDataMapper()
iso_mapper.SetInputConnection(hydrogen.GetOutputPort())


#scalebar :
color_change = vtk.vtkColorTransferFunction()
color_change.SetColorSpaceToRGB()
color_change.AddRGBPoint(0.0, 0.0, 1.0, 0.0)
color_change.AddRGBPoint(1.0, 1.0, 1.0, 1.0)

color_bar = vtk.vtkScalarBarActor()
color_bar.SetLookupTable(color_change)
color_bar.SetWidth(0.13)
color_bar.SetHeight(0.85)
color_bar.SetLabelFormat("%.5g")
color_bar.SetTitle("Probability")
color_bar.VisibilityOn()

#text (just as an actor) :
iso_txt = vtk.vtkTextActor();
iso_txt.SetInput("Isovalue: 0.10");
txtprop=iso_txt.GetTextProperty()
txtprop.SetFontSize(15)
txtprop.SetColor(1,1,1)
iso_txt.SetDisplayPosition(15,25)

#Iso actor:
iso_actor = vtk.vtkActor()
iso_actor.GetProperty().SetColor(color_change.GetColor(0.10))
iso_actor.SetMapper(iso_mapper)
iso_actor.GetMapper().ScalarVisibilityOff()

#A renderer that renders our geometry into the render window
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.1, 0.2)

#Add actors to our renderer
renderer.AddActor(outlineActor)
#personal actors added:
renderer.AddActor(iso_actor)
renderer.AddActor(iso_txt)
renderer.AddActor(color_bar)


#The render window
renwin = vtk.vtkRenderWindow()
renwin.SetSize( 512, 512);
renwin.AddRenderer(renderer)

#Interactor to handle mouse and keyboard events
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetInteractorStyle(MyInteractorStyle(parent = interactor))
interactor.SetRenderWindow(renwin)

interactor.Initialize()
interactor.Start()
