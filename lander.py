from math_utils import *

class lander():
    def __init__(self, model, pos, vel, orient, ang_vel, dry_mass,
                 prop_mass, torque, thrust, max_thrust, min_thrust,
                 main_engine, mass_flow, landing_offset):

        self.model = model
        self.pos = pos
        self.vel = vel
        self.accel = [0,0,0]
        self.orient = orient
        self.ang_vel = ang_vel
        self.dry_mass = dry_mass
        self.prop_mass = prop_mass
        self.torque = torque
        self.thrust = thrust
        self.max_thrust = max_thrust
        self.min_thrust = min_thrust
        self.main_engine = main_engine
        self.mass_flow = mass_flow
        self.landing_offset = landing_offset

    def get_pos(self):
        return self.pos

    def get_vel(self):
        return self.vel

    def get_accel(self):
        return self.accel

    def get_orient(self):
        return self.orient

    def get_max_thrust(self):
        return self.max_thrust

    def get_percent_thrust(self):
        return (self.thrust / self.max_thrust) * 100

    def get_ang_vel(self):
        return self.ang_vel

    def get_prop_mass(self):
        return self.prop_mass

    def toggle_main_engine(self):
        self.main_engine = not self.main_engine

    def get_main_engine_str(self):
        if self.main_engine:
            return "Running"
        else:
            return "Shut down"

    def update_ang_vel(self, rcs, dt):
        self.ang_vel = [self.ang_vel[0] + int(rcs[0]) * dt * self.torque[0],
                        self.ang_vel[1] + int(rcs[1]) * dt * self.torque[1],
                        self.ang_vel[2] + int(rcs[2]) * dt * self.torque[2]]

    # we need to clamp thrust values between min and max thrust, obviously
    def update_thrust(self, d_thrust):
        self.thrust = min(max(self.thrust + d_thrust, self.min_thrust), self.max_thrust)

    def set_thrust(self, thrust):
        self.thrust = min(max(thrust, self.min_thrust), self.max_thrust)

    def set_percent_thrust(self, thrust_percent):
        self.thrust = min(max(thrust_percent * self.max_thrust, self.min_thrust), self.max_thrust)

    def update_orient(self, dt):
        self.orient = rotate_matrix(self.orient, vector_scale(self.ang_vel, dt))

    # there is only gravity and main engine
    # that apply linear acceleration
    def update_accel(self, dt):
        self.accel = [0, -lunar_gravity, 0]

        if self.main_engine:
            thrust_dt = self.thrust * dt
            thrust_dt_vector = vector_scale(self.orient[1], thrust_dt)
            thrust_dt_accel = vector_scale(thrust_dt_vector, 1/(self.dry_mass + self.prop_mass))
            self.accel = vector_add(self.accel, thrust_dt_accel)

    def update_vel(self, dt):
        accel_dt = vector_scale(self.accel, dt)
        self.vel = vector_add(self.vel, accel_dt)

    def update_pos(self, dt):
        vel_dt = vector_scale(self.vel, dt)
        self.pos = vector_add(self.pos, vel_dt)

    def update_mass(self, dt):
        if self.main_engine:
            self.prop_mass -= (self.thrust/self.max_thrust) * self.mass_flow * dt

    def update_physics(self, dt):
        self.update_accel(dt)
        self.update_vel(dt)
        self.update_pos(dt)
        self.update_orient(dt)
        self.update_mass(dt)
        
    def get_landing_tag_pos(self):
        landing_tag_pos = numpy.matmul(numpy.array([0, self.landing_offset, 0]), self.orient).tolist()
        landing_tag_pos = vector_add(landing_tag_pos, self.pos)

        return landing_tag_pos
