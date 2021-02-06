Simple text display on an 8x8 Neopixel compatible display, driven from a raspberry pi. I'm using an 8x8 array and a Raspberry Pi Zero W.

The font I'm using is

Setup:

1. Run through the Neopixel setup at https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage to connect and install the neopixel libraries on the Pi.
1. Install and configure nginx (basic config provided)
1. Run the flask app on the Pi
  * I've included my deploy.sh, will need some tweaking if you want to use it
  * It's best to run it using uwsgi, as a service (service file provided), and then enable that service, which will ensure the service starts up with the pi on boot
  * Remember to install/run everything as root

`PxPlus_IBM_BIOS.ttf` is from [VilR's Oldschool PC Font Resource](https://int10h.org/oldschool-pc-fonts) and is [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.ast) licensed.
