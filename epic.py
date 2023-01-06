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

# Settings
check_delay = 120 #minutes
rotate_delay = 20 #seconds

# Set up the drawing window
screen = pygame.display.set_mode([480,480], pygame.FULLSCREEN)
pygame.mouse.set_visible(0)

# Fill the background with black
screen.fill((0,0,0))

# Display loading image
image = pygame.image.load(r"./loading.jpg")
screen.blit(image, (0,0))
pygame.display.flip()

print("Checking for new photos every "+str(check_delay)+" minutes")
print("Rotating photos every "+str(rotate_delay)+" seconds")

def get_epic_images_json():
    # Call the epic api
    response = requests.get("https://epic.gsfc.nasa.gov/api/natural")
    imjson = response.json()
    return imjson


def create_image_urls(photos):
    urls = []
    for photo in photos:
        dt = datetime.datetime.strptime(photo["date"], "%Y-%m-%d %H:%M:%S")
        imageurl = "https://epic.gsfc.nasa.gov/archive/natural/"+str(dt.year)+"/"+str(dt.month).zfill(2)+"/"+str(dt.day).zfill(2)+"/jpg/"+photo["image"]+".jpg"
        urls.append(imageurl)    
    return urls
    
    
def save_photos(imageurls):
    print("saving photos")
    counter=0
    for imageurl in imageurls:
        # Create a surface object, draw image on it..
        image_file = io.BytesIO(urlopen(imageurl).read())
        image = pygame.image.load(image_file)

        # Crop out the centre 830px square from the image to make globe fill screen
        cropped = pygame.Surface((830,830))
        cropped.blit(image,(0,0),(125,125,830,830))
        cropped = pygame.transform.scale(cropped, (480,480))

        pygame.image.save(cropped,"./"+str(counter)+".jpg")
        counter+=1
    print("photos saved")

def rotate_photos(num_photos, rotate_delay):
    counter=0
    while counter<num_photos:
        # First check if anyone's tried to quit the app while we've been rotating
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
        # Create a surface object and draw image on it.
        image = pygame.image.load(r"./"+str(counter)+".jpg")

        # Display image
        screen.blit(image, (0,0))
        pygame.display.flip()
        
        counter+=1
        
        # How many seconds to wait between changing images
        time.sleep(rotate_delay)

# Run until the user asks to quit
running = True
first_run = True
last_data = ""
newest_data = ""
last_check = datetime.datetime.now()-datetime.timedelta(hours=1)
num_photos = 0

while running:
    # Did anyone try to quit the app?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    # If we haven't checked for new images recently, check for new images
    if last_check < datetime.datetime.now()-datetime.timedelta(minutes=check_delay) or first_run == True:
        print(str(datetime.datetime.now())+" Checking for new images.")
        
        last_check = datetime.datetime.now()
    
        json = get_epic_images_json()
        newest_data=json[0]["date"]
    
        print("OLD: "+last_data)
        print("NEW: "+newest_data)
        
        # If there are new images available, download them, then quickly display them all.
        if last_data != newest_data:
            print("Ooh! New Images!")
            last_data = newest_data
            imageurls = create_image_urls(json)    
            save_photos(imageurls)
            num_photos = len(imageurls)
            rotate_photos(num_photos, 1)
        else:
            print("No new images")

    # Show each photo in order.
    rotate_photos(num_photos, rotate_delay)

# Done! Time to quit.
pygame.quit()


