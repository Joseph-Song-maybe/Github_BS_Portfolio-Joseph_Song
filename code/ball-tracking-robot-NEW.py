# import the necessary packages
import cv2 #OpenCV
from picamera import PiCamera
import RPi.GPIO as GPIO
import time              
import numpy as np

#Ultrasonic Sensor Proximity parameter
proximity = 10 

#Hardware work
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER1 = 19     #LEFT ultrasonic sensor
GPIO_ECHO1 = 26

GPIO_TRIGGER2 = 16     #FRONT ultrasonic sensor
GPIO_ECHO2 = 20

GPIO_TRIGGER3 = 11     #RIGHT ultrasonic sensor
GPIO_ECHO3 = 12

motor1B=24#6  #LEFT Motor
motor1E=10#5

motor2B=22  #RIGHT Motor
motor2E=23

LED_PIN=18  #If it finds the ball, then it will light up the led

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER1,GPIO.OUT)  # Trigger 1
GPIO.setup(GPIO_ECHO1,GPIO.IN)  # Echo 1
GPIO.setup(GPIO_TRIGGER2,GPIO.OUT)  # Trigger 2
GPIO.setup(GPIO_ECHO2,GPIO.IN)  # Echo 2
GPIO.setup(GPIO_TRIGGER3,GPIO.OUT)  # Trigger 3
GPIO.setup(GPIO_ECHO3,GPIO.IN)  # Echo 3
GPIO.setup(LED_PIN,GPIO.OUT)  # LED light 

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
    
    # Distance pulse traveled in that time is time multiplied by the speed of sound (cm/s)
    distance = elapsed * 34000
     
    # That was the distance there and back, so take half of the value
    distance = distance / 2

    # Reset GPIO settings
    return distance

GPIO.setup(motor1B, GPIO.OUT)
GPIO.setup(motor1E, GPIO.OUT)

GPIO.setup(motor2B, GPIO.OUT)
GPIO.setup(motor2E, GPIO.OUT)

# Define motor movement functions
def forward():
    GPIO.output(motor1B, GPIO.HIGH)
    GPIO.output(motor1E, GPIO.LOW)
    GPIO.output(motor2B, GPIO.HIGH)
    GPIO.output(motor2E, GPIO.LOW)
     
def reverse():
    GPIO.output(motor1B, GPIO.LOW)
    GPIO.output(motor1E, GPIO.HIGH)
    GPIO.output(motor2B, GPIO.LOW)
    GPIO.output(motor2E, GPIO.HIGH)
     
def leftturn():
    GPIO.output(motor1B,GPIO.LOW)
    GPIO.output(motor1E,GPIO.LOW)
    GPIO.output(motor2B,GPIO.HIGH)
    GPIO.output(motor2E,GPIO.LOW)
     
def rightturn():
    GPIO.output(motor1B,GPIO.HIGH)
    GPIO.output(motor1E,GPIO.LOW)
    GPIO.output(motor2B,GPIO.LOW)
    GPIO.output(motor2E,GPIO.LOW)

def stop():
    GPIO.output(motor1E,GPIO.LOW)
    GPIO.output(motor1B,GPIO.LOW)
    GPIO.output(motor2E,GPIO.LOW)
    GPIO.output(motor2B,GPIO.LOW)
    
def sharp_left():
    GPIO.output(motor1B,GPIO.LOW)
    GPIO.output(motor1E,GPIO.HIGH)
    GPIO.output(motor2B,GPIO.HIGH)
    GPIO.output(motor2E,GPIO.LOW)
    
def sharp_right():
    GPIO.output(motor1B,GPIO.HIGH)
    GPIO.output(motor1E,GPIO.LOW)
    GPIO.output(motor2B,GPIO.LOW)
    GPIO.output(motor2E,GPIO.HIGH)
    
def back_left():
    GPIO.output(motor1B,GPIO.LOW)
    GPIO.output(motor1E,GPIO.LOW)
    GPIO.output(motor2B,GPIO.LOW)
    GPIO.output(motor2E,GPIO.HIGH)
    
def back_right():
    GPIO.output(motor1B,GPIO.LOW)
    GPIO.output(motor1E,GPIO.HIGH)
    GPIO.output(motor2B,GPIO.LOW)
    GPIO.output(motor2E,GPIO.LOW)
     
     
#Image analysis work
def segment_colour(frame):    #returns only the red colors in the frame
    hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    mask_1 = cv2.inRange(hsv_roi, np.array([150, 140,1]), np.array([190,255,255])) #Experimentally set BGR values 
    # ycr_roi=cv2.cvtColor(frame,cv2.COLOR_BGR2YCrCb)
    # mask_2=cv2.inRange(ycr_roi, np.array((0.,165.,0.)), np.array((255.,255.,255.)))

    mask = mask_1 # | mask_2
    kern_dilate = np.ones((8,8),np.uint8)
    kern_erode  = np.ones((3,3),np.uint8)
    mask= cv2.erode(mask,kern_erode)    #Eroding
    mask=cv2.dilate(mask,kern_dilate)     #Dilating
    
    (h,w) = mask.shape
    
    #cv2.imshow('mask', mask) # Shows mask (identified red pixels) 
    
    return mask

