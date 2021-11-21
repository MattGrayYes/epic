
# DSCOVR:EPIC Image Viewer
This is not complete.

I'm testing this on a 2.1" Hyperpixel Round Touch display from Pimoroni, with a Raspberry Pi Zero W.

It displays each image for 10s then moves to the next one.

It currently checks the API for new images every 30 mins as it's in test. It doesn't need to be anywhere near this often, as I think they only upload new images once a day.

## Running It
Still testing it. I'm making it run in the background, while populating a log file like this:

    python3 -u epic.py &> epic.log &


