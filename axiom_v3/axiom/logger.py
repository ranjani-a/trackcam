import csv
import os
from datetime import datetime


class Logger:

    def __init__(self):

        os.makedirs("logs", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.filename = f"logs/tracking_{timestamp}.csv"

        self.file = open(self.filename, "w", newline="")

        self.writer = csv.writer(self.file)

        self.writer.writerow([
            "time",
            "center_x",
            "center_y",
            "smooth_x",
            "smooth_y",
            "confidence"
        ])

    def log(self, target):

        if target is None:
            return

        self.writer.writerow([
            datetime.now().strftime("%H:%M:%S.%f"),
            target.center_x,
            target.center_y,
            round(target.smooth_x, 2),
            round(target.smooth_y, 2),
            round(target.confidence, 3)
        ])

    def close(self):

        self.file.close()