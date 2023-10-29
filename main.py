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

    contours, _ = cv2.findContours(allRangesImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Перебор контуров
    realContours = list()
    for contour in contours:
        # Вычисление длины и ширины контура
        x, y, w, h = cv2.boundingRect(contour)

        # Проверка длины и ширины контура
        if 250>w>30 and 100>h>30:
            realContours.append([x, x+w, y, y+h])
        #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    i = 0
    le = len(realContours)
    while True:
        j = i + 1
        flag = False
        while j < le:

            if abs(np.subtract(realContours[i][0], realContours[j][1], dtype=np.dtype(float))) < 20 and\
                    abs(np.subtract(realContours[i][2], realContours[j][2], dtype=np.dtype(float))) < 20:

                realContours[i] = [min(realContours[i][0], realContours[j][0]),
                                   max(realContours[i][1], realContours[j][1]),
                                   min(realContours[i][2], realContours[j][2]),
                                   max(realContours[i][3], realContours[j][3])
                                   ]

            elif abs(np.subtract(realContours[i][0], realContours[j][1], dtype=np.dtype(float))) < 20 and\
                    abs(np.subtract(realContours[i][2], realContours[j][2], dtype=np.dtype(float))) < 20:

                realContours[i] = [min(realContours[i][0], realContours[j][0]),
                                   max(realContours[i][1], realContours[j][1]),
                                   min(realContours[i][2], realContours[j][2]),
                                   max(realContours[i][3], realContours[j][3])
                                   ]

            else:
                j += 1
                continue

            flag = True
            realContours.pop(j)
            le -= 1

        else:
            if not flag:
                i += 1

        if i > le - 1:
            break

    for contour in realContours:
        x, x_w, y, y_h = contour
        print(x_w - x, y_h - y)
        if 250 > x_w - x > 100 and 76 > y_h - y > 38:
            cv2.rectangle(image, (x, y), (x_w, y_h), (0, 255, 0), 2)
    print("##########")

    cv2.imshow('Image with boundaries', image)
    cv2.waitKey(0)