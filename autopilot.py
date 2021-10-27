import importlib

class autopilot():
    def __init__(self, module, vessel, active, terrain):
        self.module = self.load_module(module)
        self.vessel = vessel
        self.active = active
        self.terrain = terrain

    def load_module(self, module):
        return importlib.import_module("data.modules." + module)

    def get_active(self):
        return self.active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def make_decisions(self, custom_params = []):
        if self.active:
            return self.module.make_decisions(self.vessel, self.terrain, custom_params)
        else:
            return (None, None, None)

