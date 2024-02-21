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
    ground.SetBodyFixed(True)
    if not pos:
        pos = chrono.ChVectorD(0, -1, 0)
    ground.SetPos(pos)
    return ground


def load_step_body(file_name: str, part_name: str, mass=3, pos: chrono.ChVectorD = None):
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

            return mbody

        else:
            raise RuntimeError(f"Error: cannot retrieve the shape named {part_name}")
    else:
        print("Error: cannot load the file.")


# Smooth contacts for collisions
system = chrono.ChSystemNSC()

# The collision system to use. "Bullet" is just the name of the library used
system.SetCollisionSystem(chrono.ChCollisionSystemBullet())
coll_mat = chrono.ChMaterialSurfaceNSC()

system.AddBody(setup_ground(3, 3))

body = load_step_body('MotorAssembly.step', 'Assembly/Body')
motor = load_step_body('MotorAssembly.step', 'Assembly/Motor')
shaft = load_step_body('MotorAssembly.step', 'Assembly/Shaft')


body_motor_fixed = chrono.ChLinkLockLock()
body_motor_fixed.Initialize(body, motor, chrono.ChCoordsysD(chrono.ChVectorD(0, 0, 0), chrono.Q_from_AngAxis(chrono.CH_C_PI / 2, chrono.ChVectorD(1, 0, 0))))

motor_shaft_revolute = chrono.ChLinkLockRevolute()
motor_shaft_revolute.Initialize(motor, shaft, chrono.ChCoordsysD(chrono.ChVectorD(0, 0, 0), chrono.Q_from_AngAxis(chrono.CH_C_PI / 2, chrono.ChVectorD(1, 0, 0))))


actuator = chrono.ChLinkMotorRotationTorque()
actuator.Initialize(shaft, motor, chrono.ChFrameD(chrono.ChVectorD(0, 0, 1)))
actuator.SetTorqueFunction(chrono.ChFunction_Const(1))

system.AddBody(body)
system.AddBody(motor)
system.AddBody(shaft)
system.Add(body_motor_fixed)
system.Add(motor_shaft_revolute)
system.Add(actuator)

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
        print(f"Time is {system.GetChTime():.1f}")
        last_tenth_sec_passed = system.GetChTime()
