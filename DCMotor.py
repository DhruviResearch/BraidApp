import RPi.GPIO as GPIO # import GPIO librery

from time import sleep

GPIO.setmode(GPIO.BCM)

Motor1A = 13 # set GPIO as Input 1 of the controller IC
Motor1B = 12 # set GPIO as Input 2 of the controller IC
Motor1E = 13 # set GPIO 

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

pwm = GPIO.PWM(Motor1E,100) # configuring Enable pin for PWM

def test():
    print("Hi")
    
def dcStart():
    #pwm.start(50)
    #GPIO.output(Motor1E, GPIO.HIGH)
    GPIO.setmode(GPIO.BCM)

    Motor1A = 13 # set GPIO as Input 1 of the controller IC
    Motor1B = 12 # set GPIO as Input 2 of the controller IC
    Motor1E = 13 # set GPIO 

    GPIO.setup(Motor1A,GPIO.OUT)
    GPIO.setup(Motor1B,GPIO.OUT)
    GPIO.setup(Motor1E,GPIO.OUT)

    #pwm = GPIO.PWM(Motor1E,100) # configuring Enable pin for PW
    pwm.start(50) # Thats the starting duty cycle percentage

def dcMotorCW():
    print ("GO forward")
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)

# this will run your motor in forward direction for 2 seconds with 50% speed.

def setDCRPM(speed):
    pwm.ChangeDutyCycle(speed) # Changes pwm within the motor



def dcMotorCCW():
    print ("GO backward")
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)

def dcStop():
    print ("Now stop")
    GPIO.output(Motor1E,GPIO.LOW)
    pwm.stop() # stop PWM from GPIO output it is necessary
    GPIO.cleanup()
