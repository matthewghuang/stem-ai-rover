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
		center = (x + w // 2, y + h // 2)
		frame = cv.ellipse(frame, center, (w // 2, h // 2), 0, 0, 360, (255, 0, 255), 4)
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