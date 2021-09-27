import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import glfw

import pywavefront
import keyboard
import time
from os import system

from lander import *
from graphics import *
from terrain import *

def dampen_rotation(ship, dt):
    if not ship.get_ang_vel() == [0,0,0]:
        ship.update_ang_vel([-sign(ship.get_ang_vel()[0]),
                             -sign(ship.get_ang_vel()[1]),
                             -sign(ship.get_ang_vel()[2])],
                            dt)

def main():
    
    def init():
        # init objects
        ship = lander(pywavefront.Wavefront("data/models/lunar_lander.obj", collect_faces=True),
                      [2000, 500, 0], [-100, -20, 0],
                      [[1,0,0], [0,1,0], [0,0,1]],
                      [0,0,0],
                      5000, 3000,
                      [10, 10, 10],
                      200000, 1000000, 200000,
                      True, 100, -5)

        landing_zone = terrain([0,-5,0], [5000, 20, 5000], 0.01)
        landing_zone.generate()

        # init graphics
        glfw.init()

        window = glfw.create_window(800,600,"miniLanding3D", None, None)
        glfw.set_window_pos(window,200,200)
        glfw.make_context_current(window)
        
        gluPerspective(90, 800/600, 0.005, 50000.0)
        glEnable(GL_CULL_FACE)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        
        # init variables
        delta_t = 0.05
        sim_time = 0

        return ship, landing_zone, window, delta_t, sim_time

    ship, landing_zone, window, delta_t, sim_time = init()

    glRotate(30, 1, 0, 0)
    glTranslate(-ship.get_pos()[0], -ship.get_pos()[1] - 5, -ship.get_pos()[2]-50)

    while True:
        cycle_start = time.perf_counter()
        sim_time += delta_t
        glfw.poll_events()

        rot_damp = False

        # engine ignition
        if keyboard.is_pressed("r"):
            ship.toggle_main_engine()

        # throttle control
        if (keyboard.is_pressed("u") - keyboard.is_pressed("j")):
            ship.update_thrust((keyboard.is_pressed("u") - keyboard.is_pressed("j")) * ship.get_max_thrust() * delta_t)

        # attitude control
        
        # dampen rotation?
        if keyboard.is_pressed("x"):
            dampen_rotation(ship, delta_t)
            rot_damp = True

        # not dampening, manual control
        else:
            attitude_thrust = [0,0,0]
            
            if keyboard.is_pressed("w"):
                attitude_thrust[0] += 1
            if keyboard.is_pressed("s"):
                attitude_thrust[0] -= 1
            if keyboard.is_pressed("a"):
                attitude_thrust[2] += 1
            if keyboard.is_pressed("d"):
                attitude_thrust[2] -= 1
            if keyboard.is_pressed("q"):
                attitude_thrust[1] += 1
            if keyboard.is_pressed("e"):
                attitude_thrust[1] -= 1

            if not attitude_thrust == [0,0,0]:
                ship.update_ang_vel(attitude_thrust, delta_t)

        ship.update_physics(delta_t)

        # have the camera follow the ship
        glTranslate(-ship.get_vel()[0] * delta_t, -ship.get_vel()[1] * delta_t, -ship.get_vel()[2] * delta_t)

        # touched down?
        if ship.get_landing_tag_pos()[1] <= landing_zone.get_height_at_pos([ship.get_pos()[0], ship.get_pos()[2]]):
            print("Touchdown!")
            time.sleep(5)
            break

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        drawOrigin()
        drawTerrain(landing_zone)
        drawVessel(ship)
        
        glfw.swap_buffers(window)

        # console output
        try:
            system("cls")
        except:
            system("clear")

        print("T: ", sim_time)
        print("\nAltitude:", ship.get_landing_tag_pos()[1] - landing_zone.get_height_at_pos([ship.get_pos()[0], ship.get_pos()[2]]))
        print("Velocity:", vector_mag(ship.get_vel()))

        print("\nMain Engine:", ship.get_main_engine_str())
        print("Throttle:", ship.get_percent_thrust())
        print("Propellant:", ship.get_prop_mass())

        if rot_damp:
            print("\nKILL ROT")

        cycle_dt = time.perf_counter() - cycle_start
        if cycle_dt < delta_t:
            time.sleep(delta_t - cycle_dt)

main()
