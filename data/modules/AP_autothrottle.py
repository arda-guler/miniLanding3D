# autothrottle autopilot
from math_utils import *
import math

def make_decisions(vessel, terrain):

    thrust_command = None
    thrust_update_command = 0

    if vessel.get_orient()[1][1] > 0:
        # we don't want vehicle moving up, ever
        # if that's the case, set throttle to NOT support
        # the weight of the vessel
        if vessel.get_vel()[1] > 0:
            thrust_command = vessel.get_mass() * lunar_gravity * 5 * (1/vessel.get_orient()[1][1])

        # good, we are not going up
        else:
            if vessel.get_alt_quick(terrain) > 200:
                good_descent_rate = math.log2(vessel.get_alt_quick(terrain)) * 0.5
            else:
                good_descent_rate = max(vessel.get_alt_quick(terrain) * 0.05, 3)

            if vessel.get_alt_quick(terrain) < 200 and vector_mag([vessel.get_vel()[0], 0, vessel.get_vel()[2]]) > 10:
                thrust_command = vessel.get_max_thrust()

            elif -vessel.get_vel()[1] > good_descent_rate and -vessel.get_vel()[1] * 5 + -vessel.get_accel()[1] * 25 > vessel.get_alt_quick(terrain):
                thrust_command = vessel.get_max_thrust()

            elif -vessel.get_vel()[1] > good_descent_rate * 2:
                thrust_command = vessel.get_max_thrust()

            elif -vessel.get_vel()[1] > good_descent_rate:
                thrust_command = vessel.get_mass() * 10 * lunar_gravity * 1.5 * (1/vessel.get_orient()[1][1])

            elif good_descent_rate > -vessel.get_vel()[1] > 0.5 * good_descent_rate:
                thrust_command = vessel.get_mass() * 10 * lunar_gravity * 1 * (1/vessel.get_orient()[1][1])

            elif 0.5 * good_descent_rate > -vessel.get_vel()[1]:
                thrust_command = vessel.get_mass() * 10 * lunar_gravity * 0.8 * (1/vessel.get_orient()[1][1])
                
    else:
        thrust_command = 0

    thrust_update_command = thrust_command - vessel.get_thrust()

    return (None, thrust_update_command, None)
