import cv2

path = r"Images\Screenshoots\evening"
file = "img_4.png"

image = cv2.imread(rf"{path}\{file}")
mask = cv2.inRange(image, (105, 109, 108), (138, 126, 137))
result = cv2.bitwise_and(image, image, mask=mask)
result[mask > 0] = (255, 255, 255)

cv2.imshow('Image with boundaries', result)
cv2.waitKey(0)

#105-138
#109-126
#108-137