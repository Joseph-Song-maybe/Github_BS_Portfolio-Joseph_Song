import RPi.GPIO as GPIO
import cv2
import numpy as np

GPIO.setmode(GPIO.BCM)

MOTOR1B=24 #5 #Left Motor 22 10 23 24 (22&23 , 10&24)
MOTOR1E=10 #6

MOTOR2B=22 #17  #Right Motor
MOTOR2E=23 #27

GPIO.setup(MOTOR1B, GPIO.OUT)
GPIO.setup(MOTOR1E, GPIO.OUT)

GPIO.setup(MOTOR2B, GPIO.OUT)
GPIO.setup(MOTOR2E, GPIO.OUT)

while(True):
    userInput = input()
    
    if(userInput == 'w'):
        GPIO.output(MOTOR1B,GPIO.HIGH)
        GPIO.output(MOTOR1E,GPIO.LOW)
        GPIO.output(MOTOR2B,GPIO.HIGH)
        GPIO.output(MOTOR2E,GPIO.LOW)
    
    if(userInput == 'a'):
        GPIO.output(MOTOR1B,GPIO.LOW)
        GPIO.output(MOTOR1E,GPIO.LOW)
        GPIO.output(MOTOR2B,GPIO.HIGH)
        GPIO.output(MOTOR2E,GPIO.LOW)
        
    if(userInput == 's'):
        GPIO.output(MOTOR1B,GPIO.LOW)
        GPIO.output(MOTOR1E,GPIO.HIGH)
        GPIO.output(MOTOR2B,GPIO.LOW)
        GPIO.output(MOTOR2E,GPIO.HIGH)
    
    if(userInput == 'd'):
        GPIO.output(MOTOR1B,GPIO.HIGH)
        GPIO.output(MOTOR1E,GPIO.LOW)
        GPIO.output(MOTOR2B,GPIO.LOW)
        GPIO.output(MOTOR2E,GPIO.LOW)

    if(userInput == 'x'):
         GPIO.output(MOTOR1B,GPIO.LOW)
         GPIO.output(MOTOR1E,GPIO.LOW)
         GPIO.output(MOTOR2B,GPIO.LOW)
         GPIO.output(MOTOR2E,GPIO.LOW)