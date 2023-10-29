import cv2
import os
import numpy as np


def createRange(x: list) -> list[list]:
    listOfRanges = list()
    for el in x:
        le = len(listOfRanges)
        for i in range(0, le):
            if listOfRanges[i][0] < el < listOfRanges[i][1]:
                break
            elif np.subtract(listOfRanges[i][0], el, dtype=np.dtype(float)) < 2 and el < listOfRanges[i][0]:
                listOfRanges[i][0] = el
                break

            elif np.subtract(el, listOfRanges[i][1], dtype=np.dtype(float)) < 2 and el > listOfRanges[i][0]:
                listOfRanges[i][1] = el
                break
        else:
            listOfRanges.append([el, el])

    i = 0
    le = len(listOfRanges)
    while True:
        j = i + 1
        flag = False
        while j < le:
            if abs(np.subtract(listOfRanges[i][0], listOfRanges[j][1], dtype=np.dtype(float))) < 2:
                if listOfRanges[i][0] > listOfRanges[j][0]:
                    listOfRanges[i][0] = listOfRanges[j][0]
                else:
                    listOfRanges[i][1] = listOfRanges[j][1]

            elif abs(np.subtract(listOfRanges[i][1], listOfRanges[j][0], dtype=np.dtype(float))) < 2:
                if listOfRanges[i][1] < listOfRanges[j][1]:
                    listOfRanges[i][1] = listOfRanges[j][1]
                else:
                    listOfRanges[i][0] = listOfRanges[j][0]

            else:
                j += 1
                continue

            flag = True
            listOfRanges.pop(j)
            le -= 1

        else:
            if not flag:
                i += 1

        if i > le - 1:
            break

    i = 0
    while i < le:
        if np.subtract(listOfRanges[i][1], listOfRanges[i][0], dtype=np.dtype(float)) < 3:
            listOfRanges.pop(i)
            le -= 1
        else:
            i += 1

    return listOfRanges


folders = os.listdir(path=".")

for folder in folders:
    if folder == "readPix.py":
        continue

    files = os.listdir(path=f"./{folder}")
    dictOfPixels = dict()

    for file in files:
        image = cv2.imread(rf"{folder}\{file}")
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        for strings in gray_image:
            for el in strings:
                if el in dictOfPixels:
                    dictOfPixels[el] += 1
                else:
                    dictOfPixels[el] = 1

    ranges = createRange(list(dictOfPixels.keys()))
    print(f"{folder} range is", end=" ")
    print(*ranges)

