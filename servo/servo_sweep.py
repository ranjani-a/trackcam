import serial
import time

ser = serial.Serial('COM13', 115200, timeout=1)
time.sleep(2)

print("Starting sweep...")

while True:
    # Sweep from 0 to 180
    for angle in range(0, 181, 5):
        ser.write(f"{angle},{angle}\n".encode())
        time.sleep(0.05)
    
    # Sweep from 180 back to 0
    for angle in range(180, -1, -5):
        ser.write(f"{angle},{angle}\n".encode())
        time.sleep(0.05)