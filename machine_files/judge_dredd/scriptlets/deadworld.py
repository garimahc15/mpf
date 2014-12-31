"""Handles the ball locking in the Deadworld globe."""

from mpf.system.scriptlet import Scriptlet


class Deadworld(Scriptlet):

    def on_load(self):
        self.machine.events.add_handler('machineflow_Game_start', self.start)
        self.machine.events.add_handler('machineflow_Game_stop', self.stop)
        self.machine.events.add_handler('ball_ending', self.disable_lock)
        self.machine.events.add_handler('balldevice_deadworld_ball_enter',
                                        self.ball_locked)

    def start(self):
        self.log.debug("Starting Deadworld")
        self.machine.events.add_handler('shot_LeftRamp', self.enable_lock)

    def stop(self):
        self.log.debug("Stopping Deadworld")
        self.machine.events.remove_handler(self.enable_lock)
        self.stop_globe()

    def enable_lock(self):
        self.log.debug("Starting Deadworld motor")
        self.start_globe()
        self.machine.balldevices['deadworld'].num_balls_desired += 1

    def disable_lock(self, **kwargs):
        self.log.debug("Stopping Deadworld motor")
        self.stop_globe()
        self.machine.balldevices['deadworld'].num_balls_desired = \
            self.machine.balldevices['deadworld'].num_balls_contained

    def ball_locked(self, **kwargs):
        self.machine.ball_controller.add_live()

    def start_globe(self, ):
        self.machine.coils.globeMotor.enable()

    def stop_globe(self):
        self.machine.coils.globeMotor.disable()

