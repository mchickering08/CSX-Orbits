""""
┌───────────────────────────────────────────────────────────────────────────┐
│                            Orbit Simulation                               │
├───────────────────────────────────────────────────────────────────────────┤
│ Name: Mary Chickering and Shep Okeefe                                     │
| Course: CSX                                                               |
│ Log: Finished project (1.0)                                               |
| Bugs: N/K                                                                 │
│ Description:  A two-body gravitational simulation written in Python.      |
| The system models a binary star system interacting solely                 |
| under Newtons Law of Universal Gravitation.                               |
└───────────────────────────────────────────────────────────────────────────┘
"""
import sys
import math                                                                                 #For square root and other math functions
import matplotlib.pyplot as plt                                                             #For graphing and animations
from matplotlib.animation import FuncAnimation                                              #Tool to make animations

G = 6.67e-11                                                                                #Gravitational Constant
class Planet:
    '''
    Purpose: Represents a single body in a gravity simulation.

    Attributes:
        name (str): Name of the body 
        mass (float): Mass in kilograms
        x, y (float): Current position in meters
        vx, vy (float): Current velocity in m/s
        x_history, y_history (list[float]): Lists storing past positions for trails
    
        Returns: None
    '''
    def __init__(self, name, mass, x_init, y_init, vx_init, vy_init):
        """
        Purpose: Initialize a celestial body with mass, position, velocity, and position history

        Args:
            self (Planet): the object being created
            name (str): name of the body
            mass (float): mass in kilograms
            x_init (float): initial x position in meters
            y_init (float): initial y position in meters
            vx_init (float): initial x velocity in meters per second
            vy_init (float): initial y velocity in meters per second

        Returns: None
        """
        self.name = name                                                                    #Store the object's name
        self.mass = mass                                                                    #Store mass
        self.x = x_init                                                                     #Current x position
        self.y = y_init                                                                     #Current y position
        self.vx = vx_init                                                                   #Current x velocity
        self.vy = vy_init                                                                   #Current y velocity
        self.x_history = [x_init]                                                           #List storing all past x positions (for the trail)
        self.y_history = [y_init]                                                           #List storing all past y positions

    def add_points(self):
        """
        Purpose: Store current position in history lists for drawing trails

        Args:
            self (Planet): current body object

        Returns: None
        """
        self.y_history.append(self.y)                                                       #Adds current y to history
        self.x_history.append(self.x)                                                       #Adds current x to history

def acceleration_of_both(host, planet): 
    """
    Purpose: Compute gravitational acceleration on both bodies using Newton's Law of Universal Gravitation

    Args:
        host (Planet): first body in the system
        planet (Planet): second body in the system

    Returns:
        tuple:
            planet_acceleration_x
            planet_acceleration_y
            host_acceleration_x
            host_acceleration_y
    """
    dx = planet.x - host.x                                                                  #Horizontal seperation between bodies
    dy = planet.y - host.y                                                                  #Vertical seperation
    r2 = dx*dx + dy*dy                                                                      #Distance squared

    if r2 == 0:
        return 0.0, 0.0, 0.0, 0.0                                                           #No dividing by 0 if overlapping
    
    distance = math.sqrt(r2)                                                                #Actual distance r
    distance_cubed = r2 * distance                                                          #r^3 used in vector gravity formula

    planet_acceleration_x = -(G*host.mass*dx)/distance_cubed                                #Planet x accleration towards host
    planet_acceleration_y = -(G*host.mass*dy)/distance_cubed                                #Planet y acceleration towards host

    host_acceleration_x = +(G*planet.mass*dx)/distance_cubed                                #Host x acceleration towards planet
    host_acceleration_y = +(G*planet.mass*dy)/distance_cubed                                #Host y acceleration towards planet

    return planet_acceleration_x, planet_acceleration_y, host_acceleration_x, host_acceleration_y   #Return all accelerations

