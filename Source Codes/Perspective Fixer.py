import cv2
import math
import imutils
import numpy as np
import os
def perspective(event, x, y, flags, param):
    global coors, resized

    if event == cv2.EVENT_LBUTTONDOWN:
        coors.append((x, y))
        cv2.circle(resized, (x, y), 5, (0, 255, 0), -1)
        
        if len(coors) == 4:
            p1 = tuple(map(lambda x: x * ratio, coors[0]))
            p2 = tuple(map(lambda x: x * ratio, coors[1]))
            p3 = tuple(map(lambda x: x * ratio, coors[2]))
            p4 = tuple(map(lambda x: x * ratio, coors[3]))
            w = int(math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2))
            h = int(math.sqrt((p1[0] - p3[0])**2 + (p1[1] - p3[1])**2))
            
            pts1 = np.float32(p1, p2, p3, p4)
            pts2 = np.float32([[0,0], [w,0], [0,h], [w,h]])
            M = cv2.getPerspectiveTransform(pts1, pts2)
            dst = cv2.warpPerspective(image, M, (w, h))
            cv2.imwrite(os.path.join(SAVE_PATH, "warped.jpg"), dst)
            
            coors = []
            resized = clone.copy()

INPUT_PATH = "/home/faust/Desktop/transform.jpg"
image = cv2.imread(INPUT_PATH) # CHANGE THE PATH
H, W = image.shape[:2]
resized = imutils.resize(image, width=600)
ratio = W / 600
clone = resized.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", perspective)
coors = []
SAVE_PATH = "/home/faust/"

while True:
    # display the image and wait for a keypress
    cv2.imshow("image", resized)
    key = cv2.waitKey(1) & 0xFF
    # if the 'r' key is pressed, reset everthing
    if key == ord("r"):
        coors = []
        resized = clone.copy()
    # if the 'q' key is pressed, break from the loop
    elif chr(key) in ("q", "Q"):
        break
cv2.destroyAllWindows()
