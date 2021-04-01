import cv2 as cv
import numpy as np

# load cascade
stop_cascade = cv.CascadeClassifier()

if not stop_cascade.load(cv.samples.findFile("Stopsign_HAAR_19Stages.xml")):
	print("Error loading stop cascade")
	exit(0)

def detect_and_draw(frame):
	gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	gray_equalized = cv.equalizeHist(gray)
	
	stop_signs = stop_cascade.detectMultiScale(gray_equalized)

	for (x, y, w, h) in stop_signs:
		size = w * h
		frame = cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0))
		frame = cv.putText(frame, "size: %i" % size, (x, y), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))

	cv.imshow("Classifier", frame)

# setup camera
camera = cv.VideoCapture(0)

if not camera.isOpened:
	print("Failed to open video capture")
	exit(0)

# detection loop
while True:
	ret, frame = camera.read()

	if frame is None:
		print("No frame captured")
		break

	detect_and_draw(frame)

	if cv.waitKey(50) == 27:
		cv.destroyAllWindows()
		break

exit(0)
