import cv2
import os
def cut(event, x, y, flags, param):
    global coors
    
    if event == cv2.EVENT_LBUTTONDOWN:
        coors.append((x, y))
        if len(coors) == 2:
            cv2.rectangle(image, coors[0], (x, y), (255, 0, 0), 1)
            image_name = input("Enter the name of the template: ")
            while not image_name.endswith(".jpg"):
                image_name = input("Type .jpg at the end of the name!", '\n')

            t_region = clone[coors[0][1]:y, coors[0][0]:x]
            t_region = cv2.resize(
            t_region, (0, 0), fx=RESIZE_RATIO, fy=RESIZE_RATIO)
            image_save_path = os.path.join(SAVE_PATH, image_name)
            cv2.imwrite(image_save_path, t_region)
            coors = []

image = cv2.imread('samples/ukpassporte1.jpg') # CHANGE THE PATH
clone = image.copy()
H, W = image.shape1[:2]
SAVE_PATH = "cuted_templates"
RESIZE_RATIO = 600/W

cv2.namedWindow("image")
cv2.setMouseCallback("image", cut)

coors = []

if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

while True:
    # display the image and wait for a keypress
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF

    # if the 'r' key is pressed, reset everthing
    if key == ord("r"):
        coors = []
        image = clone.copy()
    # if the 'q' key is pressed, break from the loop
    elif key == ord("q"):
        break
    
cv2.destroyAllWindows()