import cv2

image = cv2.imread(r"evening\img.png")
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

dictOfPixels = dict()
for strings in gray_image:
    for el in strings:
        if el in dictOfPixels:
            dictOfPixels[el] += 1
        else:
            dictOfPixels[el] = 1


print(list(reversed(sorted(dictOfPixels.items(), key=lambda x: x[1]))))