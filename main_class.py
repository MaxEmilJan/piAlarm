import time
import sys
import os
import board
import neopixel
from gpiozero import Button
from urllib.request import urlopen
import numpy as np

class piAlarm:
    
    # methode to check network connection
    def net_connect(self):
        try:
            urlopen("http://www.google.com")
            return True
        except:
            return False
        
    def __init__(self):
        try:
            print("init...")
            # Pin for GND (Pin 9)
            # Pin for PWR (Pin 4)
            # GPIO pin for the DATA-IN wire (GPIO 21; Pin 40)
            self.pixel_pin = board.D21
            # number of LEDs
            self.num_pixels = 26
            # init the LEDs
            self.pixels = neopixel.NeoPixel(self.pixel_pin, 
                                       self.num_pixels, 
                                       brightness=1,
                                       auto_write=False,
                                       pixel_order=neopixel.GRB)

            # set power button on GPIO 4 (Pin 7)
            self.button_alarm = Button(4)
            # set alarm button on GPIO 5 (Pin 29)
            self.button_power = Button(5)
            # init alarm time
            self.t_alarm = "4:30"
            # how many seconds until the light reaches full brightness
            self.sunrise_speed = 20 * 60
            # list of different alarms (Time = start of sunrise --> full brightness 30 min later)
            self.list_alarm = [["4:30", (255, 100, 0)], 
                               ["5:00", (0, 255, 100)],
                               ["6:30", (100, 0, 255)],
                               #[str(time.localtime()[3]) + ":" + str(time.localtime()[4] + 1), (0, 100, 255)]
                               ["off", (255, 150, 100)]
                              ]
            # counter for indexing the different alarms
            self.cnt = 0
            
            # LED values for the loading circle
            loading_led_list = [(15, 3, 0), (40, 12, 0), (90, 30, 0), (190, 66, 0)]
            # variable to index single LEDs for loading circle
            a = 0
            
            # wait for network connection
            print("Waiting for network connection!")
            
            while time.time() < 30:
                if self.net_connect() is True:
                    self.pixels.fill((0, 0, 0))
                    print("Network connection established!")
                    break
                else:
                    if a >= 23:
                        for i in range(a, 26):
                            self.pixels[i] = loading_led_list[i-a]
                        for i in range(0, a):
                            self.pixels[i] = (0, 0, 0)
                        if a == 23:
                            self.pixels[0] = (190, 66, 0)
                        elif a == 24:
                            self.pixels[1] = (190, 66, 0)
                            self.pixels[0] = (90, 30, 0)
                        elif a == 25:
                            self.pixels[2] = (190, 66, 0)
                            self.pixels[1] = (90, 30, 0)
                            self.pixels[0] = (40, 12, 0)
                        else:
                            pass
                        
                    else:
                        for i in range(a, a + 4):
                            self.pixels[i] = loading_led_list[i-a]
                        for i in range(0, a):
                            self.pixels[i] = (0, 0, 0)
                        
                    a = a + 1
                    if a == 26:
                        self.pixels[25] = (0, 0, 0)
                        a = 0
                    else:
                        pass
                    self.pixels.show()
                    time.sleep(0.1)
            
            # signal succcessfull init with green LEDs
            for i in [0, 5, 11, 16, 20, 25]:
                self.pixels[i] = (0, 100, 0)
            self.pixels.show()
            # wait 2 seconds
            time.sleep(2)
            # turn of LEDs
            self.pixels.fill((0, 0, 0))
            self.pixels.show()
            print("init done")
        except Exception as e:
            print(e)
            exit()
            
    # methode gets called when the red button is pressed
    # turns of pixels, terminates script, initiates shutdown
    def button_shutdown(self):
        print("red button pressed!")
        # turn of LEDs in case the sunrise is active

        self.pixels.fill((0, 0, 0))
        self.pixels.show()
        # shutdown the system in 60 seconds
        os.system("sudo shutdown -P +1")
        print("System will power off in one minute!")
        # signal shutdown with red LEDs
        for i in [0, 5, 11, 16, 20, 25]:
            self.pixels[i] = (100, 0, 0)
        self.pixels.show()
        # wait 2 seconds
        time.sleep(0.5)
        # turn of LEDs
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
        # terminate this script
        sys.exit("Programm terminated!")
        exit()
        
    # methode get called when the blue button is pressed
    # switches between three different alarm times
    def button_change_alarm(self):
        print("blue button pressed!")
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
        # set alarm time to one of the three in list
        self.t_alarm = self.list_alarm[self.cnt][0]
        # if last option selected --> turn on light
        if self.t_alarm == "off":
            self.pixels.fill((255, 255, 100))
            self.pixels.show()
        # if any other time is selected
        else:
            # signal set alarm time with different LED colors
            # yellow - 5:00; cyan - 6:00; pink - 6:30
            for i in [0, 5, 11, 16, 20, 25]:
                self.pixels[i] = self.list_alarm[self.cnt][1]
                self.pixels.show()
        # increment counter so the next button push sets next alarm in list
        self.cnt = self.cnt + 1
        # if button is pushed while last alarm in list is set, reset counter --> first alarm set again
        if self.cnt > 3:
            self.cnt = 0
        else:
            pass
        print("Alarm set to " + self.t_alarm)
        
    # method called when blue button is released
    # # turns off LEDs one second after blue button is released
    def button_confirm_alarm(self):
        #for i in [0, 6, 12, 18, 24]:
        #    self.pixels[i] = (0, 0, 0)
        if self.t_alarm == "off":
            self.pixels.fill((255, 255, 100))
        else:
            self.pixels.fill((0, 0, 0))
        time.sleep(1.5)
        self.pixels.show()
            
    # actual sunrise alarm methode
    # runs after init methode finishes
    # checks current time and set alarm time every 30 seconds
    # starts sunrise if both times match
    def run(self):
        print("running...")

        while True:
            try:

                # connect buttons to their callback methodes
                self.button_power.when_pressed = self.button_shutdown
                self.button_alarm.when_pressed = self.button_change_alarm
                self.button_alarm.when_released = self.button_confirm_alarm

                # get the current time
                t = time.localtime()
                
                # grab only time information (hh:mm)
                t_time = str(t[3]) + ":" + str(t[4])
                
                # if time equals set alarm time
                if t_time == self.t_alarm:
                    # start sunrise
                    print("Sun rises!")
                    for i in range(17, 501):
                        # calculate RGB values (quadratic functions)
                        pixel_r = round(0.005 * i ** 2)
                        pixel_g = round(0.0012 * i ** 2)
                        pixel_b = round(0.00013 * i ** 2)
                        # set limits for each RGB channel
                        if pixel_r > 255:
                            pixel_r = 255
                        if pixel_g > 90:
                            pixel_g = 90
                        if pixel_b > 15:
                            pixel_b = 15
                        # write Values to LEDs
                        self.pixels.fill((pixel_r, pixel_g, pixel_b))
                        self.pixels.show()
                        # wait so the sunrise lasts for excactly the duration set with "sunrise_speed"
                        time.sleep(self.sunrise_speed/484)
                    
                    # keep the sunlight for 25 minutes
                    time.sleep(1500)
                    
                    # after sunrise finishes, start shutdown routine (as if red button was pressed)
                    self.button_shutdown
                
                # if time doesn't equal alarm time
                #else:
                #    # turn off LEDs
                #    self.pixels.fill((0, 0, 0))
                #    self.pixels.show()
                
                # repeat checking the time every second
                time.sleep(30)
                
            # catch Keyboard Interrupt (Ctrl+C)
            except KeyboardInterrupt:
                # tunr off LEDs
                self.pixels.fill((0, 0, 0))
                self.pixels.show()
                # exit script
                break


if __name__ == '__main__':
    # run init methode
    alarm = piAlarm()
    # run alarm routine
    alarm.run()
