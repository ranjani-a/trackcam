from axiom.config import config


class Tracker:

    def __init__(self):

        self.confidence = config.get("tracking", "confidence")
        self.alpha = config.get("tracking", "ema_alpha")

        self.smooth_x = None
        self.smooth_y = None

    def update(self, targets):

        # Keep only people above confidence threshold
        people = []

        for target in targets:

            if target.class_id != 0:
                continue

            if target.confidence < self.confidence:
                continue

            people.append(target)

        if len(people) == 0:
            self.smooth_x = None
            self.smooth_y = None
            return None

        # Choose largest person
        people.sort(key=lambda t: t.area, reverse=True)
        target = people[0]

        # First detection
        if self.smooth_x is None:
            self.smooth_x = target.center_x
            self.smooth_y = target.center_y

        else:
            self.smooth_x = (
                self.alpha * target.center_x
                + (1 - self.alpha) * self.smooth_x
            )

            self.smooth_y = (
                self.alpha * target.center_y
                + (1 - self.alpha) * self.smooth_y
            )

        target.smooth_x = self.smooth_x
        target.smooth_y = self.smooth_y

        return target
    