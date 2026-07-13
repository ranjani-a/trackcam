from dataclasses import dataclass


@dataclass
class Target:
    """
    Represents a single detected object in AXIOM.

    Every module after vision.py works with this object
    instead of raw YOLO detections.
    """

    # Bounding box
    x1: int
    y1: int
    x2: int
    y2: int

    # Raw center from YOLO
    center_x: int
    center_y: int

    # Smoothed center (filled in later by the tracker)
    smooth_x: float = 0.0
    smooth_y: float = 0.0

    # Detection confidence
    confidence: float = 0.0

    # YOLO class ID
    class_id: int = 0

    # Bounding box area
    area: int = 0

    # Tracking ID (for future multi-object tracking)
    track_id: int = -1

    # Estimated velocity (for Kalman filter later)
    velocity_x: float = 0.0
    velocity_y: float = 0.0

    # Timestamp of this detection
    timestamp: float = 0.0

    