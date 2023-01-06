
# DSCOVR:EPIC Image Viewer

This script looks for new images from the EPIC camera on NASA's DSCOVR satellite, and displays them on screen.

This is designed for a 2.1" Hyperpixel Round Touch display from Pimoroni, with a Raspberry Pi Zero W.

It displays each image for 20s then moves to the next one.

It currently checks the API for new images every 120 mins, but I think they only upload new images once a day, so it probably doesn't need to be this often.

This uses Python3 and pygame.

## Running It
1. Create the directory `mkdir ~pi/code/epic/`
1. Go into the directory `cd ~pi/code/epic/`
1. make sure `start-epic.sh` is executable (`chmod +x start-epic.sh`)
1. Copy the autostart file `cp epic.desktop ~pi/.config/autostart/`
1. Test you can run it `python3 -u epic.py &> epic.log`
	* If it doesn't work look in `~pi/code/epic/epic.log` for errors, and google them.
1. If the test works, kill it with CTRL+C
1. Reboot and hope it runs automatically `sudo reboot`


