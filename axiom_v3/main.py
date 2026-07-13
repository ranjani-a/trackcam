import cv2

from axiom.vision import Vision
from axiom.tracker import Tracker
from axiom.logger import Logger
from axiom.utils import GUI


vision = Vision()
tracker = Tracker()
logger = Logger()
gui = GUI()


while True:

    success, frame = vision.read()

    if not success:
        break

    targets = vision.detect(frame)

    target = tracker.update(targets)

    logger.log(target)

    frame = gui.draw(frame, target)

    cv2.imshow("AXIOM v3", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


vision.release()
logger.close()

cv2.destroyAllWindows()

