import os
import cv2
import numpy as np

listOfFogs = [[79, 97], [97, 122]]
path = r"Images\Screenshoots\fog"
files = os.listdir(path=fr".\{path}")

for file in files:
    image = cv2.imread(rf"{path}\{file}")
    shapeIm = image.shape[0:2]
    print(shapeIm)
    black = np.zeros(shapeIm, dtype=np.uint8)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    lower = listOfFogs[0][0]
    upper = listOfFogs[0][1]
    mask = cv2.inRange(gray, lower, upper)

    result = cv2.bitwise_and(gray, gray, mask=mask)
    result[mask > 0] = 255
    result1 = result

    if cv2.countNonZero(result) > (shapeIm[0] * shapeIm[1]) / 5:
        result1 = black

    cv2.waitKey(0)
    lower = listOfFogs[1][0]
    upper = listOfFogs[1][1]
    mask = cv2.inRange(gray, lower, upper)

    result = cv2.bitwise_and(gray, gray, mask=mask)
    result[mask > 0] = 255
    result2 = result

    if cv2.countNonZero(result) > (shapeIm[0] * shapeIm[1]) / 5:
        result2 = black

    result = cv2.bitwise_or(result1, result2)
    cv2.imshow("Result", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
