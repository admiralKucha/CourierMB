import cv2
import os
import numpy as np


def filterImg(image: np.ndarray, range: list) -> np.ndarray:
    global black

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mask = cv2.inRange(gray, range[0], range[1])
    result = cv2.bitwise_and(gray, gray, mask=mask)
    result[mask > 0] = 255

    if cv2.countNonZero(result) > (shapeIm[0] * shapeIm[1]) / 10:
        result = black.copy()

    return result


listOfRanges = [[16, 36], [79, 97], [97, 122], [30, 76], [40, 70]]
path = r"Images\Screenshoots\normal"
files = os.listdir(path=fr".\{path}")


for file in files:
    image = cv2.imread(rf"{path}\{file}")
    shapeIm = image.shape[0:2]
    black = np.zeros(shapeIm, dtype=np.uint8)
    allRangesImg = black.copy()

    for range in listOfRanges:
        buf = filterImg(image, range)
        allRangesImg = cv2.bitwise_or(allRangesImg, buf)

    cv2.imshow("Result", allRangesImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()