


# import the necessary packages
import cv2
from picamera.array import PiRGBArray     #As there is a resolution problem in raspberry pi, will not be able to capture frames by VideoCapture
from picamera import PiCamera
import RPi.GPIO as GPIO
import time             
import numpy as np
from PIL import Image

# Detection & Sensor Parameters
proximity = 10
saveVideo = False

#hardware work
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER1 = 19     #Left ultrasonic sensor
GPIO_ECHO1 = 26

GPIO_TRIGGER2 = 16     #Front ultrasonic sensor
GPIO_ECHO2 = 20

GPIO_TRIGGER3 = 11     #Right ultrasonic sensor
GPIO_ECHO3 = 12

MOTOR1B=24  #Left Motor
MOTOR1E=10

MOTOR2B=22  #Right Motor
MOTOR2E=23

LED_PIN=13  #If it finds the ball, then it will light up the led

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER1,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO1,GPIO.IN)    # Echo
GPIO.setup(GPIO_TRIGGER2,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO2,GPIO.IN)
GPIO.setup(GPIO_TRIGGER3,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO3,GPIO.IN)
GPIO.setup(LED_PIN,GPIO.OUT)

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER1, False)
GPIO.output(GPIO_TRIGGER2, False)
GPIO.output(GPIO_TRIGGER3, False)

# Allow module to settle
def sonar(GPIO_TRIGGER,GPIO_ECHO):
    start=0                     
    stop=0
    # Set pins as output and input
    GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
    GPIO.setup(GPIO_ECHO,GPIO.IN)    # Echo

    # Set trigger to False (Low)
    GPIO.output(GPIO_TRIGGER, False)

    # Allow module to settle
    time.sleep(0.01)

    #while distance > 5:
    #Send 10us pulse to trigger
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    begin = time.time()
    while GPIO.input(GPIO_ECHO)==0 and time.time()<begin+0.05:
        start = time.time()

    while GPIO.input(GPIO_ECHO)==1 and time.time()<begin+0.1:
        stop = time.time()

    # Calculate pulse length
    elapsed = stop-start
    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34000

    # That was the distance there and back so halve the value
    distance = distance / 2

    #print ("Distance : %.1f" % distance)


    # Reset GPIO settings
    return distance

GPIO.setup(MOTOR1B, GPIO.OUT)
GPIO.setup(MOTOR1E, GPIO.OUT)

GPIO.setup(MOTOR2B, GPIO.OUT)
GPIO.setup(MOTOR2E, GPIO.OUT)

def forward():
    GPIO.output(MOTOR1B, GPIO.HIGH)
    GPIO.output(MOTOR1E, GPIO.LOW)
    GPIO.output(MOTOR2B, GPIO.HIGH)
    GPIO.output(MOTOR2E, GPIO.LOW)

def reverse():
    GPIO.output(MOTOR1B, GPIO.LOW)
    GPIO.output(MOTOR1E, GPIO.HIGH)
    GPIO.output(MOTOR2B, GPIO.LOW)
    GPIO.output(MOTOR2E, GPIO.HIGH)

def leftturn():
    GPIO.output(MOTOR1B,GPIO.LOW)
    GPIO.output(MOTOR1E,GPIO.LOW)
    GPIO.output(MOTOR2B,GPIO.HIGH)
    GPIO.output(MOTOR2E,GPIO.LOW)

def rightturn():
    GPIO.output(MOTOR1B,GPIO.HIGH)
    GPIO.output(MOTOR1E,GPIO.LOW)
    GPIO.output(MOTOR2B,GPIO.LOW)
    GPIO.output(MOTOR2E,GPIO.LOW)

def stop():
    GPIO.output(MOTOR1E,GPIO.LOW)
    GPIO.output(MOTOR1B,GPIO.LOW)
    GPIO.output(MOTOR2E,GPIO.LOW)
    GPIO.output(MOTOR2B,GPIO.LOW)

def sharp_left():
    GPIO.output(MOTOR1E,GPIO.LOW)
    GPIO.output(MOTOR1B,GPIO.HIGH)
    GPIO.output(MOTOR2E,GPIO.HIGH)
    GPIO.output(MOTOR2B,GPIO.LOW)

def sharp_right():
    GPIO.output(MOTOR1E,GPIO.HIGH)
    GPIO.output(MOTOR1B,GPIO.LOW)
    GPIO.output(MOTOR2E,GPIO.LOW)
    GPIO.output(MOTOR2B,GPIO.HIGH)




#Image analysis work
def segment_colour(frame):    #returns only the red colors in the frame
    hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask_1 = cv2.inRange(hsv_roi, np.array([160, 140,1]), np.array([190,255,255]))
    ycr_roi=cv2.cvtColor(frame,cv2.COLOR_BGR2YCrCb)
    mask_2=cv2.inRange(ycr_roi, np.array((0.,165.,0.)), np.array((255.,255.,255.)))

    mask = mask_1 #| mask_2
    kern_dilate = np.ones((8,8),np.uint8)
    kern_erode  = np.ones((3,3),np.uint8)
    mask= cv2.erode(mask,kern_erode)    #Eroding
    mask=cv2.dilate(mask,kern_dilate)     #Dilating
    # Debug: Eren
    (h,w) = mask.shape
    #cv2.imshow('mask', cv2.resize(mask, (w//1,h//1)) )
    #cv2.imshow('mask',mask)
    return mask

