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
from matplotlib.animation import FuncAnimation

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

    def add_points(self):
        self.y_history.append(self.y)
        self.x_history.append(self.x)

def acceleration_of_both(host, planet): #the a from gravity
    dx = planet.x - host.x
    dy = planet.y - host.y
    r2 = dx*dx + dy*dy
    if r2 == 0:
        return 0.0, 0.0, 0.0, 0.0 #no diving by 0
    distance = math.sqrt(r2)
    distance_cubed = r2 * distance

    planet_acceleration_x = -(G*host.mass*dx)/distance_cubed
    planet_acceleration_y = -(G*host.mass*dy)/distance_cubed

    host_acceleration_x = +(G*planet.mass*dx)/distance_cubed
    host_acceleration_y = +(G*planet.mass*dy)/distance_cubed

    return planet_acceleration_x, planet_acceleration_y, host_acceleration_x, host_acceleration_y

def fayman(host, planet, dt):
    planet_acceleration_x, planet_acceleration_y, host_acceleration_x, host_acceleration_y = acceleration_of_both(host, planet)

    #update velocities
    planet.vx += planet_acceleration_x*dt
    planet.vy += planet_acceleration_y*dt
    host.vx += host_acceleration_x*dt
    host.vy += host_acceleration_y*dt

    #update positions
    planet.x += planet.vx * dt
    planet.y += planet.vy * dt

    host.x += host.vx * dt
    host.y += host.vy * dt

    host.add_points()
    planet.add_points()

host = Planet("Host", 1.99e30, 0.0, 0.0, 0.0, 0.0)
starting_r = 1.50e11
x0, y0 = starting_r, 0.0 

v_centripital = math.sqrt(G*host.mass/starting_r)
#planet_eccentricity = 0.0167 #that is earths eccentricity but idk how to use it
#last is at 1 to make it a circle
planet = Planet("Planet", 5.97e24, x0, y0, 0.0, v_centripital) #mass of earth

#total momentum zero
host.vx = -(planet.mass/host.mass) * planet.vx
host.vy = -(planet.mass/host.mass) * planet.vy

dt = 903500
rows = 12000 #idk what to call this but rows is wrong


fig, ax = plt.subplots()
ax.set_aspect("equal", adjustable="box")
ax.set_title("Planet Orbiting a Fixed Host YAY!!!")
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")

view = 2.0*starting_r 
ax.set_xlim(-view, view)
ax.set_ylim(-view, view)



host_dot, = ax.plot([], [], "o", markersize=8, label="Host")

planet_dot, = ax.plot([], [], "o", markersize=5, label="Planet")
trail_line, = ax.plot([], [], "-", linewidth=2, alpha=0.9) #alpha is the opacity

ax.legend(loc="upper right")
trail_length = 500 #u can change this idk

def init():
    host_dot.set_data([host.x], [host.y])
    planet_dot.set_data([], [])
    trail_line.set_data([], [])
    return host_dot, planet_dot, trail_line

def update(frame):
    fayman(host, planet, dt)
    host_dot.set_data([host.x], [host.y])
    planet_dot.set_data([planet.x], [planet.y])
    start = max(0, len(planet.x_history) - trail_length)
    trail_line.set_data(planet.x_history[start:], planet.y_history[start:])
    t = frame*dt #frame times the delta t
    print("Time:", t) #print time
    return host_dot, planet_dot, trail_line

animation = FuncAnimation(fig, update, init_func=init, interval=20, blit=True)
plt.show()