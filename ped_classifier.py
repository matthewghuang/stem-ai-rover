import cv2 as cv

class PedestrianClassifier():
    def __init__(self):
        self.hog = cv.HOGDescriptor()
        self.hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())
        self.cap = cv.VideoCapture()
        self.frame = None

    def on_loop(self):
        ret, self.frame = self.cap.read()

    def detect(self):
        tmp_frame = cv.resize(self.frame, (640, 480))
        regions, _ = hog.detectMultiScale(tmp_frame)

        return len(regions)

