import cv2

cap = cv2.VideoCapture(0)
print("Camera opened:", cap.isOpened())

if not cap.isOpened():
    cap = cv2.VideoCapture(1)
    print("Trying index 1:", cap.isOpened())

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Can't read frame")
        break
    
    height, width = frame.shape[:2]
    cx = width // 2
    cy = height // 2
    
    cv2.line(frame, (cx - 20, cy), (cx + 20, cy), (0, 255, 0), 2)
    cv2.line(frame, (cx, cy - 20), (cx, cy + 20), (0, 255, 0), 2)
    cv2.putText(frame, "AXIOM", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow("AXIOM Vision", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()