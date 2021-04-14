import cv2 as cv

class PedestrianClassifier():
    def __init__(self):
        self.hog = cv.HOGDescriptor()
        self.hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())
        self.cap = cv.VideoCapture(0)
        self.frame = None
        self.ready = False

    def on_loop(self):
        ret, self.frame = self.cap.read()

        if not ret:
            print("failed to capture frame") 
        else:
            self.ready = True

    def detect(self):
        if self.ready:
            tmp_frame = cv.resize(self.frame, (640, 480))
            regions, _ = self.hog.detectMultiScale(tmp_frame)

            return len(regions)
        else:
            return 0

