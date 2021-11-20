
# DSCOVR:EPIC Image Viewer

I'm testing this on a 2.1" Hyperpixel Round Touch display from Pimoroni, with a Raspberry Pi Zero W.

It currently checks the API for a new image every 15mins as it's in test. It doesn't need to be anywhere near this often, new images are every 2hrs at least.

## Running It
Still testing it. I'm making it run in the background, while populating a log file like this:

    python3 -u epic.py &> epic.log &


