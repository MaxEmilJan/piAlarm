## required

After the raspberry pi got set up with the raspbian os you should run the following commands:

1. remove libreoffice and the preinstalled numpy version, since it consumes a lot of memory and is not needed for this application.
~~~
sudo apt-get purge libreoffice*
sudo apt remove python-numpy
sudo apt-get clean
~~~
2. update and upgrade the system (may take about 10 minutes)
~~~
sudo apt-get update && sudo apt-get upgrade
~~~
3. install the newest version of pip
~~~
sudo apt-get install python3-pip
sudo pip3 install --upgrade setuptools
~~~
4. install "venv" to create a virtual environment for your project
~~~
sudo apt-get install python3-venv
~~~
5. create a virtual env
~~~
python3.9 -m venv <name_of_your_env>
~~~
6. verify the correct python version
~~~
cd <name_of_your_env>
cat pyvenv.cfg
~~~
7. activate the env
~~~
source bin/activate
~~~
8. install circuitpython libraries
~~~
sudo pip install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python raspi-blinka.py
~~~
9. install driver for the neopixel led
~~~
pip install adafruit-circuitpython-neopixel
~~~
10. open terminal and type
~~~
sudo nano /etc/rc.local
~~~
11. enter following command before the "exit 0" line. this will make the startup.py file to run on boot. also it will turn of the power led of the pi
~~~
sudo sh -c 'echo none > /sys/class/leds/led0/trigger'
sudo sh -c 'echo none > /sys/class/leds/led1/trigger'
sudo sh -c 'echo 0 > /sys/class/leds/led0/brightness'
sudo sh -c 'echo 0 > /sys/class/leds/led1/brightness'

sudo python /home/pi/<...your_folders...>/startup.py
~~~
12. hit CTRL+X
13. enter
~~~
sudo reboot
~~~
---
