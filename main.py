import cv2
import os
listOfRanges = [[16, 36], [79, 97], [97, 122]]
path = r"Images\Screenshoots\fog"
files = os.listdir(path=fr".\{path}")

for file in files:
    image = cv2.imread(rf"{path}\{file}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    lower = 97
    upper = 122
    mask = cv2.inRange(gray, lower, upper)

    result = cv2.bitwise_and(image, image, mask=mask)

    cv2.imshow("Result", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()