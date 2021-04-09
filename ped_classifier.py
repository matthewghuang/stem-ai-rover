# %%
import cv2 as cv
import time

# %%
hog = cv.HOGDescriptor()
hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

# %%
image = cv.imread("pedestrians-2.jpg")

# %%
regions, _ = hog.detectMultiScale(image)

for x, y, w, h in regions:
    cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255))

cv.imshow("Image", image)
cv.waitKey(0)

cv.destroyAllWindows()

# %%
hog = cv.HOGDescriptor()
hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

cap = cv.VideoCapture("./IMG_3440.MOV")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to read video")
        break

    height, width, layers = frame.shape

    frame = cv.resize(frame, (640, 480))

    start = time.time()
    regions, _ = hog.detectMultiScale(frame)
    end = time.time()

    print(end - start)

    for x, y, w, h in regions:
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255))

    cv.imshow("Video", frame)

    if cv.waitKey(10) == 27:
        break

cap.release()
cv.destroyAllWindows()

# %%
haar = cv.CascadeClassifier()
haar.load("./fullbody.xml")

cap = cv.VideoCapture("./IMG_3440.MOV")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to read video")
        break

    frame = cv.resize(frame, (640, 480))

    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # gray_frame = cv.equalizeHist(gray_frame)

    start = time.time()
    regions = haar.detectMultiScale(gray_frame)
    end = time.time()

    print(end - start)

    for x, y, w, h in regions:
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255))

    cv.imshow("Video", frame)
    cv.imshow("Video Gray", gray_frame)

    if cv.waitKey(10) == 27:
        break

cap.release()
cv.destroyAllWindows()
