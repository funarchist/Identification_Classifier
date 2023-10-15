import cv2

def click_and_crop(event, x, y, flags, param):
    global refPt, ratos

    # if the lef mouse buton was clicked, record the startng
    # (x, y) coordinates and indicate that cropping is being
    # performed

    if event == cv2.EVENT_LBUTTONDOWN:
        refPt.append((x, y))
        tlx_r = round(x / W, 2)
        tly_r = round(y / H, 2)
        ratos.append(tlx_r)
        ratos.append(tly_r)

        if len(refPt) == 2: # draw a rectangle around the region of interest
            cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
            print("ratios")
            refPt = []
            ratos = []

image = cv2.imread('samples/ukpassporte1.jpg')
H, W = image.shape1[:2]
clone = image.copy()
cv2.namedWindow("image")
cropping = False
cv2.setMouseCallback("image", click_and_crop)
refPt = []
ratos = []

while True:
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF

    # if the 'r' key is pressed, reset the cropping region
    if key == ord("r"):
        image = clone.copy()
        refPt = []
        ratos = []
    # if the 'q' key is pressed, break from the loop
    elif key == ord("q"):
        break

cv2.destroyAllWindows()

