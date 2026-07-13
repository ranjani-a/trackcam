import cv2
import time


class GUI:

    def __init__(self):
        self.start_time = time.time()
        self.prev_time = time.time()

    def draw(self, frame, target):

        h, w = frame.shape[:2]

        # FPS
        current = time.time()
        fps = 1 / (current - self.prev_time)
        self.prev_time = current

        runtime = int(current - self.start_time)

        # ---------- TITLE ----------
        cv2.putText(
            frame,
            "AXIOM v3",
            (15, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        # ---------- FPS ----------
        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (15, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )

        # ---------- Runtime ----------
        cv2.putText(
            frame,
            f"Runtime: {runtime}s",
            (15, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )

        # ---------- Frame Center ----------
        cv2.drawMarker(
            frame,
            (w // 2, h // 2),
            (255, 0, 0),
            cv2.MARKER_CROSS,
            20,
            2,
        )

        if target:

            # Status
            cv2.putText(
                frame,
                "STATUS: TRACKING",
                (15, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )

            cv2.putText(
                frame,
                f"Confidence: {target.confidence:.2f}",
                (15, 145),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
            )

            # Bounding Box
            cv2.rectangle(
                frame,
                (target.x1, target.y1),
                (target.x2, target.y2),
                (0, 255, 0),
                2,
            )

            # Raw Center
            cv2.circle(
                frame,
                (target.center_x, target.center_y),
                5,
                (0, 255, 0),
                -1,
            )

            # Smoothed Center
            cv2.circle(
                frame,
                (int(target.smooth_x), int(target.smooth_y)),
                6,
                (0, 0, 255),
                -1,
            )

        else:

            cv2.putText(
                frame,
                "STATUS: NO TARGET",
                (15, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2,
            )

        return frame
    