import time
import serial

PACKET_END = b"\n"

HELLO_MESSAGE = b"hello!" + PACKET_END
READY_MESSAGE = b"ready!" + PACKET_END
READY_ASK_COMMAND = b"r" + PACKET_END
START_COMMAND = b"g" + PACKET_END
STOP_COMMAND = b"s" + PACKET_END
MESSAGE_DELIMITER = b"\t"


class WaitForPacketException(Exception):
    pass


class AzimuthServo:
    def __init__(self, address, **serial_kwargs):
        self.address = address
        self.serial_kwargs = serial_kwargs
        self.serial_ref = None

    def begin(self):
        self.serial_ref = serial.Serial(self.address, **self.serial_kwargs)

        time.sleep(0.25)
        if not self.wait_for_packet(READY_ASK_COMMAND, READY_MESSAGE):
            raise WaitForPacketException
        self.serial_ref.write(START_COMMAND)

    def end(self):
        self.serial_ref.write(STOP_COMMAND)
        self.serial_ref.close()

    def update(self):
        if self.serial_ref.in_waiting() > 0:
            serial_buffer = self.serial_ref.readline()
            if serial_buffer[0] == '-':
                print("message: %s", serial_buffer.substr(1).c_str())
                return

            # parse data here and return it
        else:
            return None

    def wait_for_packet(self, ask_packet, response_packet):
        self.serial_ref.write(ask_packet)
        time.sleep(0.01)

        now = time.time()
        begin = now
        prev_write_time = now

        serial_buffer = ""

        while now - begin < 10.0:
            if self.serial_ref.in_waiting() > 0:
                serial_buffer += self.serial_ref.read(1)
                if serial_buffer[-1] == '\n':
                    if serial_buffer == response_packet:
                        return True

            if now - prev_write_time > 2.0:
                self.serial_ref.write(ask_packet)
            now = time.time()
            time.sleep(0.005)

        return False

    def set(self, angle):
        angle = min(max(angle, 0), 180)  # limit angle to 0...180 degrees
        self.serial_ref.write(b"a" + str(angle).encode() + PACKET_END)
