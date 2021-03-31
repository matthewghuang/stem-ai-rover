import cv2 as cv
import numpy as np

stop_cascade = cv.CascadeClassifier()

if not stop_cascade.load(cv.samples.findFile("Stopsign_HAAR_19Stages.xml")):
	print("Error loading stop cascade")
	exit(0)

def detect_and_draw(frame):
	gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	gray_equalized = cv.equalizeHist(gray)
	b, g, r = cv.split(frame)
	r_equalized = cv.equalizeHist(r)
	r_equalized_inverted = cv.bitwise_not(r_equalized)

	cv.imshow("r", r)
	cv.imshow("r_equalized", r_equalized)
	cv.imshow("r_equalized_inverted", r_equalized_inverted)
	cv.imshow("g", gray)
	cv.imshow("g_equalized", gray_equalized)
	
	stop_signs = stop_cascade.detectMultiScale(r_equalized_inverted)

	for (x, y, w, h) in stop_signs:
		size = w * h
		frame = cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0))
		frame = cv.putText(frame, "size: %i" % size, (x, y), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))

	cv.imshow("Classifier", frame)

	# frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	# frame_gray = cv.equalizeHist(frame_gray)

	# stop_signs = stop_cascade.detectMultiScale(frame_gray)

	# for (x, y, w, h) in stop_signs:
	# 	size = w * h
	# 	frame = cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0))
	# 	frame = cv.putText(frame, "size: %i" % size, (x, y), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))

	# cv.imshow("Classifier", frame)

camera = cv.VideoCapture(0)

if not camera.isOpened:
	print("Failed to open video capture")
	exit(0)

while True:
	ret, frame = camera.read()

	if frame is None:
		print("No frame captured")
		break

	detect_and_draw(frame)
	# cv.imshow("test", frame)

	if cv.waitKey(50) == 27:
		cv.destroyAllWindows()
		break
