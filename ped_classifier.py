import cv2 as cv

class PedestrianClassifier():
    def __init__(self):
        self.hog = cv.HogDescriptor()
        self.hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())
        self.cap = cv.VideoCapture()
        self.frame = None

    def __del__(self):
        self.cap.release()

    def on_loop(self):
        ret, self.frame = cap.read()

    def detect(self):
        tmp_frame = cv.resize(self.frame, (640, 480))
        regions, _ = hog.detectMultiScale(tmp_frame)

        return len(regions)

