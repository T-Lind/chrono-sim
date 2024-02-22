import pychrono as chrono
import pychrono.cascade as cascade
import pychrono.irrlicht as chronoirr
from OCC.Core.TopoDS import TopoDS_Shape


def setup_ground(x: float, y: float, coll_mat=None, pos=None):
    if not coll_mat:
        coll_mat = chrono.ChMaterialSurfaceNSC()
    ground = chrono.ChBodyEasyBox(
        x, 0.01, y,
        100,  # Density
        True,  # Visualization
        True,  # Collision
        coll_mat
    )
    ground.GetVisualShape(0).SetTexture(chrono.GetChronoDataFile("textures/concrete.jpg"))
    ground.SetBodyFixed(True)
    if not pos:
        pos = chrono.ChVectorD(0, -0.02, 0)
    ground.SetPos(pos)
    return ground


def load_step_body(file_name: str, part_name: str, mass: float = 3, pos: chrono.ChVectorD = None, texture=None):
    my_doc = cascade.ChCascadeDoc()
    load_ok = my_doc.Load_STEP(file_name)

    if load_ok:
        shape = TopoDS_Shape()
        if my_doc.GetNamedShape(shape, part_name):  # Assem1/body1 is the name of the shape in the STEP file
            mbody = cascade.ChCascadeBodyEasy(shape, 1000, True, True, coll_mat)

            # Most of the time, you'd run something like the following to get it right side up
            rot_1 = chrono.Q_from_AngAxis(chrono.CH_C_PI / 2, chrono.ChVectorD(1, 0, 0))  # Rotate 90 degrees on X axis
            rot_2 = chrono.Q_from_AngAxis(chrono.CH_C_PI,
                                          chrono.ChVectorD(0, 1, 0))  # Rotate 180 degrees on vertical Y axis
            tot_rotation = rot_1 % rot_2  # This operator is just regular quaternion product

            root_frame = chrono.ChFrameMovingD(chrono.ChVectorD(0, 0, 0), tot_rotation)
            mbody.ConcatenatePreTransformation(root_frame)

            mbody.SetMass(mass)  # Setting the mass to 0 would mean no gravity
            print(f"Loaded {part_name}.")
            if pos:
                mbody.SetPos(pos)

            if texture:
                mbody.GetVisualShape(0).SetTexture(texture)

            return mbody

        else:
            raise RuntimeError(f"Error: cannot retrieve the shape named {part_name}")
    else:
        print("Error: cannot load the file.")


# Smooth contacts for collisions
system = chrono.ChSystemNSC()

chrono.ChCollisionModel_SetDefaultSuggestedMargin(0.1)
chrono.ChCollisionModel_SetDefaultSuggestedEnvelope(0.1)

# The collision system to use. "Bullet" is just the name of the library used
system.SetCollisionSystem(chrono.ChCollisionSystemBullet())
coll_mat = chrono.ChMaterialSurfaceNSC()

system.AddBody(setup_ground(3, 3))

# Note: list of default textures can be found here: https://github.com/projectchrono/chrono/tree/main/data/textures
base = load_step_body('JustMotorTest.step', 'JustMotorTest/Base', mass=9,
                      texture=chrono.GetChronoDataFile("textures/blue.png"))
shaft = load_step_body('JustMotorTest.step', 'JustMotorTest/Shaft', mass=0.3,
                       texture=chrono.GetChronoDataFile("textures/bluewhite.png"))

# setup revolute

# setup torque motor
motor = chrono.ChLinkMotorRotationTorque()

system.AddBody(base)
system.AddBody(shaft)

my_motor = chrono.ChLinkMotorRotationTorque()
my_motor.Initialize(base, shaft, base.GetPos())
my_motor.SetTorqueFunction(chrono.ChFunction_Const(10))

system.AddBody(my_motor)

# Create the Irrlicht visualization
vis = chronoirr.ChVisualSystemIrrlicht()
vis.AttachSystem(system)
vis.SetWindowSize(1024, 768)
vis.SetWindowTitle('Rigid Body Demo')
vis.Initialize()
vis.AddLogo(chrono.GetChronoDataFile('logo_pychrono_alpha.png'))
vis.AddSkyBox()
vis.AddCamera(chrono.ChVectorD(0.3, 0.3, 0.6))
vis.AddTypicalLights()

# Specify what information is visualized
mode = chrono.ChCollisionSystem.VIS_Shapes

#  Run the simulation
last_tenth_sec_passed = 0
while vis.Run():
    vis.BeginScene()
    vis.Render()
    vis.EndScene()
    system.DoStepDynamics(1e-3)

    system.GetCollisionSystem().Visualize(chrono.ChCollisionSystem.VIS_Shapes)

    if system.GetChTime() - last_tenth_sec_passed > 0.1:
        print(f"Time is {system.GetChTime():.1f}, Motor angle is {motor.GetMotorRot()} degrees.")
        last_tenth_sec_passed = system.GetChTime()
