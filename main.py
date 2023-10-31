import cv2
import os
import numpy as np


def timeOfDay(image: np.ndarray):
    y, h = 1054, 19
    x, w = 1625, 206
    crop_img = image[y:y + h, x:x + w]
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    for i in range(1, 4):
        img1 = cv2.imread(rf"Images\time\img{i}.png")
        img1 = img1.T[0].T

        if np.array_equal(img1, gray):
            return True

    return False

def filterImg(image: np.ndarray, range: list) -> np.ndarray:
    global black

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mask = cv2.inRange(gray, range[0], range[1])
    result = cv2.bitwise_and(gray, gray, mask=mask)
    result[mask > 0] = 255

    if (shapeIm[0] * shapeIm[1]) / 10 < cv2.countNonZero(result):
        result = black.copy()

    return result


listOfNight = [[16, 36]]
listOfRanges = [[79, 97], [97, 122], [27, 76], [40, 70]]

folderTest = "morning"
path = rf"Images\Screenshoots\{folderTest}"
pathToWrite = rf"Images\results\{folderTest}"

files = os.listdir(path=fr".\{path}")


for file in files:
    image = cv2.imread(rf"{path}\{file}")
    flag = timeOfDay(image)
    shapeIm = image.shape[0:2]
    black = np.zeros(shapeIm, dtype=np.uint8)
    allRangesImg = black.copy()

    if flag:
        for rang in listOfNight:
            buf = filterImg(image, rang)
            allRangesImg = cv2.bitwise_or(allRangesImg, buf)

    else:
        for rang in listOfRanges:
            buf = filterImg(image, rang)
            allRangesImg = cv2.bitwise_or(allRangesImg, buf)


    contours, _ = cv2.findContours(allRangesImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Перебор контуров
    realContours = list()
    for contour in contours:
        # Вычисление длины и ширины контура
        x, y, w, h = cv2.boundingRect(contour)

        # Проверка длины и ширины контура
        if w>30 and h>30:
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
        w = x_w - x
        h = y_h-y
        if h < w and 80 < w < 300 and 30 < h < 100:
            cv2.rectangle(image, (x, y), (x_w, y_h), (0, 255, 0), 2)

    cv2.imshow('Image with boundaries', image)
    cv2.imwrite(rf"{pathToWrite}\{file}", image)

    cv2.waitKey(0)