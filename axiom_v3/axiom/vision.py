import cv2
from ultralytics import YOLO

from axiom.config import config
from axiom.target import Target


class Vision:

    def __init__(self):

        # Load YOLO model
        self.model = YOLO("models/yolov8n.pt")

        # Open camera
        self.cap = cv2.VideoCapture(
            config.get("camera", "index")
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            config.get("camera", "width")
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            config.get("camera", "height")
        )

    def read(self):
        """
        Capture one frame from the camera.
        Returns:
            success (bool)
            frame (numpy array)
        """
        success, frame = self.cap.read()
        return success, frame

    def detect(self, frame):
        """
        Detect objects using YOLO and convert them
        into AXIOM Target objects.
        """

        results = self.model(frame, verbose=False)

        targets = []

        for result in results:

            for box in result.boxes:

                cls = int(box.cls)
                conf = float(box.conf)

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                area = (x2 - x1) * (y2 - y1)

                targets.append(
                    Target(
                        x1=x1,
                        y1=y1,
                        x2=x2,
                        y2=y2,
                        center_x=cx,
                        center_y=cy,
                        confidence=conf,
                        class_id=cls,
                        area=area
                    )
                )

        return targets

    def release(self):
        """
        Release the webcam.
        """
        self.cap.release()
        