def find_blob(blob): #returns the red colored circle
    largest_contour=0
    cont_index=0
    contours, hierarchy = cv2.findContours(blob, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    for idx, contour in enumerate(contours):
        area=cv2.contourArea(contour)
        if (area >largest_contour) :
            largest_contour=area
            cont_index=idx
        #if res>15 and res<18:
        #    cont_index=idx

    r=(0,0,2,2)
    if len(contours) > 0:
        r = cv2.boundingRect(contours[cont_index])

    return r,largest_contour

def target_hist(frame):
    hsv_img=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hist=cv2.calcHist([hsv_img],[0],None,[50],[0,255])
    return hist

def no_obstacle(distanceL, distanceC, distanceR):
    if(distanceL > proximity and distanceC > proximity and distanceR > proximity):
        return True
    return False

#CAMERA CAPTURE
##initialize the camera and grab a reference to the raw camera capture
#camera = PiCamera()
#camera.resolution = (160, 120)
#camera.framerate = 16
#rawCapture = PiRGBArray(camera, size=(160, 120))
## allow the camera to warmup
#time.sleep(0.001)

camera = cv2.VideoCapture(0)
camera.set(3,320)
camera.set(4,240)

# capture frames from the camera
#-------------------------------
# Commented out by Eren
#for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#    #grab the raw NumPy array representing the image, then initialize the timestamp and occupied/unoccupied text
#    frame = image.array
#    frame=cv2.flip(frame,1)
#-------------------------------

imgs_video = []  # We are going to add frames to this list in order to greate a gif
imgs_count = 0
while(True):       
    ret, frame = camera.read()
    height = frame.shape[0]
    width = frame.shape[1]

    #cv2.imshow('frame', frame)#[:,:,[2,1,0]])

    # I guess that camera (VideoCapture.read) captures in RGB, but cv2.imshow uses BGR to display.
    # I decided to flip the channel order [0,1,2] (from camera) to [2,1,0] (to display via cv2.imshow)
    #frame_r = cv2.resize(frame, (width//4,height//4))
    #cv2.imshow('frame', frame_r[:,:,[2,1,0]])

    global centre_x
    global centre_y
    centre_x=0.
    centre_y=0.
    hsv1 = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    mask_red=segment_colour(frame[:,:,[0,1,2]])
    #masking red the frame
    loct,area=find_blob(mask_red)
    x,y,w,h=loct

    #distance coming from front ultrasonic sensor
    distanceC = sonar(GPIO_TRIGGER2,GPIO_ECHO2)
    #distance coming from right ultrasonic sensor
    distanceR = sonar(GPIO_TRIGGER3,GPIO_ECHO3)
    #distance coming from left ultrasonic sensor
    distanceL = sonar(GPIO_TRIGGER1,GPIO_ECHO1)
    print("left distance: ", distanceL//1)
    print("center distance: ", distanceC//1)
    print("right distance: ", distanceR//1)
    if (w*h) < 10:
        found=0
    else:
        found=1
        simg2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
        centre_x=x+((w)/2)
        centre_y=y+((h)/2)
        cv2.circle(frame,(int(centre_x),int(centre_y)),3,(0,110,255),-1)
        centre_x-=80
        centre_y=6--centre_y
        print (centre_x)

    initial=15000
    GPIO.output(LED_PIN,GPIO.LOW)       
    print("area of ball is: ", area)
    #mid_frame = width//2 -40
    #print("mid frame = ", mid_frame)
    if((area<15000) and (found == 1)):
        # if(distanceL > 25 and distanceC > 25 and distanceR > 25):
        if no_obstacle(distanceL, distanceC, distanceR):
            if(centre_x < -10):
                leftturn()
                print("left turn")
            elif(centre_x > 170):
                rightturn()
                print("right turn")
            else:
                forward()
                print("forward")

        else:
            stop()       
        '''
        '''
    elif(found==0):
        if no_obstacle(distanceL, distanceC, distanceR):
            print("finding ball, turning")
            rightturn()
            time.sleep(0.30)
            stop()
            time.sleep(0.30)
            reverse()
            time.sleep(0.30)
            stop()
            time.sleep(0.2)
        else:
            reverse()

    else:
        stop()



    cv2.imshow("draw",frame)
    #rawCapture.truncate(0)  # clear the stream in preparation for the next frame

    # Convert mask_red (1-channel grayscale) to 3-channel (RGB) so we can concatenate
    # with the processed RGB frame (with box, center marked) in order to display side-by-side
    mask_red_rgb = cv2.cvtColor(mask_red,cv2.COLOR_GRAY2RGB)
    frame_and_mask = np.concatenate((frame, mask_red_rgb), axis=1)
    #qcv2.imshow("side-by-side", frame_and_mask)

    if saveVideo and (imgs_count < 360):
        imgs_video.append(frame_and_mask)
        imgs_count += 1

    if(cv2.waitKey(1) & 0xff == ord('q')):
        if saveVideo:
            out = cv2.VideoWriter("side_by_side.avi", 0, 15, (2*width, height))
            for img in imgs_video:
                out.write(img)
            out.release()   
        stop()
        break

GPIO.cleanup() #free all the GPIO pins
camera.release()
