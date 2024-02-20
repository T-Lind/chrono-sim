import pychrono as chrono

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

my_system.AddBody(body_b)
