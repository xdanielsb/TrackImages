"""
    Hello User!!!
    I'm daniel this software track an object in a
    video in real time, using C, bash, dynamic
    libraries, techniques of BigData, Complex
    variables, Mathematics and Machine Vision.

    Commands
    Key         Function
    T           Tracking
    D           Debug Activated
    F           Finish the program
    P           Pause the camera
    W           Save the image
    O           Activate tracking method 1
    U           Activate tracking method 2
    S           Activate tracking method 3
    M           Visualize tracking methods
    F           Follow the track object

"""
#Just a dirty trick
from variables import *
import variables as var
from utilities import *
from useful_functions import *
from subprocess import call
#from launcher import __doc__

import numpy as np
import cv2
from matplotlib import pyplot as plt
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)


NUM_SUBPLOT = 1
#Auxiliar variable to help me to intance once
FIRST = True
BEST_POINTS = []

def nothing(x):
    pass


def choose_matcher():

    if var.ACTIVE_ORB:
        var.orb = cv2.ORB_create()
    if var.ACTIVE_SIFT:
        var.sift = cv2.xfeatures2d.SIFT_create()
    if var.ACTIVE_SURF:
        var.surf = cv2.xfeatures2d.SURF_create(400)


def debug(blur):
    global  DEBUG, THRESH_VALUE, FIRST
    if(var.DEBUG):
        cv2.imshow('blur', blur)
        cv2.moveWindow("blur", 800, 0)
        if(FIRST):
            cv2.createTrackbar('THRESH_VALUE','blur',var.THRESH_VALUE,255,nothing)
            FIRST = False
        var.THRESH_VALUE = cv2.getTrackbarPos('THRESH_VALUE','blur')
    else:
        cv2.destroyWindow('blur')
        FIRST = True


def tracking(blur):
    global TRACKING, ACTUAL_IMAGE
    if(var.TRACKING):
        contours = find_contours(blur)
        #DRAW ALL COUNTOURS IN THE IMAGE
        #print(contours)
        var.ACTUAL_IMAGE = draw_contours(var.ACTUAL_IMAGE, contours)


def find_matches(bf, des1, des2, kp1 , kp2, color):
    global BEST_POINTS

    matches = bf.match(des1,des2)
    matches = sorted(matches, key = lambda x:x.distance)
    #print("Number of matches: {}".format(len(matches)))
    best_matches = matches
    if len(matches) < 5:
        best_matches = matches
    else:
        pass
        #best_matches = matches[0:5]
        #for aux in best_matches:
        #    print aux.distance

    points, aux = drawMatches(best_matches, kp1, kp2, color)
    BEST_POINTS.extend(aux[:2])
    if len(points)>0:
        hull = get_convex_hull(points)
        if var.ACTIVE_METHODS:
            draw_convex_hull(var.ACTUAL_IMAGE, hull, color)
        return hull

    return []

def find_intersections_convex(convex):
    dim = var.ACTUAL_IMAGE.shape[0:2]
    blank = np.zeros( dim)

    news = []
    for c in convex:
        aux = drawContours( blank.copy(), c, 0, 1 )
        news.append(aux)


