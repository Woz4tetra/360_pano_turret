import os
import time

from ticcmdpy import TicT500
# from joystick import Joystick
from azimuth_servo import AzimuthServo

# os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.environ['SDL_VIDEODRIVER'] = 'dummy'

import pygame
pygame.init()
pygame.display.set_mode((1,1))
pygame.joystick.init()


class PanoTurret:
    def __init__(self):
        self.servo = AzimuthServo("/dev/ttyACM0", baudrate=115200)
        self.stepper = TicT500()

        self.clock = pygame.time.Clock()
        self.should_run = True

    def begin(self):
        print("initializing servo...")
        self.servo.begin()
        print("done!")

        print("initializing stepper...")
        self.stepper.arm()
        print("done!")

    def end(self):
        self.servo.end()
        self.stepper.disarm()

    def init_joysticks(self):
        joystick_count = pygame.joystick.get_count()

        print("Number of joysticks:", joystick_count)
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        name = joystick.get_name()
        print("joystick name:", name)

        axes = joystick.get_numaxes()
        print("\tnum axes:", axes)

        buttons = joystick.get_numbuttons()
        print("\tnum buttons:",  buttons)

        hats = joystick.get_numhats()
        print("\tnum hats:", hats)


    def run(self):
        self.begin()
        self.init_joysticks()

        max_speed = self.stepper.status()["Max speed"]

        try:
            while self.should_run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.should_run = False

                    # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN
                    # JOYBUTTONUP JOYHATMOTION
                    # if event.type == pygame.JOYBUTTONDOWN:
                    #     print("Joystick button pressed.")
                    # if event.type == pygame.JOYBUTTONUP:
                    #     print("Joystick button released.")
                    if event.type == pygame.JOYAXISMOTION:
                        # axis 0: left X, + right
                        # axis 1: left Y, + down
                        # axis 2: left trigger, rest: -1.0, engaged: 1.0
                        # axis 3: right X, + right
                        # axis 4: right Y, + down
                        # axis 5: right trigger, rest: -1.0, engaged: 1.0
                        if event.axis == 1:
                            self.servo.set(int(event.value * 90 + 90))
                        elif event.axis == 3:
                            self.stepper.velocity(int(max_speed * event.value))

                    print(event)
                self.clock.tick(60)
        except KeyboardInterrupt:
            print("exiting")

        self.end()


if __name__ == '__main__':
    def main():
        turret = PanoTurret()
        turret.run()

    main()
