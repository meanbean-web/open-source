import cv2

## we'll be using this file to communicate graphics to the projector

projImg = cv2.imread('circleGrid.png')

keyb = input("Hit 'q'")
if keyb == 'q':
    cv2.namedWindow('image', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("image", projImg)
    cv2.waitKey()