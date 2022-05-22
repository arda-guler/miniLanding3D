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
from sound import *
from camera import *
from gpws import *

def dampen_rotation(ship, dt):
    if not ship.get_ang_vel() == [0,0,0]:
        ship.update_ang_vel([-sign(ship.get_ang_vel()[0]),
                             -sign(ship.get_ang_vel()[1]),
                             -sign(ship.get_ang_vel()[2])],
                            dt)

def main():
    
    def init():
        print("Initializing lander...")
        # init objects
        ship = lander(pywavefront.Wavefront("data/models/lunar_lander.obj", collect_faces=True),
                      [5000, 1000, 0], [-175, -12.5, 0],
                      [[1,0,0], [0,1,0], [0,0,1]],
                      [0,0,0],
                      5000, 4000,
                      [10, 10, 10],
                      10000, 25000, 4500,
                      True, 35, -5)

        landing_zone = terrain([0,0,0], [20000, 250, 4000], 0.0125)
        landing_zone.generate()

        wide_field = terrain([0,-15,0], [100000, 1, 100000], 0.00005)
        wide_field.generate()

        print("Initializing autopilot...")
        autothrottle = autopilot("AP_autothrottle", ship, False, landing_zone)
        at_descent_rate = -5

        main_cam = camera([0,0,0],
                          [[1,0,0],
                           [0,1,0],
                           [0,0,1]])

        print("Initializing graphics...")
        # init graphics
        glfw.init()

        window = glfw.create_window(800,600,"miniLanding3D", None, None)
        glfw.set_window_pos(window,200,200)
        glfw.make_context_current(window)
        
        gluPerspective(70, 800/600, 0.05, 25000.0)
        glEnable(GL_CULL_FACE)
        glPolygonMode(GL_FRONT, GL_FILL)
        
        # init variables
        delta_t = 0.05
        sim_time = 0

        print("Initializing sound...")
        # init sound
        init_sound()

        return ship, landing_zone, wide_field, autothrottle, at_descent_rate, window, main_cam, delta_t, sim_time

    ship, landing_zone, wide_field, autothrottle, at_descent_rate, window, main_cam, delta_t, sim_time = init()

    main_cam.set_pos([-ship.get_pos()[0], -ship.get_pos()[1] - 5, -ship.get_pos()[2]-50])
    main_cam.rotate([-30, 0, 0])
    #glRotate(30, 1, 0, 0)
    #glTranslate(-ship.get_pos()[0], -ship.get_pos()[1] - 5, -ship.get_pos()[2]-50)

    cycle_num = 0
    while not glfw.window_should_close(window):
        cycle_start = time.perf_counter()
        sim_time += delta_t
        cycle_num += 1
        glfw.poll_events()

        rot_damp = False
        autopilot_active = False

        if keyboard.is_pressed("t"):
            autothrottle.activate()
            play_sfx("AP_on", 0, 2)
        elif keyboard.is_pressed("g"):
            autothrottle.deactivate()
            play_sfx("AP_off", 0, 2)
            
        if keyboard.is_pressed("y"):
            at_descent_rate += 0.5
        elif keyboard.is_pressed("h"):
            at_descent_rate -= 0.5

        # engine ignition
        if ((keyboard.is_pressed("r") and not ship.get_main_engine()) or
            keyboard.is_pressed("f") and ship.get_main_engine()):
            ship.toggle_main_engine()

        # throttle control
        if (keyboard.is_pressed("u") - keyboard.is_pressed("j")):
            ship.update_thrust((keyboard.is_pressed("u") - keyboard.is_pressed("j")) * ship.get_max_thrust(), delta_t)

        if cycle_num % 2 == 0 and autothrottle.make_decisions([at_descent_rate])[1]:
            ship.update_thrust(autothrottle.make_decisions([at_descent_rate])[1], delta_t)
            autopilot_active = True

        # attitude control
        
        # dampen rotation?
        if keyboard.is_pressed("x"):
            dampen_rotation(ship, delta_t)
            rot_damp = True

        # not dampening, manual control
        else:
            attitude_thrust = [0,0,0]
            attitude_thrust[0] = keyboard.is_pressed("w") - keyboard.is_pressed("s")
            attitude_thrust[1] = keyboard.is_pressed("q") - keyboard.is_pressed("e")
            attitude_thrust[2] = keyboard.is_pressed("a") - keyboard.is_pressed("d")

            if not attitude_thrust == [0,0,0]:
                ship.update_ang_vel(attitude_thrust, delta_t)
                play_sfx("rcs", 0, 1)

        ship.update_physics(delta_t)

        # have the camera follow the ship
        main_cam.move_absolute([-ship.get_vel()[0] * delta_t, -ship.get_vel()[1] * delta_t, -ship.get_vel()[2] * delta_t])
        #glTranslate(-ship.get_vel()[0] * delta_t, -ship.get_vel()[1] * delta_t, -ship.get_vel()[2] * delta_t)

        # touched down?
        if ship.get_landing_tag_pos()[1] - 50 <= landing_zone.estimate_height_at_pos([ship.get_pos()[0], ship.get_pos()[2]]):
            if ship.get_landing_tag_pos()[1] <= landing_zone.get_height_at_pos([ship.get_pos()[0], ship.get_pos()[2]]):
                if vector_mag(ship.get_vel()) <= 10:
                    print("Touchdown!")
                    play_sfx("land", 0, 3)
                    if ship.get_main_engine():
                        ship.toggle_main_engine()
                        stop_channel(0)
                else:
                    print("Crash!")
                    play_sfx("crash", 0, 3)
                    if ship.get_main_engine():
                        ship.toggle_main_engine()
                        stop_channel(0)
                time.sleep(5)
                break

        if ship.get_main_engine() and not get_channel_busy(0):
            play_sfx("main_engine", -1, 0)

        elif not ship.get_main_engine() and get_channel_busy(0):
            stop_channel(0)

        set_channel_volume(0, ship.get_percent_thrust()/100)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #drawOrigin()
        drawTerrain(wide_field, ship, 50)
        drawTerrain(landing_zone, ship, 2)
        drawVessel(ship)
        drawInterface(main_cam, ship, autopilot_active)

        gpws(ship, landing_zone, delta_t)
        alt_readout(ship, landing_zone)
        
        glfw.swap_buffers(window)

        # console output
        try:
            system("cls")
        except:
            system("clear")

        print("T: %.2f" % sim_time)
        if ship.get_alt_quick(landing_zone) > 50:
            print("\nAltitude: %.1f" % ship.get_alt_quick(landing_zone))
        else:
            print("\nAltitude: %.1f" % ship.get_alt(landing_zone))
        print("Velocity: %.2f" % vector_mag(ship.get_vel()))
        print("Descent Rate: %.2f" % ship.get_vel()[1])
        print("AP Descent Rate Cmd: %.1f" % at_descent_rate)

        print("\nMain Engine:", ship.get_main_engine_str())
        print("Throttle: %.2f" % ship.get_percent_thrust())
        print("Propellant: %.2f" % ship.get_prop_mass())

        if rot_damp:
            print("\nKILL ROT")

        if autopilot_active:
            print("\nATPL ACTV")

        cycle_dt = time.perf_counter() - cycle_start
        if cycle_dt < delta_t:
            time.sleep(delta_t - cycle_dt)

        delta_t = cycle_dt

main()
