# %%
import cv2 as cv

# %%
stop_cascade = cv.CascadeClassifier()

if not stop_cascade.load(cv.samples.findFile("Stopsign_HAAR_19Stages.xml")):
	print("Error loading stop cascade")
	exit(0)
# %%
def detect(frame):
	frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	frame_gray = cv.equalizeHist(frame_gray)

	stop_signs = stop_cascade.detectMultiScale(frame_gray)

	for (x, y, w, h) in stop_signs:
		size = w * h
		frame = cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
		frame = cv.putText(frame, "size: %x" % size, (x, y), cv.FONT_HERSHEY_SIMPLEX, (0, 255, 0), 2)
		cv.imshow("Stop Sign Classification", frame)

# %%
camera = cv.VideoCapture(0)

if not camera.isOpened:
	print("Failed to open video capture")
	exit(0)

while True:
	ret, frame = camera.read()

	if frame is None:
		print("No frame captured")
		break

	detect(frame)

	if cv.waitKey(10) == 27:
		break