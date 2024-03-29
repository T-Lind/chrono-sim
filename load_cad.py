import pychrono as chrono
import pychrono.cascade as cascade
import pychrono.irrlicht as irr
from OCC.Core.TopoDS import TopoDS_Shape

system = chrono.ChSystemNSC()

coll_mat = chrono.ChMaterialSurfaceNSC()

# ground object
ground = chrono.ChBodyEasyBox(1, 0.05, 1, 100, True, True, coll_mat)
ground.SetPos(chrono.ChVectorD(0, -0.25, 0))
ground.GetVisualShape(0).SetTexture(chrono.GetChronoDataFile("textures/concrete.jpg"))
ground.SetBodyFixed(True)
ground.SetMass(100)
system.Add(ground)

# Load cad model top.stl
my_doc = cascade.ChCascadeDoc()

load_ok = my_doc.Load_STEP('Part1.step')
# chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.002)
# chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.001)

body_1 = chrono.ChBody()
if load_ok:
    shape_1 = TopoDS_Shape()
    part_name = "Part 1"
    if my_doc.GetNamedShape(shape_1, part_name):  # Assem1/body1 is the name of the shape in the STEP file
        mbody_1 = cascade.ChCascadeBodyEasy(shape_1, 1000, True, True, coll_mat)

        # Most of the time, you'd run something like the following to get it right side up
        rot_1 = chrono.Q_from_AngAxis(chrono.CH_C_PI / 2, chrono.ChVectorD(1, 0, 0))  # Rotate 90 degrees on X axis
        rot_2 = chrono.Q_from_AngAxis(chrono.CH_C_PI, chrono.ChVectorD(0, 1, 0))  # Rotate 180 degrees on vertical Y axis
        tot_rotation = rot_1 % rot_2  # This operator is just regular quaternion product

        root_frame = chrono.ChFrameMovingD(chrono.ChVectorD(0, 0, 0), tot_rotation)
        mbody_1.ConcatenatePreTransformation(root_frame)

        mbody_1.SetMass(1)  # Setting the mass to 0 would mean no gravity
        print("Loaded assembly.")
        mbody_1.SetPos(chrono.ChVectorD(0, 0, 0))
        mbody_1.SetPos_dt(chrono.ChVectorD(0, 1, 0))
        mbody_1.SetRot_dt(chrono.Q_from_AngAxis(chrono.CH_C_PI / 4, chrono.ChVectorD(0, 0, 7)))
        # For above:
        # First argument sets velocity to flip it vertically, second rotates about the hole axis, third along the other


        system.Add(mbody_1)

    else:
        raise RuntimeError(f"Error: cannot retrieve the shape named {part_name}")
else:
    print("Error: cannot load the file.")

# Create a visualization application
# Create the Irrlicht visualization
vis = irr.ChVisualSystemIrrlicht()
vis.AttachSystem(system)
# vis.SetWindowSize(1024, 768)
vis.SetWindowTitle('CAD demo')
vis.Initialize()
vis.AddLogo(chrono.GetChronoDataFile('logo_pychrono_alpha.png'))
vis.AddSkyBox()
vis.AddCamera(chrono.ChVectorD(0.1, 0.2, -0.3))
vis.AddTypicalLights()

# Specify what information is visualized
mode = chrono.ChCollisionSystem.VIS_Shapes

#  Run the simulation
while vis.Run():
    vis.BeginScene()
    vis.Render()
    vis.EndScene()
    system.DoStepDynamics(1e-3)

    # print(sys.GetChTime(), "  ", sys.GetNcontacts())
    system.GetCollisionSystem().Visualize(chrono.ChCollisionSystem.VIS_Shapes)
