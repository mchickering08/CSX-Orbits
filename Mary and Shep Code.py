#Construct a model that has two masses
#Properties of your two masses should be consistent with the attributes of a star and a planet
#The only constraints on your model should be that the two masses interact solely by the Law of Gravity

'''
Mary:
Planet class
- sat_x_init
- sat_y_init
- sat_vx_init
- Sat_vy_init
Ability to create a planet with those variables (not all)
'''

import math
import matplotlib.pyplot as plt


G = 6.67e-11 #gravity ofc 
class Planet:
    def __init__(self, name, mass, x_init, y_init, vx_init, vy_init):
        self.name = name
        self.mass = mass
        self.x = x_init
        self.y = y_init
        self.vx = vx_init
        self.vy = vy_init
        self.x_history = [x_init]
        self.y_history = [y_init]  