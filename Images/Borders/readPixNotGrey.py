import cv2
import os

folder = "water"
files = os.listdir(path=f"./{folder}")
dictOfPixels = dict()

for file in files:
    image = cv2.imread(rf"{folder}\{file}")

    for strings in image:
        for el in strings:
            buf = tuple(el)
            if buf in dictOfPixels:
                dictOfPixels[buf] += 1
            else:
                dictOfPixels[buf] = 1

print(max(dictOfPixels.keys(), key=lambda x: x[2]))

#105-138
#109-126
#108-137