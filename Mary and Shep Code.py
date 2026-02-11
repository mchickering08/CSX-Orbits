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

import numpy as np
import matplotlib.pyplot as plt


G = 6.67e-11 #Gravity constant 

dt = 30.0 #Each step is 30 sec of sumulated time??

m_host = 5.00e24 #mass 1 
m_planet = 1.00e22 #mass 2

#planet starts 4 mil meters to the right of the star
planet_x = 4.00e6
planet_y = 0.0

#planet starts moving upward so it orbits
planet_vx = 0.0
planet_vy = 9130.991184