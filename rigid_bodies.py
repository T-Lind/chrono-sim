import pychrono as chrono
import pychrono.irrlicht as chronoirr

# Smooth contacts for collisions
my_system = chrono.ChSystemSMC()

# The collision system to use. "Bullet" is just the name of the library used
my_system.SetCollisionSystem(chrono.ChCollisionSystemBullet())

body_b = chrono.ChBody()
body_b.SetMass(10)
body_b.SetInertiaXX(chrono.ChVectorD(4, 4, 4))
body_b.SetPos(chrono.ChVectorD(0.2, 0.4, 2.0))
body_b.SetPos_dt(chrono.ChVectorD(0.1, 0.0, 0.0))
body_b.SetCollide(True)

coll_mat = chrono.ChMaterialSurfaceSMC()

sphere_body = chrono.ChBodyEasySphere(
    0.5,
    1000,
    True,  # Visualization
    True,  # Collision
    coll_mat
)

sphere_body.SetPos(chrono.ChVectorD(0, 0, 0))
sphere_body.SetPos_dt(chrono.ChVectorD(0, 0, 0))
my_system.AddBody(sphere_body)
# Create the Irrlicht visualization


vis = chronoirr.ChVisualSystemIrrlicht()
vis.AttachSystem(my_system)
vis.SetWindowSize(1024, 768)
vis.SetWindowTitle('Collision visualization demo')
vis.Initialize()
vis.AddLogo(chrono.GetChronoDataFile('logo_pychrono_alpha.png'))
vis.AddSkyBox()
vis.AddCamera(chrono.ChVectorD(0, 8, 6))
vis.AddTypicalLights()


class DebugDrawer(chrono.VisualizationCallback):
    def __init__(self):
        super().__init__()


    def DrawLine(self, pA, pB, color):
        print("   pA = ", pA.x, pA.y, pA.z)
        print("   pB = ", pB.x, pB.y, pB.z)


# Create collision shape drawer
drawer = DebugDrawer()
my_system.GetCollisionSystem().RegisterVisualizationCallback(drawer)

# Specify what information is visualized
mode = chrono.ChCollisionSystem.VIS_Shapes

use_zbuffer = True

#  Run the simulation
while vis.Run():
    vis.BeginScene()
    vis.Render()
    vis.EndScene()
    my_system.DoStepDynamics(1e-3)

    # print(sys.GetChTime(), "  ", sys.GetNcontacts())
    my_system.GetCollisionSystem().Visualize(chrono.ChCollisionSystem.VIS_Shapes)
