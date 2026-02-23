"""
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
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

G = 6.67e-11

class Planet:
    '''
    Purpose: Represents a single body in a gravity simulation.
    '''

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


def acceleration_of_both(body1, body2):

    dx = body2.x - body1.x
    dy = body2.y - body1.y
    r2 = dx*dx + dy*dy

    if r2 == 0:
        return 0.0, 0.0, 0.0, 0.0

    distance = math.sqrt(r2)
    distance_cubed = r2 * distance

    a1x = -(G*body2.mass*dx)/distance_cubed
    a1y = -(G*body2.mass*dy)/distance_cubed

    a2x = +(G*body1.mass*dx)/distance_cubed
    a2y = +(G*body1.mass*dy)/distance_cubed

    return a1x, a1y, a2x, a2y


def update_binary_and_planet(star1, star2, planet3, dt):

    # Star-star interaction
    a1x, a1y, a2x, a2y = acceleration_of_both(star1, star2)

    star1.vx += a1x * dt
    star1.vy += a1y * dt
    star2.vx += a2x * dt
    star2.vy += a2y * dt

    star1.x += star1.vx * dt
    star1.y += star1.vy * dt
    star2.x += star2.vx * dt
    star2.y += star2.vy * dt

    # Planet acceleration from both stars

    dx1 = planet3.x - star1.x
    dy1 = planet3.y - star1.y
    r1 = math.sqrt(dx1*dx1 + dy1*dy1)

    a1x = -G*star1.mass*dx1/(r1**3)
    a1y = -G*star1.mass*dy1/(r1**3)

    dx2 = planet3.x - star2.x
    dy2 = planet3.y - star2.y
    r2 = math.sqrt(dx2*dx2 + dy2*dy2)

    a2x = -G*star2.mass*dx2/(r2**3)
    a2y = -G*star2.mass*dy2/(r2**3)

    planet3.vx += (a1x + a2x) * dt
    planet3.vy += (a1y + a2y) * dt

    planet3.x += planet3.vx * dt
    planet3.y += planet3.vy * dt

    star1.add_points()
    star2.add_points()
    planet3.add_points()


starting_r = 1.50e11

star1 = Planet("Star 1", 1.0e30, -7.5e10, 0.0, 0.0, 0.0)
star2 = Planet("Star 2", 1.0e30, 7.5e10, 0.0, 0.0, 0.0)

v_bin = math.sqrt(G*star1.mass/(2*starting_r))
star1.vy = -v_bin
star2.vy = v_bin

planet3_acceleration = math.sqrt(G*(star1.mass + star2.mass)/6.0e11)
planet3 = Planet("Planet", 5.97e24, 6.0e11, 0.0, 0.0, planet3_acceleration)

dt = 3600

fig, ax = plt.subplots()
ax.set_aspect("equal", adjustable="box")
ax.set_title("Planet Orbiting Binary Star System!!")
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")

view = 5*starting_r
ax.set_xlim(-view, view)
ax.set_ylim(-view, view)

star1_dot, = ax.plot([], [], "o", markersize=8, label="Star 1")
star2_dot, = ax.plot([], [], "o", markersize=8, label="Star 2")
planet_dot, = ax.plot([], [], "o", markersize=4, label="Planet")

planet_trail, = ax.plot([], [], "-", linewidth=2, alpha=0.8)

ax.legend(loc="upper right")


def init():
    star1_dot.set_data([], [])
    star2_dot.set_data([], [])
    planet_dot.set_data([], [])
    planet_trail.set_data([], [])
    return star1_dot, star2_dot, planet_dot, planet_trail


def update(frame):

    update_binary_and_planet(star1, star2, planet3, dt)

    star1_dot.set_data([star1.x], [star1.y])
    star2_dot.set_data([star2.x], [star2.y])
    planet_dot.set_data([planet3.x], [planet3.y])
    planet_trail.set_data(planet3.x_history, planet3.y_history)

    return star1_dot, star2_dot, planet_dot, planet_trail


animation = FuncAnimation(fig, update, init_func=init, interval=20, blit=False)
plt.show()