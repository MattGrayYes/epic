import json
import datetime
import requests
import io
from urllib.request import urlopen
import time

import pygame
pygame.init()

import os
os.environ["DISPLAY"] = ":0"
pygame.display.init()

# Set up the drawing window
screen = pygame.display.set_mode([480,480], pygame.FULLSCREEN)
pygame.mouse.set_visible(0)

# Fill the background with black
screen.fill((0,0,0))


def get_epic_image():
    # Call the epic api
    response = requests.get("https://epic.gsfc.nasa.gov/api/natural")
    # Get the last photo in the list (most recent)
    photo = response.json()[-1]
    # Get the date of the photo to construct the url
    dt = datetime.datetime.strptime(photo["date"], "%Y-%m-%d %H:%M:%S")

    imageurl = "https://epic.gsfc.nasa.gov/archive/natural/"+str(dt.year)+"/"+str(dt.month)+"/"+str(dt.day)+"/jpg/"+photo["image"]+".jpg"

    return imageurl




# Run until the user asks to quit
running = True
lasturl = ""

while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    print(datetime.datetime.now())
    print("Checking for new image.")
    imageurl = get_epic_image()
    
    print("OLD: "+lasturl)
    print("NEW: "+imageurl)
        
    if imageurl != lasturl:
        print("OOH New Image!")
        lasturl = imageurl
        # create a surface object, image is drawn on it.
        image_file = io.BytesIO(urlopen(imageurl).read())
        image = pygame.image.load(image_file)
        
        # Crop out the centre 830px square from the image to make globe fill screen
        cropped = pygame.Surface((830,830))
        cropped.blit(image,(0,0),(125,125,830,830))
        cropped = pygame.transform.scale(cropped, (480,480))
        
        # Display cropped image
        screen.blit(cropped, (0,0))
        pygame.display.flip()
        
    else:
        print("No new image.")
           
    # Sleep for 15mins
    print("sleeping")
    time.sleep(900)

# Done! Time to quit.
pygame.quit()


