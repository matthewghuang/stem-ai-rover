import cv2 as cv
import numpy as np
from PIL import Image
import pytesseract

img = cv.imread("./test-paper-image-with-text.png", cv.IMREAD_COLOR)

# def detect(image):
# 	gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
# 	#edges = cv.Canny(gray, cv.getTrackbarPos("Low", "sliders"), cv.getTrackbarPos("High", "sliders"))
# 	edges = cv.Canny(gray, 36, 300)
# 	contours, hierarchy = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
# 	contours_drawn = gray.copy()
# 	largest_contours = sorted(contours, key=cv.contourArea, reverse=True)
# 	for contour in largest_contours[:5]:
# 		x, y, w, h = cv.boundingRect(contour)
# 		cv.rectangle(contours_drawn, (x, y), (x + w, y + h), (0, 255, 0), 2)
# 	# largest_contour = max(contours, key=cv.contourArea, reverse=True)
# 	# x, y, w, h = cv.boundingRect(largest_contour)
# 	# cv.rectangle(contours_drawn, (x, y), (x + w, y + h), (0, 255, 0), 2)
# 	#cv.drawContours(contours_drawn, contours, -1, (0, 255, 0), 3)
	
# 	cv.imshow("Gray", gray)
# 	cv.imshow("Edges", edges)
# 	cv.imshow("Contours", contours_drawn)

def greater_than_thousand(curve):
	return cv.arcLength(curve, True) > 1000

def detect(image):
	hls = cv.cvtColor(image, cv.COLOR_BGR2HLS)

	# lower_h = cv.getTrackbarPos("LH", "s")
	# lower_l = cv.getTrackbarPos("LL", "s")
	# lower_s = cv.getTrackbarPos("LS", "s")
	# upper_h = cv.getTrackbarPos("UH", "s")
	# upper_l = cv.getTrackbarPos("UL", "s")
	# upper_s = cv.getTrackbarPos("US", "s")
	lower_h = 104
	lower_l = 0
	lower_s = 0
	upper_h = 180
	upper_l = 255
	upper_s = 255

	lower_white = np.array([lower_h, lower_l, lower_s])
	upper_white = np.array([upper_h, upper_l, upper_s])

	mask = cv.inRange(hls, lower_white, upper_white)

	res = cv.bitwise_and(image, image, mask=mask)
	gray_res = cv.cvtColor(res, cv.COLOR_BGR2GRAY)

	edges = cv.Canny(gray_res, 420, 1324)
	# edges = cv.Canny(gray_res, cv.getTrackbarPos("LC", "s"), cv.getTrackbarPos("UC", "s"))

	contours_drawn = image.copy()
	contours, hierarchy = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

	filtered_contours = filter(greater_than_thousand, contours)

	for cnt in filtered_contours:
		x, y, w, h = cv.boundingRect(cnt)
		cv.rectangle(contours_drawn, (x, y), (x + w, y + h), (0, 0, 255), 2)
		cv.putText(contours_drawn, "{}".format(int(cv.arcLength(cnt, True))), (x, y), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
		rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
		pil_image = Image.fromarray(rgb_image)
		cropped_image = pil_image.crop((x, y, x + w, y + h))
		print(pytesseract.image_to_string(cropped_image))


	# cv.drawContours(contours_drawn, contours, -1, (0, 255, 0), 2)

	cv.imshow("og", image)
	# cv.imshow("hls", hls)
	# cv.imshow("mask", mask)
	cv.imshow("masked", res)
	cv.imshow("edges", edges)
	cv.imshow("contours", contours_drawn)

	
def nothing(v):
	pass

cv.namedWindow("s", cv.WINDOW_NORMAL)
# cv.createTrackbar("LH", "s", 0, 180, nothing)
# cv.createTrackbar("LL", "s", 0, 255, nothing)
# cv.createTrackbar("LS", "s", 0, 255, nothing)
# cv.createTrackbar("UH", "s", 0, 180, nothing)
# cv.createTrackbar("UL", "s", 0, 255, nothing)
# cv.createTrackbar("US", "s", 0, 255, nothing)
# cv.createTrackbar("LC", "s", 0, 2000, nothing)
# cv.createTrackbar("UC", "s", 0, 2000, nothing)

while True:
	detect(img)

	if cv.waitKey(10) == 27:
		cv.destroyAllWindows()
		break