def find_blob(blob): # Returns the red colored circle
    largest_contour=0
    cont_index=0
    contours, hierarchy = cv2.findContours(blob, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    for idx, contour in enumerate(contours):
        area=cv2.contourArea(contour)
        if (area >largest_contour) :
            largest_contour=area
            cont_index=idx
                    
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
    else:
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
flag = 0 #SEARCHING: 0: left turn for last location of ball, 1: right turn for last location of ball
flag_reroute = -1 #REROUTE SEARCHING  -1: No reroute, 0:reroute left , 1: reroute rigth
while(True):       
    ret, frame = camera.read()
    height = frame.shape[0]
    width = frame.shape[1]

    #cv2.imshow('frame', frame)#[:,:,[2,1,0]])
    
    # I guess that camera (VideoCapture.read) captures in RGB, but cv2.imshow uses BGR to display.
    # I decided to flip the channel order [0,1,2] (from camera) to [2,1,0] (to display via cv2.imshow)
    #frame_r = cv2.resize(frame, (width//4,height//4))
    #cv2.imshow('frame', frame_r[:,:,[2,1,0]])
    
    global center_x
    global center_y
    center_x=0.
    center_y=0.
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
    #print("left distance: ", distanceL//1)
    #print("center distance: ", distanceC//1)
    #print("right distance: ", distanceR//1)
    print("\n\n--------------")
    #print("x,y,w,h = ", x,y,w,h)
    #print("dL,dC,dR = ", distanceL//1, distanceC//1, distanceR//1)
    print("0:left, 1: right => flag = ", flag)
    
    if (w*h) < 400:
        print ("no boxjcjsghdjcgsdhcdsc")
        GPIO.output(LED_PIN, GPIO.LOW)
        found=0
    else:
        found=1
        simg2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
        center_x=x+((w)/2)
        center_y=y+((h)/2)
        cv2.circle(frame,(int(center_x),int(center_y)),3,(0,110,255),-1)
        #center_x-=80
        center_y=6--center_y
        print (center_x)
    
    initial=150000  # Something very large
    #print("area of ball is: ", area)
    #mid_frame = width//2 -40
    #print("mid frame = ", mid_frame)
    if((area<initial) and (found == 1)):
        print("ball found")
        if no_obstacle(distanceL, distanceC, distanceR):
            #print("distance good")                
            GPIO.output(LED_PIN,GPIO.HIGH)
            #GPIO.output(LED_PIN,GPIO.LOW)
            #if(center_x < 0):
            if(center_x < 40): # width=320 full frame
                flag = 0
                leftturn()
                print("left turn")
            #elif(center_x > 190):
            elif(center_x > 280):
                flag = 1
                rightturn()
                print("right turn")
            else:
                forward()
                print("forward")
    
        else:
            stop()
            #''
            if (distanceC < proximity):
                stop()
            elif(distanceL<proximity):
                print("rerouting right")
                back_left()
                time.sleep(0.2)
                flag_reroute = 1
                if(flag_reroute == 1):
                    forward()
                    
                #time.sleep(0.1)
                #back_left()
                #time.sleep(0.1)
            elif(distanceR<proximity):
                print("rerouting left")
                back_right()
                time.sleep(0.2)
                flag_reroute = 0
                if(flag_reroute == 0):
                    forward()
                #time.sleep(0.1)
                #back_right()
                #time.sleep(0.1)
            #stop()
            

    elif(found==0):
        GPIO.output(LED_PIN,GPIO.LOW)
        if no_obstacle(distanceL, distanceC, distanceR):
            print("finding ball, turning")
            if(flag == 0): # If last seen location was on the left, search by turning left
                print("searching left")
                sharp_left()
                time.sleep(0.08)
                stop()
            elif(flag == 1):
                sharp_right()
                print("searching right")
                time.sleep(0.08)
                stop()
            '''
            print("finding ball, turning")
            rightturn()
            time.sleep(0.05)
            stop()
            time.sleep(0.05)
            reverse()
            time.sleep(0.05)
            stop()
            '''
        else:
            reverse()
            print("reversing")
    else:
        stop()

    
    
    #cv2.imshow("draw",frame)
    #rawCapture.truncate(0)  # clear the stream in preparation for the next frame
    
    # Convert mask_red (1-channel grayscale) to 3-channel (RGB) so we can concatenate
    # with the processed RGB frame (with box, center marked) in order to display side-by-side
    #mask_red_rgb = cv2.cvtColor(mask_red,cv2.COLOR_GRAY2RGB)
    #frame_and_mask = np.concatenate((frame, mask_red_rgb), axis=1)

    
    if(cv2.waitKey(1) & 0xff == ord('q')):
        stop()
        break

GPIO.cleanup() #free all the GPIO pins
camera.release()
