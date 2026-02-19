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

def acceleration_to_host(host, planet): #the a from gravity
    x = planet.x
    y = planet.y
    r2 =x*x + y*y #squaring them!

    if r2 == 0:
        return 0.0, 0.0 #no diving by 0
    distance = math.sqrt(r2)
    distance_cubed = r2 * distance

    ax = -(G*host.mass*x)/distance_cubed
    ay = -(G*host.mass*y)/distance_cubed
    return ax, ay

def fayman(host, planet, dt):
    ax, ay = acceleration_to_host(host, planet)
    planet.vx += ax*dt
    planet.vy += ay*dt #update both velocities
    planet.x += planet.vx * dt #update both points
    planet.y += planet.vy * dt
    planet.add_points()

host = Planet("Host", 1.99e30, 0.0, 0.0, 0.0, 0.0)
starting_r = 1.50e11
x0, y0 = starting_r, 0.0 

v_centripital = math.sqrt(G*host.mass/starting_r)
#planet_eccentricity = 0.0167 #that is earths eccentricity but idk how to use it
#last is at 1 to make it a circle
planet = Planet("Planet", 5.97e24, x0, y0, 0.0, .9*v_centripital) #mass of earth


dt = 63500
rows = 12000 #idk what to call this but rows is wrong


fig, ax = plt.subplots()
ax.set_aspect("equal", adjustable="box")
ax.set_title("Planet Orbiting a Fixed Host YAY!!!")
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")

view = 2.0*starting_r 
ax.set_xlim(-view, view)
ax.set_ylim(-view, view)



ax.plot([0], [0], "o", markersize=8, label="Host")

planet_dot, = ax.plot([], [], "o", markersize=5, label="Planet")
trail_line, = ax.plot([], [], "-", linewidth=2, alpha=0.9) #alpha is the opacity

ax.legend(loc="upper right")
trail_length = 500 #u can change this idk

def init():
    planet_dot.set_data([], [])
    trail_line.set_data([], [])
    return planet_dot, trail_line

def update(frame):
    fayman(host, planet, dt)
    planet_dot.set_data([planet.x], [planet.y])
    x_update = planet.x_history
    y_update = planet.y_history
    start = max(0, len(x_update)-trail_length) 
    trail_line.set_data(x_update[start:], y_update[start:])
    t = frame*dt #frame times the delta t
    print("Time:", t) #print time
    if frame == 500:
        trail_line.set_alpha(0.4)
        trail_line.set_color("tab:orange")
    return planet_dot, trail_line

animation = FuncAnimation(fig, update, init_func=init, interval=20, blit=True)
plt.show()