#THIS CODE IS WRITTEN TO RUN THE MOTORS WITHOUT THE GUI
#(isnt complete and error proof)

import DCMotor as braider
import test as mandrel
import sys
import os
import math 

#This is the method to relate the speeds with the braid angles and mandrel radius
def equation(rpm, motor):
    if motor == "B":
        mandrel_radius_mm= 2
        Braid_angle_degrees=30
        rad_of_gear_mm=20
        return ((float(rpm))*mandrel_radius_mm)/(rad_of_gear_mm*math.tan(Braid_angle_degrees/57.296))
    elif motor == "M":
        mandrel_radius_mm= 2
        Braid_angle_degrees=30
        rad_of_gear_mm=20
        return (((float (rpm))*(rad_of_gear_mm*math.tan(Braid_angle_degrees/57.296)))/mandrel_radius_mm)

#The main method to run the motors
def main():
    mandrelSetup = False
    a=1
    while a:
    
    # here the user can select if the user wants
    # to control the speed using braider or mandrel 

        motorType = input("What type of Motor do you want to run? Braider/ Mandrel(B/M/Quit): ")
        

    #If they chose to control the Braider, you can set rotational speed and its direction
        while 1:
        
            if motorType in ["B","b"]:
                
                rpm = input("\nWhat speed do you want to move the braid head at?(Type Quit to end): ")
                

                if rpm in ["Quit","Q","q"]:
                    #StepperQuit
                    print("Quitting")
                    braider.dcStop()
                    mandrel.stop()
                    sys.exit(0)

                else:
                    if mandrelSetup == False:
                        mandrel.start()
                        braider.dcStart()
                    
                        braider.setDCRPM(float(rpm))
                        print(float(equation(rpm,"B")))
                        mandrel.set_speed(float(equation(rpm, "B")))

    # If they choose Mandrel, one can select the linear velocity of mandrel
    
            elif motorType in ["M","m"]:
                
                rpm = input("\nWhat speed do you want to move the mandrel at?(Type Quit to end): ")
                if rpm in ["Quit","Q", "q"]:
                    #StepperQuit
                    print("Quitting")
                    braider.dcStop()
                    mandrel.stop()
                    sys.exit(0)

                else:
                    print("Mandrel Running")
                    if mandrelSetup == False:
                        mandrel.start()
                        braider.dcStart()
                    mandrel.set_speed(float(rpm))
                    braider.setDCRPM(float(equation(rpm,"M")))
                    print(int(equation(rpm,"M")))


            elif motorType in ["Q","q", "Quit"]:
                #StepperQuit
                print("Quitting")
                braider.dcStop()
                mandrel.stop()
                sys.exit(0)
            else:
                print("Wrong Input please input something from the given options.\n")
                print("Quitting")
                braider.dcStop()
                mandrel.stop()
                sys.exit(0)

if __name__ == "__main__":
    main()
            
