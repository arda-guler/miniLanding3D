# hover autopilot
from math_utils import *

def make_decisions(vessel, terrain):

    thrust_command = vessel.get_mass() * lunar_gravity * 10 * (1/vessel.get_orient()[1][1])
    thrust_update_command = thrust_command - vessel.get_thrust()

    return (None, thrust_update_command, None)
