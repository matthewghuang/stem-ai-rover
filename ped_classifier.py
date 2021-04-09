import cv2 as cv
import time
import socketio

sio = socketio.Client()
sio.connect("ws://10.32.239.124:3000")

hog = cv.HOGDescriptor()
hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

cap = cv.VideoCapture("./man.mp4")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to read video")
        break

    height, width, layers = frame.shape

    frame = cv.resize(frame, (640, 480))

    regions, _ = hog.detectMultiScale(frame)

    if len(regions) > 0:
        sio.emit("set_direction", "")

    for x, y, w, h in regions:
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255))

    cv.imshow("Video", frame)

    if cv.waitKey(10) == 27:
        break

cap.release()
cv.destroyAllWindows()
