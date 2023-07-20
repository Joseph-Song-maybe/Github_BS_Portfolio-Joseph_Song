#PYTHON

#Author: Derin Gurses
#Version: 07/18/2023

import cv2 #OpenCV
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import numpy as np

#Ultrasonic Sensor proximity parameter (centimeter)
sensor_proximity = 10
rerouting_proximity = 17.5
#Hardware work
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER1 = 19     #LEFT ultrasonic sensor
GPIO_ECHO1 = 26

GPIO_TRIGGER2 = 16     #FRONT ultrasonic sensor
GPIO_ECHO2 = 20

GPIO_TRIGGER3 = 11     #RIGHT ultrasonic sensor
GPIO_ECHO3 = 12

motor1B=6  #LEFT Motor
motor1E=5

motor2B=22  #RIGHT Motor
motor2E=23

LED_SEARCH=18  #If it finds the ball, then it will light up the LED
LED_PARKED=5 #Once the robot has parked in front of the ball, it will light up the LED

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER1,GPIO.OUT)  # Trigger 1
GPIO.setup(GPIO_ECHO1,GPIO.IN)  # Echo 1
GPIO.setup(GPIO_TRIGGER2,GPIO.OUT)  # Trigger 2
GPIO.setup(GPIO_ECHO2,GPIO.IN)  # Echo 2
GPIO.setup(GPIO_TRIGGER3,GPIO.OUT)  # Trigger 3
GPIO.setup(GPIO_ECHO3,GPIO.IN)  # Echo 3
GPIO.setup(LED_SEARCH,GPIO.OUT)  # LED light for tracking
GPIO.setup(LED_PARKED,GPIO.OUT) # LED light for parking

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
    distance = elapsed * 34300
     
    # That was the distance there and back, so take half of the value
    distance = distance / 2

    # Reset GPIO settings, return distance (in cm) appropriate for robot movements
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
    GPIO.output(motor1B,GPIO.LOW)
    GPIO.output(motor1E,GPIO.LOW)
    GPIO.output(motor2B,GPIO.LOW)
    GPIO.output(motor2E,GPIO.LOW)
    
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
    
    mask_1 = cv2.inRange(hsv_roi, np.array([150, 140,1]), np.array([190,255,255])) #Experimentally set BGR values appropriate for desired color

    mask = mask_1
    kern_dilate = np.ones((8,8),np.uint8)
    kern_erode  = np.ones((3,3),np.uint8)
    mask= cv2.erode(mask,kern_erode)    #Eroding
    mask=cv2.dilate(mask,kern_dilate)     #Dilating
    
    (h,w) = mask.shape
    
    cv2.imshow('mask', mask) # Shows mask (B&W screen with identified red pixels)
    
    return mask

def find_blob(blob): # Returns the red colored largest object
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

def no_obstacle(distanceL, distanceC, distanceR): #TRUE: no obstacles within 10 cm of sensor, FALSE: obstacle
    if(distanceL > sensor_proximity and distanceC > sensor_proximity and distanceR > sensor_proximity):
        return True
    else:
        return False

#CAMERA CAPTURE
 
camera = cv2.VideoCapture(0)
camera.set(3,320)
camera.set(4,240)



flag = 0 #SEARCHING: 0: left turn for last location of ball, 1: right turn for last location of ball
flag_reroute = -1 #REROUTE SEARCHING  -1: No reroute, 0:reroute left , 1: reroute right
while(True):
    ret, frame = camera.read()
    height = frame.shape[0]
    width = frame.shape[1]

    #cv2.imshow('frame', frame) #Shows the frame (video capture)
    
    global center_x
    global center_y
    center_x=0.
    center_y=0.
    hsv1 = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    mask_red=segment_colour(frame[:,:,[0,1,2]])
    
    #Masking red the frame
    loct,area=find_blob(mask_red)
    x,y,w,h=loct
     
    #distance coming from front ultrasonic sensor
    distanceC = sonar(GPIO_TRIGGER2,GPIO_ECHO2)
    #distance coming from right ultrasonic sensor
    distanceR = sonar(GPIO_TRIGGER3,GPIO_ECHO3)
    #distance coming from left ultrasonic sensor
    distanceL = sonar(GPIO_TRIGGER1,GPIO_ECHO1)
    print("dL, dC, dR ", distanceL//1, distanceC//1, distanceR//1)
    
    print("\n\n--------------") #Nicely formatted printing for checking distance or debugging
    print("0:left, 1: right ===> flag = ", flag)
    
    if (w*h) < 400: #If the area of a found red spot is <400, ignore it and set found = 0
        print ("This object is not the ball.")
        GPIO.output(LED_SEARCH, GPIO.LOW)
        GPIO.output(LED_PARKED, GPIO.LOW)
        found=0
    else:
        found=1
        simg2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
        center_x=x+((w)/2)
        center_y=y+((h)/2)
        cv2.circle(frame,(int(center_x),int(center_y)),3,(0,110,255),-1)
        
    print("area is ", area)
    
    initial=150000  # Something very large
    
    if((area<initial) and (found == 1)):
        print("Ball is found.")
        if no_obstacle(distanceL, distanceC, distanceR): #If ball is found and no obstacle, turn on searching LED
            GPIO.output(LED_SEARCH,GPIO.HIGH)
            GPIO.output(LED_PARKED,GPIO.LOW)
            
            if(center_x < 40): # Full frame's width is 320
                flag = 0 # Last seen on the left (if robot loses ball)
                leftturn()
                print("Turning left")
            
        
            elif(center_x > 280):
                flag = 1 # Last seen on the right (if robot loses ball)
                rightturn()
                print("Turning right")
                
                
            else: #If the ball is relatively centered, move forward
                forward()
                print("moving forward")
                if(center_x < width//2):
                    flag = 0 #If ball is lost while to the left of the center, assign flag = 0
                elif(center_x >= width//2):
                    flag = 1 #If ball is lost while to the right of the center, assign flag = 1
                    
                print(width//2)
                print("Flag is ", flag)
            
    
        else:
            stop()
            
            if ((distanceC < sensor_proximity) and (area >= 10000)): # PARKED STATE: If the ball is in front of the center sensor
                stop()
                GPIO.output(LED_SEARCH,GPIO.LOW) #Turn off the tracking LED
                GPIO.output(LED_PARKED, GPIO.HIGH) #Turn on the parked LED
                
            # REROUTING MOVEMENT
            elif(distanceL < rerouting_proximity):
                print("Rerouting right")
                back_left()
                time.sleep(0.2)
                flag_reroute = 1
                if(flag_reroute == 1):
                    forward()
                    
            elif(distanceR < rerouting_proximity):
                print("rerouting left")
                back_right()
                time.sleep(0.2)
                flag_reroute = 0
                if(flag_reroute == 0):
                    forward()
            

    elif(found==0):
        GPIO.output(LED_SEARCH,GPIO.LOW)
        if no_obstacle(distanceL, distanceC, distanceR):
            print("Finding ball, turning")
            if(flag == 0): # If last seen location was on the left, search by turning left
                print("Searching left")
                sharp_left()
                time.sleep(0.08)
                stop()
            elif(flag == 1): # If last seen location was on the right, search by turning right
                sharp_right()
                print("Searching right")
                time.sleep(0.08)
                stop()
            
        else:
            reverse()
            print("Reversing")
    else:
        stop()

    
    
    cv2.imshow("draw",frame) #Shows frame with bounding box
    
    if(cv2.waitKey(1) & 0xff == ord('q')): #Press q to break the loop and stop moving
        stop()
        break

GPIO.cleanup() #free all the GPIO pins
camera.release()