def fayman(host, planet, dt):
    """
    Purpose: Advance the simulation forward by one timestep using Euler integration

    Args:
        host (Planet): first body in the system
        planet (Planet): second body in the system
        dt (float): timestep in seconds

    Returns: None
    """
    (planet_acceleration_x, planet_acceleration_y, 
    host_acceleration_x, host_acceleration_y) = acceleration_of_both(host, planet)          #Compute accelerations

    planet.vx += planet_acceleration_x*dt                                                   #Update planet x velocity
    planet.vy += planet_acceleration_y*dt                                                   #Update planet y velocity

    host.vx += host_acceleration_x*dt                                                       #Update host x velocity
    host.vy += host_acceleration_y*dt                                                       #Update host y velocity

    planet.x += planet.vx * dt                                                              #Update planet x position
    planet.y += planet.vy * dt                                                              #Update planet y position

    host.x += host.vx * dt                                                                  #Update host x position
    host.y += host.vy * dt                                                                  #Update host y position

    host.add_points()                                                                       #Store host position in history
    planet.add_points()                                                                     #Store planet position in history

    if use_planet3:
        dx1 = planet3.x - host.x                                                            #Compute separation from star 1
        dy1 = planet3.y - host.y                                                            #Compute separation from star 1
        r1 = math.sqrt(dx1*dx1 + dy1*dy1)                                                   #Compute distance to star 1
        a1x = -G*host.mass*dx1/(r1**3)                                                      #Compute acceleration from star 1
        a1y = -G*host.mass*dy1/(r1**3)                                                      #Compute acceleration from star 1

        dx2 = planet3.x - planet.x                                                          #Compute separation from star 2
        dy2 = planet3.y - planet.y                                                          #Compute separation from star 2
        r2 = math.sqrt(dx2*dx2 + dy2*dy2)                                                   #Compute distance to star 2
        a2x = -G*planet.mass*dx2/(r2**3)                                                    #Compute acceleration from star 2
        a2y = -G*planet.mass*dy2/(r2**3)                                                    #Compute acceleration from star 2

        planet3.vx += (a1x + a2x) * dt                                                      #Update planet3 x velocity
        planet3.vy += (a1y + a2y) * dt                                                      #Update planet3 y velocity

        planet3.x += planet3.vx * dt                                                        #Update planet3 x position
        planet3.y += planet3.vy * dt                                                        #Update planet3 y position

        planet3.add_points()                                                                #Store planet3 history

starting_r = 1.50e11                                                                        #Total seperation bodies

print("Choose simulation:")                                                                 #Prompt user
print("1.) Earth orbiting the Sun")                                                         #Option 1
print("2.) Binary star system")                                                             #Option 2
print("3.) Planet orbiting binary star system")                                             #Option 3
choice = input("Enter 1, 2 or 3: ")                                                         #Read user input

if choice == "1":
    host = Planet("Host", 1.99e30, 0.0, 0.0, 0.0, 0.0)                                      #Create sun

    circular_orbit = math.sqrt(G*host.mass/starting_r)                                      #Compute circular velocity
    planet = Planet("Planet", 5.97e24, starting_r, 0.0, 0.0, circular_orbit)                #Create earth

    host.vx = -(planet.mass/host.mass)*planet.vx                                            #Set zero momentum x
    host.vy = -(planet.mass/host.mass)*planet.vy                                            #Set zero momentum y

    use_second_star = False                                                                 #No second star
    use_planet3 = False                                                                     #No third body

elif choice == "2":
    host = Planet("Star 1", 1.0e30, -7.5e10, 0.0, 0.0, 0.0)                                 #Create first star
    planet = Planet("Star 2", 1.0e30, 7.5e10, 0.0, 0.0, 0.0)                                #Create second star

    v_bin = math.sqrt(G*host.mass/(2*starting_r))                                           #Compute binary velocity
    host.vy = -v_bin                                                                        #Assign opposite velocity
    planet.vy = v_bin                                                                       #Assign opposite velocity

    use_second_star = True                                                                  #Binary active
    use_planet3 = False                                                                     #No third body

elif choice == "3":
    host = Planet("Star 1", 1.0e30, -7.5e10, 0.0, 0.0, 0.0)                                 #Create first star
    planet = Planet("Star 2", 1.0e30, 7.5e10, 0.0, 0.0, 0.0)                                #Create second star
    
    v_bin = math.sqrt(G*host.mass/(2*starting_r))                                           #Compute binary velocity
    host.vy = -v_bin                                                                        #Assign opposite velocity
    planet.vy = v_bin                                                                       #Assign opposite velocity

    planet3_accleraton = math.sqrt(G*(host.mass + planet.mass)/6.0e11)                      #Compute planet3 velocity
    planet3 = Planet("Planet", 5.97e24, 6.0e11, 0.0, 0.0, planet3_accleraton)               #Create third body

    use_second_star = True                                                                  #Binary active
    use_planet3 = True                                                                      #Third body active

else:
    print("Invalid choice. Program is ending.")                                             #Display error
    sys.exit()                                                                              #Stop program


dt = 360000                                                                                 #Set timestep   

fig, ax = plt.subplots()                                                                    #Creatre figure and axes
ax.set_aspect("equal", adjustable="box")                                                    #Prevent distorted orbit
if choice == "1":
    ax.set_title("Planet Orbiting Host")                                                    #Set title
    view = 1.2*starting_r                                                                   #Set view window
elif choice == "2":
    ax.set_title("Binary Star System!")                                                     #Set title
    view = 3*starting_r                                                                     #Set view window
else:
    ax.set_title("Planet Orbiting Binary Star System!!")                                    #Set title
    view = 5*starting_r                                                                     #Set view window

ax.set_xlim(-view, view)                                                                    #Set x limits
ax.set_ylim(-view, view)                                                                    #Set y limits
ax.set_xlabel("x (m)")                                                                      #Label x axis
ax.set_ylabel("y (m)")                                                                      #Label y axis                                                                 


