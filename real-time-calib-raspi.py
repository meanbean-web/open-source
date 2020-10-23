from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy


#comments for improvement: separate the main chunks of this code into separate definitions

#1: detect chessboard
#2: load image from user on key input


#DECLARE CAMERA MODULE
camera = PiCamera()
camera.resolution = (848, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(848, 480))
camera.vflip = True

time.sleep(0.2)

#DECLARE CHESSBOARD PROPERTIES

imageSize = None # Determined at runtime
CHESSBOARD_CORNERS_ROWCOUNT = 8
CHESSBOARD_CORNERS_COLCOUNT = 5
objpoints = [] # 3D point in real world space where chess squares are
imgpoints = [] # 2D point in image plane, determined by CV2
objp = numpy.zeros((CHESSBOARD_CORNERS_ROWCOUNT*CHESSBOARD_CORNERS_COLCOUNT,3), numpy.float32)
# The following line fills the tuples just generated with their values (0, 0, 0), (1, 0, 0), ...
objp[:,:2] = numpy.mgrid[0:CHESSBOARD_CORNERS_ROWCOUNT,0:CHESSBOARD_CORNERS_COLCOUNT].T.reshape(-1, 2)


#GET REAL TIME VIDEO STREAM FOR RASPI

counter = 0

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    counter += 1
    img = frame.array
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #DETECT CHESSBOARD

    board, corners = cv2.findChessboardCorners(gray, (CHESSBOARD_CORNERS_ROWCOUNT, CHESSBOARD_CORNERS_COLCOUNT), None)
    if board == True:
        # Add the points in 3D that we just discovered
        objpoints.append(objp)

        # Enhance corner accuracy with cornerSubPix
        corners_acc = cv2.cornerSubPix(
            image=gray,
            corners=corners,
            winSize=(11, 11),
            zeroZone=(-1, -1),
            criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30,
                      0.001))  # Last parameter is about termination critera
        imgpoints.append(corners_acc)

        # If our image size is unknown, set it now
        if not imageSize:
            imageSize = gray.shape[::-1]

        # Draw the corners to a new image to show whoever is performing the calibration
        # that the board was properly detected
        img = cv2.drawChessboardCorners(img, (CHESSBOARD_CORNERS_ROWCOUNT, CHESSBOARD_CORNERS_COLCOUNT), corners_acc,
                                        board)

        # DETECT RED CIRCLES FROM THE PROJECTOR
        # circles_grid_size = (4, 7)
        # ret, circles = cv2.findCirclesGrid(gray, circles_grid_size, flags=cv2.CALIB_CB_SYMMETRIC_GRID )
        # img = cv2.drawChessboardCorners(img, circles_grid_size, circles, ret)
    # preview checkerboard detection frame + vectorial orientation

    cv2.imshow("Frame", img)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        break

    if counter < 40:
        print(counter)

    # CALIBRATE CAMERA
    # if the number of retrieved images is 40, then calibrate the camera > you might want to add the first 40 frames to a folder

    if counter == 40:
        calibration, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(
            objectPoints=objpoints,
            imagePoints=imgpoints,
            imageSize=imageSize,
            cameraMatrix=None,
            distCoeffs=None)

        # Print matrix and distortion coefficient to the console
        print(cameraMatrix)
        print(distCoeffs)

    # # DISPLAY CIRCLE GRID
    # if counter > 40:
    #     while reprojectionError < 0.5:
    #         #declare variables for backprojection
    #         images=
    #         channels=
    #         hist=
    #         ranges=
    #
    #         pattern = cv2.imread('image files/ circleGrid.png')
    #         # show pattern full screen on the extended screen
    #         cv2.calcBackProject()
    #
    #         # returns probability in image B


    #GET CENTER AND VECTOR DIRECTION OF THE CHESSBOARD
        #if you can get the surface of the chessboard overall
        #you can get bounding edges


   # preview checkerboard detection frame + vectorial orientation

    # DETECT RED CIRCLES FROM THE PROJECTOR
    circles_grid_size = (4, 7)
    ret, circles = cv2.findCirclesGrid(img, circles_grid_size, flags=cv2.CALIB_CB_SYMMETRIC_GRID)
    img = cv2.drawChessboardCorners(img, circles_grid_size, circles, ret)

    cv2.imshow("Frame", img)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        break






    #COMPARE ORIGINAL INPUT IMAGE TO THE IMAGE RETRIEVED FROM THE PROJECTOR DETECTION

###PERSPECTIVE CORRECTION ###
    #MATCH PERSPECTIVE TO CHECKERBOARD PERSPECTIVE
         # draw bounding box around detected circles


    #at this point you'll have two separate images, matching the projection perspective as you go.

###OVERLAP CORRECTION ###







