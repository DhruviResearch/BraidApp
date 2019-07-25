import os
os.system('echo starting pigpiod')
os.system('sudo pigpiod')
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen,ScreenManager
from os import listdir
from kivy.properties import ObjectProperty
from kivy.graphics import Color, Rectangle
#import DCMotor as braider
#import Mandrel
import sys
import math
from kivy.uix.image import Image 

#This is required to upload the .kv file on the code
Builder.load_file("main.kv")
Builder.load_file("script.kv")

#This is the main screen
class Container(Screen):
    #Stop the code and exit
    def stop(self):
        try:
            #braider.dcStop()
            #Mandrel.stop()
            exit()
        except:
            exit()
    pass

#Class for independant mode, where users can control speed of the motors independantly 
class indeMotor(Screen): 
    #This is where the text inputs are initialised
    motorSetup = False
    inde_braid_angle= ObjectProperty(None)
    inde_dc_text_input= ObjectProperty(None)
    inde_step_text_input= ObjectProperty(None)
    display= ObjectProperty(None)
    
    
    self.inde_braid_angle.text = braidAngle
#methods within the class, can be called on press of buttons
    
    def submit_radius(self): #Submits the Mandrel radius 
        mandrel_rad = int(self.inde_mand_rad_text_input.text)
        print(mandrel_rad)     
    def submit_speeds(self): #Set the speeds ofthe motors after they have been started
        try:
            braid_speed = int(self.inde_dc_text_input.text)
            takeup_speed = int(self.inde_step_text_input.text)
            #braider.setDCRPM(braid_speed)
            #Mandrel.set_speed(takeup_speed)
            print("Braider speed is",  braid_speed)
            print("Step-up speed is", takeup_speed)
        except ValueError:
            print("Please enter an Integer or check if both fields have values")
        #except:
            #print("You did not start the motors...")
    def inde_start(self): #Start the motors
        #try: 
            #braider.dcStart()
            #Mandrel.start()
        #except:
            #print("There was an error starting motors! Please try again...")
        pass
    def increment(self):#used to increment the DC speed
        try:
            self.inde_dc_text_input.text =  str(int(self.inde_dc_text_input.text) + 1)
        except:
            print("Please try again! Check if there is a variable entered")
        pass
    def decrement(self):#used to decrement the DC speed
        try:
            self.inde_dc_text_input.text = str(int(self.inde_dc_text_input.text) - 1)
            braider.setDCRPM(self.inde_dc_text_input.text)
        except:
            print("Please try again! Check if there is a variable entered")
        pass
    
    def Stop(self): #Stop the Motors
        try:
            print("stop")
            braider.dcStop()
            Mandrel.stop()
        except:
            print("You already exitted")
        pass

#This is the dependant mode where one speed affects the other (STILL NEEDS TO BE WORKED ON)
class depMotor(Screen):
    dep_braid_angle_text_input = ObjectProperty(None)
    dep_mand_rad_text_input= ObjectProperty(None)
    dep_dc_text_input= ObjectProperty(None)
    dep_step_text_input= ObjectProperty(None)

    def submit_dep_angle(self):
        try:
            BraidAngleDep= int(self.dep_braid_angle_text_input.text)
            print(BraidAngleDep)
        except ValueError:
            print("Wrong Input! Please enter an Integer")
    def submit_dep_rad(self):
        try:
            MandrelRadDep = int(self.dep_mand_rad_text_input.text)
            print(MandrelRadDep)
        except ValueError:
            print("Wrong Input! Please enter an Integer")
    def submit_speed_braider(self):
        try:
            BraiderSpeed = int(self.dep_dc_text_input.text)
            print(BraiderSpeed)
            #braider.dcStart()
            #braider.setDCRPM(BraiderSpeed_speed)
        except ValueError:
            print("Wrong Input! Please enter an Integer")
    def submit_speed_takeup(self):
        try:
            MandrelSpeed = int(self.dep_step_text_input.text)
            print(MandrelSpeed)
        except ValueError:
            print("Wrong Input! Please enter an Integer")
    def increment(self):
        try:
            self.dep_dc_text_input.text =  str(int(self.dep_dc_text_input.text) + 1)
            #braider.setDCRPM(self.inde_dc_text_input.text)
        except:
            print("Please try again! Check if there is a variable entered")
        pass
    def decrement(self):
        try:
            self.dep_dc_text_input.text = str(int(self.dep_dc_text_input.text) - 1)
            #braider.setDCRPM(self.inde_dc_text_input.text)
        except:
            print("Please try again! Check if there is a variable entered")
        pass

#Script used to calculate braid variable so various configurations can be manufactured
class IndeScript(Screen):
    mandrel_rad_text_input= ObjectProperty(None)
    yarn_width_text_input= ObjectProperty(None)
    c_text_input= ObjectProperty(None)
    velocity_text_input= ObjectProperty(None)
    speed_text_input= ObjectProperty(None)
    half_cone_text_input= ObjectProperty(None)
    

    def SubmitVariables(self): #this method
        try:
            R= float(self.mandrel_rad_text_input.text)
            Wy= float(self.yarn_width_text_input.text)
            N=int(self.c_text_input.text)
            mandrelVelocity=float(self.velocity_text_input.text)
            rotationalVelocity = float(self.speed_text_input.text)
            gamma = math.radians(int(self.half_cone_text_input.text))
            #print(rotationalVelocity)

            #Calculate braid angle from mandrel/ carrier speed
            rho = 2 * math.pi * R * (mandrelVelocity / rotationalVelocity)
            angle = math.atan(rho) * (180 / math.pi)
            self.braid_angle_text_input.text = '{0:.1f}'.format(angle)
        
            #Calculate Braid Jam Angle
            numerator = Wy * math.sin(gamma)
            denominator = 2 * R * math.sin(2 * math.pi * math.sin(gamma) / N)
            thetaJammed = (math.acos(numerator / denominator)) * (180 / math.pi)
            self.jam_angle_text_input.text = '{0:.1f}'.format(thetaJammed)
        
            #Calculate Yarn Undulation and Shift angle
            beta = 2 * math.pi / N
            Angle = math.radians(angle)
            Lund = R*beta / math.sin(Angle)
            self.yarn_und_text_input.text = '{0:.3f}'.format(Lund)
            self.shift_angle_text_input.text = '{0:.3f}'.format(beta)
            
        except ValueError:
            print("Please check if all variables entered are numbers and all the variables are filled")
        except:
            print("Check if everything is working fine and try again")
    
    def startBraiding(self):
        self.manager.current = 'inde'
        self.indeMotor(self.braid_angle_text_input.text)
        
        
        

#Controls the windows within the App
sm = ScreenManager()
sm.add_widget(Container(name='main'))
sm.add_widget(indeMotor(name='inde'))
sm.add_widget(depMotor(name='dep'))
sm.add_widget(IndeScript(name='calc'))


#this is the part that runs the main App
class MainApp(App):
    def build(self):
        return sm
if __name__ == "__main__":
    MainApp().run()