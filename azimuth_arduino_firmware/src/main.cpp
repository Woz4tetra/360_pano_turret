#include <Arduino.h>
#include <Servo.h>
#include <SerialManager.h>
//#include "NeopixelPattern.h"

Servo azimuth_servo;
SerialManager manager;

int pos = 0;
#define SERVO_PIN 9

void setup()
{
    // manager.begin();  /// this doesn't work for some reason...
    Serial.begin(115200);

    delay(250);
    manager.writeHello();

    manager.writeReady();
}

void set_azimuth(int new_pos)
{
    pos = new_pos;
    azimuth_servo.write(pos);
}

void loop()
{
    if (manager.available()) {
        int status = manager.readSerial();
        String command = manager.getCommand();

        if (status == 2)  // start event
        {
            azimuth_servo.attach(SERVO_PIN);
        }
        else if (status == 1)  // stop event
        {
            azimuth_servo.detach()
        }
        else if (status == 0)  // user command
        {
            switch(command.charAt(0)) {
                case 'a': set_azimuth(command.substring(1).toInt()); break;
            }
        }
    }

//    if (!manager.isPaused()) {
//
//    }
}