host_dot, = ax.plot([], [], "o", markersize=8, label=host.name)                             #Host marker
planet_dot, = ax.plot([], [], "o", markersize=5, label=planet.name)                         #Planet marker
planet3_dot, = ax.plot([], [], "o", markersize=4, label="Planet")                           #Planet marker for orbitting binary star
planet3_trail, = ax.plot([], [], "-", linewidth=2, alpha=0.8)                               #Planet trail line
trail_line, = ax.plot([], [], "-", linewidth=2, alpha=0.9)                                  #Planet trail line
host_trail_line, = ax.plot([], [], "-", linewidth=2, alpha=0.6)                             #Host trail line

ax.legend(loc="upper right")                                                                #Show legend
trail_length = 12000                                                                        #Maximum number of trail points displayed at once

def init():
    """
    Purpose: Initialize matplotlib animation objects before simulation begins

    Args:
        None

    Returns:
        tuple:
            host_dot
            planet_dot
            trail_line
            host_trail_line
    """
    host_dot.set_data([host.x], [host.y])                                                   #Set initial host position
    planet_dot.set_data([], [])                                                             #Clear planet marker

    trail_line.set_data([], [])                                                             #Clear planet trail
    host_trail_line.set_data([], [])                                                        #Clear host trail (binary star system)
 
    if use_planet3:
        planet3_dot.set_data([planet3.x], [planet3.y])
        planet3_trail.set_data([], [])
    else:
        planet3_dot.set_data([], [])
        planet3_trail.set_data([], [])

    return host_dot, planet_dot, planet3_dot, trail_line, planet3_trail, host_trail_line

def update(frame):
    """
    Purpose: Update physics and redraw animation for each frame

    Args:
        frame (int): current animation frame number

    Returns:
        tuple:
            host_dot
            planet_dot
            trail_line
            host_trail_line
    """
    fayman(host, planet, dt)                                                                #Recalculate for one timestep
    
    host_dot.set_data([host.x], [host.y])                                                   #Update host marker
    planet_dot.set_data([planet.x], [planet.y])                                             #Update planet marker

    trail_line.set_data(planet.x_history, planet.y_history)                                 #Update planet trail  
    host_trail_line.set_data(host.x_history, host.y_history)                                #Update host trail
  
    if use_planet3:
        planet3_dot.set_data([planet3.x], [planet3.y])                                      #Update planet3 marker
        planet3_trail.set_data(planet3.x_history, planet3.y_history)                        #Update planet3 trail
    else:
        planet3_dot.set_data([], [])                                                        #Hide planet3
        planet3_trail.set_data([], [])                                                      #Hide planet3 trail

    t = frame*dt                                                                            #Compute simulated time
    print("Time:", t)                                                                       #Print time
    return host_dot, planet_dot, planet3_dot, trail_line, planet3_trail, host_trail_line

animation = FuncAnimation(fig, update, init_func=init, interval=20, blit=False)
plt.show()                                                                                  #Display animation window


#Computations to answer questions:
x_rel = []                                                                                  #Initialize relative x list
y_rel = []                                                                                  #Initialize relative y list

if use_planet3:
    for i in range(len(planet3.x_history)):                                                 #Loop through history
        x_com = (host.mass*host.x_history[i] + planet.mass*planet.x_history[i])/(host.mass + planet.mass) #Compute barycenter x
        y_com = (host.mass*host.y_history[i] + planet.mass*planet.y_history[i])/(host.mass + planet.mass) #Compute barycenter y

        x_rel.append(planet3.x_history[i] - x_com)                                          #Compute relative x
        y_rel.append(planet3.y_history[i] - y_com)                                          #Compute relative y
else:
    for i in range(len(planet.x_history)):                                                  #Loop through history
        x_rel.append(planet.x_history[i] - host.x_history[i])                               #Compute relative x
        y_rel.append(planet.y_history[i] - host.y_history[i])                               #Compute relative y                             

#Eccentricity calculations
c_distance = []                                                                             #List for seperation distances
for i in range(len(x_rel)):                                                                 #For each timestep
    c_distance.append(math.sqrt(x_rel[i]**2 + y_rel[i]**2))                                 #Compute seperation distance

r_min = min(c_distance)                                                                     #Minimum radius
r_max = max(c_distance)                                                                     #Maximum radius

e = (r_max - r_min)/(r_max + r_min)                                                         #Orbital eccentricity formula
print("eccentricity e =", e) 

#Areal velocity calculations
areal_velocities = []                                                                       #List to store areal velocity values
for i in range(len(x_rel) - 1):                                                             #Compute area swept between points
    area = 0.5*abs(x_rel[i]*y_rel[i+1]-y_rel[i]*x_rel[i+1])                                 #Triangle area formula from vertices
    areal_velocities.append(area/dt)                                                        #Divide by dt to get areal velocity

avg_av = sum(areal_velocities)/len(areal_velocities)                                        #Average areal velocity
min_av = min(areal_velocities)                                                              #Minimum areal velocity
max_av = max(areal_velocities)                                                              #Maximum areal velocity

print("average areal velocity: ", avg_av)                                                   #Print average
print("min areal velocity: ", min_av)                                                       #Print minimum
print("max areal velocity: ", max_av)                                                       #Print maximum