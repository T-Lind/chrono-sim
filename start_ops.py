import pychrono as chrono
import numpy as np
from numpy import linalg as LA

chrono.GetLog().Bar()
chrono.GetLog() << "result is: " << 11 + 1.5 << "\n"
chrono.GetLog().Bar()

my_vect1 = chrono.ChVectorD()
my_vect1.x = 5
my_vect1.y = 2
my_vect1.z = 3

my_vect2 = chrono.ChVectorD(3, 4, 5)
my_vect4 = my_vect1 * 10 + my_vect2
my_len = my_vect4.Length()
print('Vector sum is', my_vect1 + my_vect2)
print("Vector cross is", my_vect1 % my_vect2)
print("Vector dot is", my_vect1 ^ my_vect2)

x = chrono.ChMatrixDynamicD(3,3)
print(x.setitem(0, 0, 1))
print(x.getitem(0, 0))
