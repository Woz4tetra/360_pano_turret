import time
import gobject
from ticcmdpy import TicT500
from joystick import Joystick
from azimuth_servo import AzimuthServo


class PanoTurret:
    def __init__(self):
        self.servo = AzimuthServo("")
        self.stepper = TicT500()

        self.should_run = True

    def begin(self):
        self.servo.begin()
        self.stepper.arm()

    def end(self):
        self.servo.end()
        self.stepper.disarm()

    def axis_handler(self, signal, number, value, init):
        print('axis; ', signal, number, value, init)
        # if number == "0":
        #     self.servo.set(value)
        # if number == "1":
        #     self.stepper.velocity(value)

    def button_handler(self, signal, number, value, init):
        print('button; ', signal, number, value, init)

    def run(self):
        j = Joystick(0)
        j.connect('axis', self.axis_handler)
        j.connect('button', self.button_handler)
        loop = gobject.MainLoop()
        context = loop.get_context()

        self.begin()

        while self.should_run:
            # self.servo.update()
            if context.pending():
                context.iteration(True)
            else:
                time.sleep(0.01)

        self.end()


if __name__ == '__main__':
    def main():
        turret = PanoTurret()
        turret.run()
