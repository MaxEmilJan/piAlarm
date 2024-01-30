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
---
