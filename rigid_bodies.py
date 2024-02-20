import pychrono as chrono
import pychrono.irrlicht as chronoirr

# Smooth contacts for collisions
my_system = chrono.ChSystemNSC()

# The collision system to use. "Bullet" is just the name of the library used
my_system.SetCollisionSystem(chrono.ChCollisionSystemBullet())
coll_mat = chrono.ChMaterialSurfaceNSC()

# box for the ground, it'll be fixed so the ball can bounce on it
ground = chrono.ChBodyEasyBox(
    10, 0.1, 10,
    100,  # Density
    True,  # Visualization
    True,  # Collision
    coll_mat
)
ground.SetBodyFixed(True)
ground.SetPos(chrono.ChVectorD(0, -1, 0))
my_system.AddBody(ground)


sphere_body = chrono.ChBodyEasySphere(
    0.5,
    100,
    True,  # Visualization
    True,  # Collision
    coll_mat
)
sphere_body.SetMass(10)
sphere_body.SetPos(chrono.ChVectorD(0, 0, 0))
sphere_body.SetPos_dt(chrono.ChVectorD(4, 10, 0.05))  # This gives the ball an initial upward velocity of 10 and moves towards the cylinder to knock it over
my_system.AddBody(sphere_body)


cylindrical_body = chrono.ChBodyEasyCylinder(
    chrono.ChAxis_Y,
    0.25,
    7.5,
    100,
    True,  # Visualization
    True,  # Collision
    coll_mat
)
cylindrical_body.SetMass(10)
cylindrical_body.SetPos(chrono.ChVectorD(3, 3, 0))
cylindrical_body.SetPos_dt(chrono.ChVectorD(1, 1, 0))

# Set acceleration along the axis of the cylinder
# cylindrical_body.SetRot_dt(chrono.Q_from_AngAxis(chrono.CH_C_PI / 4, chrono.ChVectorD(3, 0, 0)))
my_system.AddBody(cylindrical_body)

# Create the Irrlicht visualization
vis = chronoirr.ChVisualSystemIrrlicht()
vis.AttachSystem(my_system)
vis.SetWindowSize(1024, 768)
vis.SetWindowTitle('Rigid Body Demo')
vis.Initialize()
vis.AddLogo(chrono.GetChronoDataFile('logo_pychrono_alpha.png'))
vis.AddSkyBox()
vis.AddCamera(chrono.ChVectorD(0, 8, 6))
vis.AddTypicalLights()


# Specify what information is visualized
mode = chrono.ChCollisionSystem.VIS_Shapes

#  Run the simulation
i = 0
while vis.Run():
    vis.BeginScene()
    vis.Render()
    vis.EndScene()
    my_system.DoStepDynamics(1e-3)

    my_system.GetCollisionSystem().Visualize(chrono.ChCollisionSystem.VIS_Shapes)
    if i % 1000 == 0:
        print(f"Cylinder position: {cylindrical_body.GetPos()}, velocity: {cylindrical_body.GetPos_dt()}, acceleration: {cylindrical_body.GetPos_dtdt()}")
    i += 1
