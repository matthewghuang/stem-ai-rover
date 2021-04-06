import cv2 as cv
import numpy as np
from mss import mss
from PIL import Image

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
		frame = cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		frame = cv.putText(frame, "size: %i" % size, (x, y), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

	cv.imshow("Classifier", frame)

monitor = {
	"left": 0,
	"top": 0,
	"width": 1280,
	"height": 720
}

# detection loop
while True:
	with mss() as sct:
		shot = sct.grab(monitor)
		img = Image.frombytes("RGBA", (shot.width, shot.height), shot.bgra)
		img_array = np.array(img)

		detect_and_draw(img_array)
	
	if cv.waitKey(50) == 27:
		cv.destroyAllWindows()
		break

exit(0)
