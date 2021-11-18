# Apollo LM-like autothrottle autopilot
from math_utils import *

def make_decisions(vessel, terrain, custom_params):

    descent_rate_set = custom_params[0]

    if vessel.get_vel()[1] > descent_rate_set:
        if vessel.get_vel()[1] > descent_rate_set + 10:
            thrust_command = 0
        else:
            thrust_command = (vessel.get_mass() * lunar_gravity * 10 * (1/vessel.get_orient()[1][1])) * (1 - (vessel.get_vel()[1] - descent_rate_set)/10)
    else:
        thrust_command = (vessel.get_mass() * lunar_gravity * 10 * (1/vessel.get_orient()[1][1]) +
                          ((1 - (descent_rate_set - vessel.get_vel()[1])/10) * (vessel.get_max_thrust()/20)))

    thrust_update_command = thrust_command - vessel.get_thrust()

    return (None, thrust_update_command, None)
