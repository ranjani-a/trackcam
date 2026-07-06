import cv2
from ultralytics import YOLO
import serial
import time

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
DEAD_ZONE = 20

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width = frame.shape[:2]
    cx = width // 2
    cy = height // 2

    results = model(frame, verbose=False)

    person_found = False

    for result in results:
        for box in result.boxes:
            if int(box.cls) == 0:
                person_found = True
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # Use center for pan, upper third for tilt
                person_cx = (x1 + x2) // 2
                person_cy = y1 + (y2 - y1) // 4

                error_x = person_cx - cx
                error_y = person_cy - cy

                # Only move if error is outside dead zone
                if abs(error_x) > DEAD_ZONE:
                    pan_angle -= error_x * SENSITIVITY
                if abs(error_y) > DEAD_ZONE:
                    tilt_angle -= error_y * SENSITIVITY

                pan_angle = max(0, min(180, pan_angle))
                tilt_angle = max(0, min(180, tilt_angle))

                command = f"{int(pan_angle)},{int(tilt_angle)}\n"
                ser.write(command.encode())

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(frame, (person_cx, person_cy), 5, (0, 0, 255), -1)
                cv2.putText(frame, f"Error X: {error_x}", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"Error Y: {error_y}", (10, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"Pan: {int(pan_angle)} Tilt: {int(tilt_angle)}", (10, 120),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                break

    cv2.line(frame, (cx - 20, cy), (cx + 20, cy), (255, 0, 0), 2)
    cv2.line(frame, (cx, cy - 20), (cx, cy + 20), (255, 0, 0), 2)
    cv2.putText(frame, "AXIOM v1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if not person_found:
        cv2.putText(frame, "NO TARGET", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("AXIOM Vision", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
ser.close()
cv2.destroyAllWindows()