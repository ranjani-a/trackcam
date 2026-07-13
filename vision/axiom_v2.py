import cv2
from ultralytics import YOLO
import serial
import time
from collections import deque

ser = serial.Serial('COM13', 115200, timeout=1)
time.sleep(2)
print("Connected to ESP32")

model = YOLO('yolov8n.pt')

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

pan_angle = 90
tilt_angle = 90

SENSITIVITY = 0.02
DEAD_ZONE = 25
CONFIDENCE_THRESHOLD = 0.5
COMMAND_INTERVAL = 0.05

# Smoothing buffer — average last 5 detections
cx_buffer = deque(maxlen=5)
cy_buffer = deque(maxlen=5)

prev_time = time.time()
last_command_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width = frame.shape[:2]
    cx = width // 2
    cy = height // 2

    results = model(frame, verbose=False)

    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    best_box = None
    best_area = 0

    for result in results:
        for box in result.boxes:
            if int(box.cls) == 0 and float(box.conf) > CONFIDENCE_THRESHOLD:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                area = (x2 - x1) * (y2 - y1)
                if area > best_area:
                    best_area = area
                    best_box = (x1, y1, x2, y2)

    if best_box:
        x1, y1, x2, y2 = best_box

        # Raw detection center
        raw_cx = (x1 + x2) // 2
        raw_cy = y1 + (y2 - y1) // 4

        # Add to smoothing buffer
        cx_buffer.append(raw_cx)
        cy_buffer.append(raw_cy)

        # Use smoothed average position
        smooth_cx = int(sum(cx_buffer) / len(cx_buffer))
        smooth_cy = int(sum(cy_buffer) / len(cy_buffer))

        error_x = smooth_cx - cx
        error_y = smooth_cy - cy

        if abs(error_x) > DEAD_ZONE:
            pan_angle -= error_x * SENSITIVITY
        if abs(error_y) > DEAD_ZONE:
            tilt_angle -= error_y * SENSITIVITY

        pan_angle = max(10, min(170, pan_angle))
        tilt_angle = max(10, min(170, tilt_angle))

        if curr_time - last_command_time > COMMAND_INTERVAL:
            command = f"{int(pan_angle)},{int(tilt_angle)}\n"
            ser.write(command.encode())
            last_command_time = curr_time

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.circle(frame, (smooth_cx, smooth_cy), 5, (0, 0, 255), -1)
        cv2.putText(frame, f"Error X: {error_x}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Error Y: {error_y}", (10, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Pan: {int(pan_angle)} Tilt: {int(tilt_angle)}", (10, 120),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    else:
        # Clear buffer when target lost
        cx_buffer.clear()
        cy_buffer.clear()
        cv2.putText(frame, "NO TARGET", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.line(frame, (cx - 20, cy), (cx + 20, cy), (255, 0, 0), 2)
    cv2.line(frame, (cx, cy - 20), (cx, cy + 20), (255, 0, 0), 2)
    cv2.putText(frame, "AXIOM v2.1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"FPS: {int(fps)}", (width - 120, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    cv2.imshow("AXIOM Vision", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
ser.close()
cv2.destroyAllWindows()
