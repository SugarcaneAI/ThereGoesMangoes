import cv2

from util.draw_crosshair import crosshair_norm

cam = cv2.VideoCapture(0)
_, image = cam.read()
print(image.shape)

while True:
 0.1, 0.1, 0.05) 
    cv2.imshow('Imagetest',image)
    k = cv2.waitKey(1)
    if k != -1:
        break
cv2.imwrite('/home/pi/testimage.jpg', image)
cam.release()
cv2.destroyAllWindows()
