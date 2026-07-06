import cv2
from ultralytics import YOLO

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

model = YOLO('yolov8n.pt')

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't read frame")
        break

    height, width = frame.shape[:2]
    cx = width // 2
    cy = height // 2

    results = model(frame, verbose=False)

    for result in results:
        for box in result.boxes:
            if int(box.cls) == 0:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                person_cx = (x1 + x2) // 2
                person_cy = (y1 + y2) // 2

                error_x = person_cx - cx
                error_y = person_cy - cy

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(frame, (person_cx, person_cy), 5, (0, 0, 255), -1)
                
                cv2.putText(frame, f"Error X: {error_x}", (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"Error Y: {error_y}", (10, 90), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.line(frame, (cx - 20, cy), (cx + 20, cy), (255, 0, 0), 2)
    cv2.line(frame, (cx, cy - 20), (cx, cy + 20), (255, 0, 0), 2)
    cv2.putText(frame, "AXIOM", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("AXIOM Vision", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()