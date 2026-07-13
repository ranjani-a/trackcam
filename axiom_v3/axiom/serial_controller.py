import serial
import time

from axiom.config import config


class SerialController:

    def __init__(self):

        self.port = config.get("serial", "port")
        self.baudrate = config.get("serial", "baudrate")

        self.serial = None

        self.last_pan = None
        self.last_tilt = None

    def connect(self):

        self.serial = serial.Serial(
            self.port,
            self.baudrate,
            timeout=1
        )

        time.sleep(2)

        print(f"Connected to ESP32 on {self.port}")

    def send(self, pan, tilt):

        pan = int(pan)
        tilt = int(tilt)

        if pan == self.last_pan and tilt == self.last_tilt:
            return

        command = f"{pan},{tilt}\n"

        print(f"Sending: {command.strip()}")


        self.serial.write(command.encode())
        self.last_pan = pan
        self.last_tilt = tilt

    def close(self):

        if self.serial:

            self.serial.close()

            print("Serial connection closed.")
