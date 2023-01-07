
# DSCOVR:EPIC Image Viewer

This script looks for new [images from the Earth Polychromatic Imaging Camera](https://epic.gsfc.nasa.gov/) on NASA's [Deep Space Climate Observatory](https://www.nesdis.noaa.gov/current-satellite-missions/currently-flying/dscovr-deep-space-climate-observatory) satellite, and displays them on screen.

This is designed for a [2.1" Hyperpixel Round Touch display from Pimoroni](https://shop.pimoroni.com/products/hyperpixel-round), with a [Raspberry Pi Zero W](https://www.raspberrypi.com/products/raspberry-pi-zero-w/).

It displays each image for 20s then moves to the next one.

It currently checks the [EPIC "Blue Marble" API](https://epic.gsfc.nasa.gov/about/api) for new images every 120 mins, but I think they only upload new images once a day, so it probably doesn't need to be this often.

This is programmed using Python3 and PyGame.

# Running It
I've been fiddling with this for over a year now, so I've never followed these instructions in order. They're more of a guessed guideline.

## Raspberry Pi Setup
I'll assume you've already followed Pimoroni's instructions for getting the Hyperpixel Round screen going.

1. Use the terminal or log in as pi via ssh.
1. Create the directory `mkdir ~pi/code/epic/`
1. Go into the directory `cd ~pi/code/epic/`
1. Copy the code from this repository in
	* `git clone https://github.com/MattGrayYes/epic.git .`
1. make sure `start-epic.sh` is executable (`chmod +x start-epic.sh`)
1. Copy the autostart file `cp epic.desktop ~pi/.config/autostart/`
1. Install any python requirements `pip3 install -r requirements.txt`
1. Test you can run it `./start-epic.sh`
	* If that doesn't work, test you can run it directly `python3 -u epic.py`
	* If it still doesn't work check the output for errors, and google them.
1. If the test works, kill it with CTRL+C
1. Reboot and hope it runs automatically `sudo reboot`


