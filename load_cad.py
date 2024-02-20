import pychrono as cno
import pychrono.cascade as cascade
import pychrono.irrlicht as irr
from OCC.Core.TopoDS import TopoDS_Shape

system = cno.ChSystemNSC()

coll_mat = cno.ChMaterialSurfaceNSC()

# ground object
ground = cno.ChBodyEasyBox(1, 0.05, 1, 100, True, True, coll_mat)
ground.SetPos(cno.ChVectorD(0, -1, 0))
ground.SetBodyFixed(True)
system.Add(ground)

# Load cad model top.stl
my_doc = cascade.ChCascadeDoc()
# load_ok = my_doc.Load_STEP('C:/Users/tenant/PycharmProjects/chrono-sim/top.stp')
load_ok = my_doc.Load_STEP(cno.GetChronoDataFile('cascade/assembly.stp'))
# cno.ChCollisionModel.SetDefaultSuggestedEnvelope(0.002)
# cno.ChCollisionModel.SetDefaultSuggestedMargin(0.001)

body_1 = cno.ChBody()
if load_ok:
    shape_1 = TopoDS_Shape()
    if (my_doc.GetNamedShape(shape_1, "Assem1/body1")):
        mbody_1 = cascade.ChCascadeBodyEasy(shape_1, 1000, True, True, coll_mat)
        mbody_1.SetMass(1)
        print("Loaded assembly.")
        mbody_1.SetPos(cno.ChVectorD(0, 0, 0))
        mbody_1.SetPos_dt(cno.ChVectorD(0, 0.05, 0))


        system.Add(mbody_1)

    else:
        print("Error: cannot retrieve the shape named automotive_design")
else:
    print("Error: cannot load the file.")

# Create a visualization application
# Create the Irrlicht visualization
vis = irr.ChVisualSystemIrrlicht()
vis.AttachSystem(system)
vis.SetWindowSize(1024, 768)
vis.SetWindowTitle('CAD demo')
vis.Initialize()
vis.AddLogo(cno.GetChronoDataFile('logo_pychrono_alpha.png'))
vis.AddSkyBox()
vis.AddCamera(cno.ChVectorD(0.1, 0.2, -0.3))
vis.AddTypicalLights()

# Specify what information is visualized
mode = cno.ChCollisionSystem.VIS_Shapes

#  Run the simulation
while vis.Run():
    vis.BeginScene()
    vis.Render()
    vis.EndScene()
    system.DoStepDynamics(1e-3)

    # print(sys.GetChTime(), "  ", sys.GetNcontacts())
    system.GetCollisionSystem().Visualize(cno.ChCollisionSystem.VIS_Shapes)
