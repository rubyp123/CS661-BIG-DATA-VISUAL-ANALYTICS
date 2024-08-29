from vtk import *

# Load 3D data
reader = vtkXMLImageDataReader()
reader.SetFileName("Data/Isabel_3D.vti")
reader.Update()

# Creating color transfer function
color_tf = vtkColorTransferFunction()
color_tf.AddRGBPoint(-4931.54, 0.0, 1.0, 1.0)
color_tf.AddRGBPoint(-2508.95, 0.0, 0.0, 1.0)
color_tf.AddRGBPoint(-1873.9, 0.0, 0.0, 0.5)
color_tf.AddRGBPoint(-1027.16, 1.0, 0.0, 0.0)
color_tf.AddRGBPoint(-298.031, 1.0, 0.4, 0.0)
color_tf.AddRGBPoint(2594.97, 1.0, 1.0, 0.0)

# Creating opacity transfer function
opacity_tf = vtkPiecewiseFunction()
opacity_tf.AddPoint(-4931.54, 1.0)
opacity_tf.AddPoint(101.815, 0.002)
opacity_tf.AddPoint(2594.97, 0.0)

# Creating volume property
v = vtkVolumeProperty()
v.SetColor(color_tf)
v.SetScalarOpacity(opacity_tf)

user_input = int(input("Choose 0 for Without Phong Shading or 1 for With Phong Shading: "))
if(user_input==1):
    v.ShadeOn()  # Turn on shading
    # Set Phong shading parameters
    v.SetAmbient(0.5)
    v.SetDiffuse(0.5)
    v.SetSpecular(0.5)
elif(user_input!=0):
    print("Please Enter valid input")

# Create volume mapper
volume_mapper = vtkSmartVolumeMapper()
volume_mapper.SetBlendModeToComposite()  # Composite blending mode
volume_mapper.SetInputConnection(reader.GetOutputPort())

# Create volume
volume = vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(v)

# Create outline
outline = vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())


#create Text Actor
text = vtkTextActor()
text.SetTextScaleModeToNone()
if(user_input==0):
    text.SetInput("Without Phong shading")
    text.GetPositionCoordinate().SetValue(0.36, 0.05)  
else:
    text.SetInput("With Phong shading")
    text.GetPositionCoordinate().SetValue(0.38, 0.05)  

text.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
text.GetTextProperty().SetFontSize(20)
text.GetTextProperty().SetColor(0,0,0)  

# create mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(outline.GetOutputPort())

#create actor
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(0,0,0)

# Create renderer
renderer = vtkRenderer()
renderer.SetBackground(1,1,1)
renderer.AddVolume(volume)
renderer.AddActor(actor)
renderer.AddActor2D(text)


# Create render window
renderWindow = vtkRenderWindow()
renderWindow.SetSize(1000, 1000)
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)


# Start rendering
renderWindow.Render()
renderWindowInteractor.Start()