def video_capture():

    global FINISH, DEBUG, TRACKING, PAUSED, NUM_IMAGE, THRESH_VALUE, ACTUAL_IMAGE
    global kp1, des1, orb, IMG_TRAIN, OPTION_MATCHER
    global orb, sift, surf, kp_orb, kp_sift, kp_surf, des_orb, des_sift
    global des_surf, ACTIVE_ORB, ACTIVE_SIFT, ACTIVE_SURF, BEST_POINTS
    global ACTIVE_METHODS, NUM_SUBPLOT, ACTIVE_FOLLOW

    #Create the instance of the video
    cap = cv2.VideoCapture(1)

    #Choose the method to match
    choose_matcher()
    #Instance the matcher
    bf = cv2.BFMatcher()

    call(["clear"])
    print(__doc__)

    var.IMG_TRAIN = cv2.imread("train/zanahoria4.png", 1)
    cv2.imshow('Image to track', var.IMG_TRAIN)

    if var.ACTIVE_ORB:
        var.kp_orb, var.des_orb = var.orb.detectAndCompute(var.IMG_TRAIN,None)
    if var.ACTIVE_SURF:
        var.kp_surf, var.des_surf = var.surf.detectAndCompute(var.IMG_TRAIN,None)
    if var.ACTIVE_SIFT:
        var.kp_sift, var.des_sift = var.sift.detectAndCompute(var.IMG_TRAIN,None)

    while(var.FINISH == False):
        #Call the key listener for options
        var.options()
        # Capture frame-by-frame
        ret1, var.ACTUAL_IMAGE = cap.read()


        if(var.PAUSED == False):
            _, var.ACTUAL_IMAGE = cap.read()
            frame1 = to_gray(var.ACTUAL_IMAGE)
            _, frame2 = cap.read()
            frame2 = to_gray(frame2)

            #Compute the difference between the images
            difference = cv2.absdiff(frame2, frame1)

            #Threshold the image
            _,thr = threshold_bin(difference, var.THRESH_VALUE)

            #Remove possible noise
            blur = blur_(thr)

            convex = []
            #Read key points image 1
            if var.ACTIVE_ORB:
                #print("ORB")
                kp_orb2, des_orb2 = var.orb.detectAndCompute(var.ACTUAL_IMAGE,None)
                c1 = (20, 200, 241)
                #var.ACTUAL_IMAGE = cv2.drawKeypoints(var.ACTUAL_IMAGE, kp_orb2, np.array([]), c1, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                # rgb(20, 69, 241)
                h1 = find_matches(bf, var.des_orb, des_orb2, var.kp_orb, kp_orb2, (0,0,0))
                if h1 != []:
                    convex.append(h1)

            if var.ACTIVE_SURF :
                #print("SURF")
                kp_surf2, des_surf2 = var.surf.detectAndCompute(var.ACTUAL_IMAGE,None)
                c1 = (0,255,0)
                #var.ACTUAL_IMAGE = cv2.drawKeypoints(var.ACTUAL_IMAGE, kp_surf2, np.array([]), c1, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                cv2.drawKeypoints(var.ACTUAL_IMAGE, kp_surf2, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                #rgb(9, 73, 6)
                h2 = find_matches(bf, var.des_surf, des_surf2, var.kp_surf, kp_surf2, (0,255,0))
                if h2 != []:
                    convex.append(h2)


            if var.ACTIVE_SIFT:
                #print("SIFT")
                # rgb(252, 89, 9)
                kp_sift2, des_sift2 = var.sift.detectAndCompute(var.ACTUAL_IMAGE,None)
                c1 = (252, 89, 9)
                #var.ACTUAL_IMAGE = cv2.drawKeypoints(var.ACTUAL_IMAGE, kp_sift2, np.array([]), c1, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                h3 = find_matches(bf, var.des_sift, des_sift2, var.kp_sift, kp_sift2, (252, 89, 9))
                if h3 != []:
                    convex.append(h3)

            if len(BEST_POINTS)>0:
                #print(BEST_POINTS)
                #hull = get_convex_hull(np.array(BEST_POINTS, dtype=np.float32))
                #draw_convex_hull(var.ACTUAL_IMAGE, hull, (255, 255, 255))
                BEST_POINTS = []

                if var.ACTIVE_FOLLOW or True:

                    try:
                        plt.subplot(4,4, NUM_SUBPLOT)
                        NUM_SUBPLOT = ((NUM_SUBPLOT +1) % 17)
                        if(NUM_SUBPLOT == 0):
                            NUM_SUBPLOT +=  1
                        #print(NUM_SUBPLOT)
                        #plt.imshow(var.ACTUAL_IMAGE)
                        #plt.show()
                        #plt.pause(0.001)
                        var.options()
                    except Exception as e:
                        print(e)


            #print("Num of convex: {}".format( len(convex)))

            #Call debug options
            debug(blur)

            #Call tracking movement
            tracking(blur)

            #Show the image
            cv2.setMouseCallback("VIDEO", click_and_crop)

            if(var.CROP[0] != (0,0)):
                cv2.rectangle(var.ACTUAL_IMAGE, var.CROP[0], var.CROP[1], (0, 255, 0), 2)


            cv2.imshow("VIDEO", var.ACTUAL_IMAGE)
            cv2.moveWindow("VIDEO", 10, 10)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
