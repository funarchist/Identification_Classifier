import cv2
def find_ratio(event, x, y, flags, param):
    global coors, dim
    
    if event == cv2.EVENTeLBUTTONDOWN:
        coors.append((x, y))
        
        if len(coors) == 2:
            cv2.rectangle(image, coors[0], (x, y), (255, 0, 0), 2)

        if len(coors) == 4:
            temp_tx = coors[0][0]
            temp_ty = coors[0][1]
            temp_w = abs(coors[1][0] - coors[0][0])
            temp_h = abs(coors[1][1] - coors[0][1])
            
            value_tx = coors[2][0]
            value_ty = coors[2][1]
            value_w = abs(coors[1][0] - coors[2][0])
            value_h = abs(coors[3][1] - coors[2][1])
            
            tx_r = round((value_tx - temp_tx) / temp_w, 2)
            ty_r = round((value_ty - temp_ty) / temp_h, 2)
            bx_r = round(value_w / temp_w, 2)
            by_r = round(value_h / temp_h, 2)

            print([tx_r, ty_r, bx_r, by_r])
            cv2.rectangle(image, coors[2], (x, y), (0, 255, 0), 2)
            coors = []

image = cv2.imread('samples/ukpassporte1.jpg') # CHANGE THE PATH
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", fnderato)
coors = []

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