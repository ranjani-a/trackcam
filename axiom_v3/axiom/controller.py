from axiom.config import config


class Controller:

    def __init__(self):

        # Current servo positions
        self.pan = config.get("servo", "pan_start")
        self.tilt = config.get("servo", "tilt_start")

        # Servo limits
        self.pan_min = config.get("servo", "pan_min")
        self.pan_max = config.get("servo", "pan_max")

        self.tilt_min = config.get("servo", "tilt_min")
        self.tilt_max = config.get("servo", "tilt_max")

        # Direction multipliers
        self.pan_dir = config.get("servo", "pan_direction")
        self.tilt_dir = config.get("servo", "tilt_direction")

        # Tracking parameters
        self.dead_zone = config.get("tracking", "dead_zone")

        # Maximum movement each update
        self.max_step = config.get("servo", "max_step")

        # Simple proportional gain (temporary until PID)
        self.gain = 0.02

    def update(self, target, frame_width, frame_height):

        if target is None:
            return self.pan, self.tilt

        center_x = frame_width // 2
        center_y = frame_height // 2

        error_x = target.smooth_x - center_x
        error_y = target.smooth_y - center_y

        # PAN
        if abs(error_x) > self.dead_zone:

            step = error_x * self.gain

            step = max(-self.max_step,
                       min(self.max_step, step))

            self.pan += self.pan_dir * step

        # TILT
        if abs(error_y) > self.dead_zone:

            step = error_y * self.gain

            step = max(-self.max_step,
                       min(self.max_step, step))

            self.tilt += self.tilt_dir * step

        # Clamp servo limits
        self.pan = max(self.pan_min,
                       min(self.pan_max, self.pan))

        self.tilt = max(self.tilt_min,
                        min(self.tilt_max, self.tilt))

        return self.pan, self.tilt