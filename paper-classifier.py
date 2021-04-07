import cv2 as cv
import numpy as np

img = cv.imread("./test-paper-image.jpg", cv.IMREAD_COLOR)

def detect(image):
	gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
	#edges = cv.Canny(gray, cv.getTrackbarPos("Low", "sliders"), cv.getTrackbarPos("High", "sliders"))
	edges = cv.Canny(gray, 36, 300)
	contours, hierarchy = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
	contours_drawn = gray.copy()
	largest_contours = sort(contours, key=cv.contourArea)
	largest_contour = max(contours, key=cv.contourArea, reverse=True)
	x, y, w, h = cv.boundingRect(largest_contour)
	cv.rectangle(contours_drawn, (x, y), (x + w, y + h), (0, 255, 0), 2)
	#cv.drawContours(contours_drawn, contours, -1, (0, 255, 0), 3)
	
	cv.imshow("Gray", gray)
	cv.imshow("Edges", edges)
	cv.imshow("Contours", contours_drawn)
	
def nothing(v):
	pass

# cv.namedWindow("sliders")
# cv.createTrackbar("Low", "sliders", 0, 1000, nothing)
# cv.createTrackbar("High", "sliders", 0, 1000, nothing)

while True:
	detect(img)

	if cv.waitKey(10) == 27:
		cv.destroyAllWindows()
		break