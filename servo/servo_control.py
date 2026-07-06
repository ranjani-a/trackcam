import serial
import time

# Change COM13 to whatever your ESP32 port is
ser = serial.Serial('COM13', 115200, timeout=1)
time.sleep(2)  # wait for ESP32 to boot

print("Connected to ESP32")
print("Type angles as: pan,tilt (e.g. 90,90)")
print("Type 'q' to quit")

while True:
    user_input = input("Enter angles: ")
    
    if user_input == 'q':
        break
    
    # Send to ESP32
    ser.write((user_input + '\n').encode())
    time.sleep(0.1)
    
    # Read response from ESP32
    if ser.in_waiting:
        response = ser.readline().decode().strip()
        print("ESP32 says:", response)

ser.close()
print("Disconnected")