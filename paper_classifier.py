import cv2 as cv
import numpy as np
from PIL import Image
import pytesseract

img = cv.imread("./test-paper-image-with-text.png", cv.IMREAD_COLOR)
use_sliders = False

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


def closed_arc_length(curve):
    return cv.arcLength(curve, True)


def cnt_area(curve):
    rect = cv.minAreaRect(curve)
    width = rect[1][0]
    height = rect[1][1]
    return width * height


def detect(image):
    blurred = cv.GaussianBlur(image, (0, 0), 2)

    ratio = cv.getTrackbarPos("canny ratio", "s") if use_sliders else 3
    lower = cv.getTrackbarPos("canny lower", "s") if use_sliders else 25
    upper = ratio * lower
    edges = cv.Canny(blurred, lower, upper)
    cv.imshow("edges", edges)

    contours_drawn = blurred.copy()
    contours, hierarchy = cv.findContours(
        edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    cv.drawContours(contours_drawn, contours, -1, (0, 0, 255), 1)

    sorted_contours = sorted(contours, key=closed_arc_length, reverse=True)
    half_len = int(len(sorted_contours) / 2)
    print(half_len)

    found_chars = list()

    rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_image)

    for cnt in sorted_contours[:half_len]:
        x, y, w, h = cv.boundingRect(cnt)

        # cv.rectangle(contours_drawn, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # cv.putText(contours_drawn, "{}".format(int(arc_length)),
        #            (x, y), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cropped_image = pil_image.crop(
            (x, y, x + w, y + h))

        cv.imwrite("{}.png".format(int(closed_arc_length(cnt))),
                   np.array(cropped_image))

    cv.imshow("contours", contours_drawn)

    return found_chars


def nothing(v):
    pass


cv.namedWindow("s", cv.WINDOW_NORMAL)
cv.createTrackbar("canny lower", "s", 0, 2000, nothing)
cv.createTrackbar("canny ratio", "s", 1, 3, nothing)

if __name__ == "__main__":
    while True:
        print(detect(img))

        if cv.waitKey(10) == 27:
            cv.destroyAllWindows()
            break
