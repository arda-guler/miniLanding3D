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
from autopilot import *
from camera import *

def dampen_rotation(ship, dt):
    if not ship.get_ang_vel() == [0,0,0]:
        ship.update_ang_vel([-sign(ship.get_ang_vel()[0]),
                             -sign(ship.get_ang_vel()[1]),
                             -sign(ship.get_ang_vel()[2])],
                            dt)

def main():
    
    def init():
        # init objects
        ship = lander(pywavefront.Wavefront("data/models/LM_tessellated.obj", collect_faces=True),
                      [0, 1000, 10000], [0, -12.5, -175],
                      [[1,0,0], [0,1,0], [0,0,1]],
                      [0,0,0],
                      5000, 3000,
                      [10, 10, 10],
                      100000, 550000, 100000,
                      True, 35, -3)

        landing_zone = terrain([0,0,0], [4000, 15, 20000], 0.0075)
        landing_zone.generate()

        main_cam = camera([0,0,0],
                          [[1,0,0],
                           [0,1,0],
                           [0,0,1]])

        autothrottle = autopilot("AP_autothrottle", ship, False, landing_zone)
        autohover = autopilot("AP_hover", ship, False, landing_zone)

        # init graphics
        glfw.init()

        window = glfw.create_window(800,600,"miniLanding3D", None, None)
        glfw.set_window_pos(window,200,200)
        glfw.make_context_current(window)
        
        gluPerspective(70, 800/600, 0.005, 50000.0)
        glEnable(GL_CULL_FACE)
        glPolygonMode(GL_FRONT, GL_FILL)
        
        # init variables
        delta_t = 0.05
        sim_time = 0

        return ship, landing_zone, autothrottle, autohover, window, main_cam, delta_t, sim_time

    ship, landing_zone, autothrottle, autohover, window, main_cam, delta_t, sim_time = init()

    main_cam.set_pos([-ship.get_pos()[0]+0.65, -ship.get_pos()[1]-2, -ship.get_pos()[2]+1.15])
    main_cam.rotate([-45,0,0])

    cycle_num = 0
    while True:
        cycle_start = time.perf_counter()
        sim_time += delta_t
        cycle_num += 1
        glfw.poll_events()

        rot_damp = False
        autopilot_active = False

        if keyboard.is_pressed("t"):
            autohover.deactivate()
            autothrottle.activate() 
        elif keyboard.is_pressed("g"):
            autothrottle.deactivate()

        if keyboard.is_pressed("h"):
            autothrottle.deactivate()
            autohover.activate()
        elif keyboard.is_pressed("n"):
            autohover.deactivate()

        # engine ignition
        if keyboard.is_pressed("r"):
            ship.toggle_main_engine()

        # throttle control
        if (keyboard.is_pressed("u") - keyboard.is_pressed("j")):
            ship.update_thrust((keyboard.is_pressed("u") - keyboard.is_pressed("j")) * ship.get_max_thrust(), delta_t)

        if cycle_num % 3 == 0 and autothrottle.make_decisions()[1]:
            ship.update_thrust(autothrottle.make_decisions()[1], delta_t)
            autopilot_active = True
        elif cycle_num % 3 == 0 and autohover.make_decisions()[1]:
            ship.update_thrust(autohover.make_decisions()[1], delta_t)
            autopilot_active = True

        # attitude control
        
        # dampen rotation?
        if keyboard.is_pressed("x"):
            dampen_rotation(ship, delta_t)
            rot_damp = True

        # not dampening, manual control
        else:
            attitude_thrust = [0,0,0]
            attitude_thrust[0] = keyboard.is_pressed("s") - keyboard.is_pressed("w")
            attitude_thrust[1] = keyboard.is_pressed("q") - keyboard.is_pressed("e")
            attitude_thrust[2] = keyboard.is_pressed("a") - keyboard.is_pressed("d")

            if not attitude_thrust == [0,0,0]:
                ship.update_ang_vel(attitude_thrust, delta_t)

        ship.update_physics(delta_t)

        # have the camera fixed to the ship
        main_cam.move_absolute([-ship.get_vel()[0] * delta_t, -ship.get_vel()[1] * delta_t, -ship.get_vel()[2] * delta_t])

        # rotate with the ship
        main_cam.rotate([ship.get_ang_vel()[0] * delta_t, ship.get_ang_vel()[1] * delta_t, ship.get_ang_vel()[2] * delta_t], ship, True)

        # and rotate by user command
        # main_cam.rotate([keyboard.is_pressed("up") - keyboard.is_pressed("down"), keyboard.is_pressed("left") - keyboard.is_pressed("right"), 0])
        
##        main_cam.set_pos([-ship.get_pos()[0] + (0.65*ship.get_orient()[0][0]) + (-1.9*ship.get_orient()[1][0]) + (0.9*ship.get_orient()[2][0]),
##                          -ship.get_pos()[1] + (0.65*ship.get_orient()[0][1]) + (-1.9*ship.get_orient()[1][1]) + (0.9*ship.get_orient()[2][1]),
##                          -ship.get_pos()[2] + (0.65*ship.get_orient()[0][2]) + (-1.9*ship.get_orient()[1][2]) + (0.9*ship.get_orient()[2][2])])
        
        # touched down?
        if ship.get_landing_tag_pos()[1] <= landing_zone.get_height_at_pos([ship.get_pos()[0], ship.get_pos()[2]]):
            print("Touchdown!")
            time.sleep(5)
            break

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #drawOrigin()
        drawTerrain(landing_zone, ship)
        drawVessel(ship)
        
        glfw.swap_buffers(window)

        # console output
        try:
            system("cls")
        except:
            system("clear")

        print("T: ", sim_time)
        print("\nAltitude:", ship.get_alt(landing_zone))
        print("Velocity:", vector_mag(ship.get_vel()))
        print("Descent Rate: ", ship.get_vel()[1])

        print("\nMain Engine:", ship.get_main_engine_str())
        print("Throttle:", ship.get_percent_thrust())
        print("Propellant:", ship.get_prop_mass())

        if rot_damp:
            print("\nKILL ROT")

        if autopilot_active:
            print("\nATPL ACTV")

        cycle_dt = time.perf_counter() - cycle_start
        if cycle_dt < delta_t:
            time.sleep(delta_t - cycle_dt)

main()
