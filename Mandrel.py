import os

os.system('echo starting pigpiod')
os.system('sudo pigpiod')

import pigpio
import wavePWM
import time
import threading

#Initialise the variables

p = pigpio.pi()
pwm = wavePWM.PWM(p)

#the run_sequence function
def run_sequence(list, delay, loop):
    
    def sequence_loop():
        a = True
        while a:
            for speed in list:
                set_speed(int(speed))
                time.sleep(float(delay))
            if not int(loop):
                a = False
                
    sequence_loop()
        
def run_free():
    a = 1
    while a:
        x = input("Speed (RPM) or Quit\n:")
        if x == "Quit" or x == "0":
            a = 0 
        else:
            set_speed(float(x))

def get_freq_from_rpm(rpm):
    steps = 200
    freq = (rpm * steps) / 60 #this is the rpm entered from the user
    return freq

def start():
    pwm.set_frequency(33.3)
    pwm.set_pulse_start_and_length_in_fraction(20, 0, 0.30)
    pwm.set_pulse_start_and_length_in_fraction(21, 0, 0.30)
    pwm.update()

def set_speed(spd):

    def ramp(freq, steps):
        init_freq = pwm.get_frequency()
        abs_diff = abs(freq - init_freq)
        int_diff = float(freq) - float(init_freq)
        
        curr_freq = pwm.get_frequency()
    
        while not (float(freq) - steps < float(curr_freq) <= float(freq) + steps):
            pwm.set_frequency(curr_freq + (steps * int_diff / abs(int_diff) ))
            pwm.update()
            curr_freq = pwm.get_frequency()
        
        pwm.set_frequency(freq)
        pwm.update()
        
    ramp(get_freq_from_rpm(spd), 2)
    #steps are how many steps we require to complete the one rotation
    #Change this depending on the micro-stepping done
    

def stop():
    pwm.cancel()
    p.stop()
    os.system('echo stopping pigpiod')
    os.system('sudo killall pigpiod')
    
def main():
    a = 1
    start()
    while a:
        mode = input("Free Run, Sequence, or Quit (0, 1, 2)\n:")
        if mode == "2" or mode == "Quit":
            stop()
            a = 0
        
        elif mode == "0":
            run_free()
            
        elif mode == "1":
            
            loop = input("Loop (0, 1)?\n:")
            delay = input("Delay Time in ms\n:")
            sequence = input("Sequence of Speeds Space Separated\n:").split()
            run_sequence(sequence, delay, loop)
            
if __name__ == "__main__":
    main()

