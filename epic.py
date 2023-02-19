import pygame
import glob
import os.path
import json
import datetime
import requests
import io
from urllib.request import urlopen
import time

# Settings!
# This is how many images to keep cached
imageCount = 12

# This sets an age threshold for deletetion (curernt not used)
ageThreshold = datetime.timedelta(hours=36)

# This is the delay between api calls
check_delay = datetime.timedelta(hours=2)

# This is the delay rotating the slowhow
rotateTime = datetime.timedelta(seconds=20)

# This is how fast the loop runs 
# and thus how much cpu is used
# fadeTime in seconds
frameRate = 15
fadeTime = 1.0

# Crop the image?
# There some space around the earth, crop this? (pun intended)
# Apparently the sattelite moves a bit 
# since the crop settings from Matt Gray took of the edges
# The original is 1080p, cropSize should be smaller (and an even number)
cropping = True
cropSize = 916

# Constants, don't change these
scanpath = r'data/*.jpg'
if not os.path.exists('./data'):
    os.makedirs('./data')

# Setup PyGame, if a file "debug" exists run it windowed
os.environ["DISPLAY"] = ":0"
pygame.init()
if(os.path.isfile("debug")):
    window = pygame.display.set_mode((480, 480))
else:
    window = pygame.display.set_mode((480, 480), pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.mouse.set_visible(0)

# Load background surface
background = pygame.Surface(window.get_size())
background = pygame.image.load("loading.jpg").convert()

# Load foreground surface
image = pygame.Surface(window.get_size(), pygame.SRCALPHA)
image = pygame.image.load("loading.jpg").convert()
image.set_alpha(0)

window.blit(background, (0, 0))
pygame.display.flip()

def blitFadeIn(target, image, pos, step=2):
    alpha = image.get_alpha()
    alpha = min(255, alpha + step)
    image.set_alpha(alpha)
    target.blit(image, pos)
    return alpha == 255

def blitFadeOut(target, image, pos, step=2):
    alpha = image.get_alpha()
    alpha = max(0, alpha - step)
    image.set_alpha(alpha)
    target.blit(image, pos)
    return alpha == 0

def get_epic_images_json():
    # Call the epic api
    response = requests.get("https://epic.gsfc.nasa.gov/api/natural")
    imjson = response.json()
    return imjson

def save_photos(imageurls):
    print("saving photos")
    counter=0
    for imageurl in imageurls:
        # Create a surface object, draw image on it..
        image_file = io.BytesIO(urlopen(imageurl).read())
        image = pygame.image.load(image_file)

        if(cropping):
            # The original is 1080 square, crop to size
            w = cropSize
            cropped = pygame.Surface((w,w))
            cropped.blit(image,(0,0),((1080-w)/2,(1080-w)/2,w,w))
            image = pygame.transform.scale(cropped, (480,480))

        pygame.image.save(image, "./data/"+os.path.basename(imageurl))
        print("Downloaded {}".format(imageurl))
    print("photos saved")

def create_image_urls(photos):
    urls = []
    for photo in photos:
        dt = datetime.datetime.strptime(photo["date"], "%Y-%m-%d %H:%M:%S")
        imageurl = "https://epic.gsfc.nasa.gov/archive/natural/"+str(dt.year)+"/"+str(dt.month).zfill(2)+"/"+str(dt.day).zfill(2)+"/jpg/"+photo["image"]+".jpg"
        urls.append(imageurl)    
    return urls

def find_and_download_new_images():
    # Find images   
    # absolute path to search all text files inside a specific folder
    files = glob.glob(scanpath)
    basefilenames = []
    for f in files:
        basefilenames.append(os.path.basename(f))
    print(files)

    # Check for new images
    json = get_epic_images_json()
    imageurls = create_image_urls(json)
    newimageurls = []
    for url in imageurls:
        if(os.path.basename(url) not in basefilenames):
            newimageurls.append(url)
    save_photos(newimageurls)
    # Update scan list
    files = glob.glob(scanpath)

def delete_old_images():
    files = sorted(glob.glob(scanpath))
    count = len(files)
    if(count > imageCount):
        print("More than {} images, cleaning the oldest".format(imageCount))
        for file in files:
            f = os.path.splitext(os.path.basename(file))[0]
            stamp = str(f.split('_')[-1])
            # 20230218203420
            # this bit of code makes it possible to delete by date instead of numbers
            # curerntly not used
            date = datetime.datetime.strptime(stamp, '%Y%m%d%H%M%S')
            if date < datetime.datetime.now()-ageThreshold:
                print("{} old: {}".format(date,f))
            else:
                print("{} not: {}".format(date,f))
            print("Delete: {}".format(file))
            os.remove(file)
            count = count - 1
            if(count <= imageCount):
                print("Deleted enough")
                break;
    else:
        print("Less then {} images, skipping deletions".format(imageCount))

def selectNewImage(currentIndex):
    files = sorted(glob.glob(scanpath))
    currentIndex = currentIndex + 1
    if(currentIndex > len(files)-1):
        currentIndex = 0                
    return files[currentIndex],currentIndex

find_and_download_new_images()
delete_old_images()

# Read the last image count and the last time we checked api from file
try:
    with open("lastCheck","r") as file: 
        last_check = datetime.datetime.strptime(file.read(), "%d-%b-%Y (%H:%M:%S.%f)")
    print("last check from file {}".format(last_check))
except:
    last_check = datetime.datetime.now()-check_delay

# Loop
fadeStep = 255/frameRate/fadeTime
showImage = False
imageShown = False
lastRotation = datetime.datetime.now()
manual = False
currentIndex = 0
run = True
while run:
    clock.tick(frameRate)
    # Handle exit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            if(done):
                manual = True

    # Fading
    window.blit(background, (0, 0))
    if showImage:
        done = blitFadeIn(window, image, (0, 0), fadeStep)
        if done:
            imageShown = True
    if not showImage:
        done = blitFadeOut(window, image, (0, 0), fadeStep)
        if done:
            imageShown = False
    pygame.display.flip()
    
    # Scan new images
    if last_check < datetime.datetime.now()-check_delay:
        print("Checking for new images {}".format(str(datetime.datetime.now())))
        last_check = datetime.datetime.now()
        with open("lastCheck","w") as file: 
            file.write(datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"))

        find_and_download_new_images()
        delete_old_images()

    # Rotate images
    if(lastRotation < datetime.datetime.now()-rotateTime or manual):
        manual = False
        lastRotation = datetime.datetime.now()
        fileName,currentIndex = selectNewImage(currentIndex)
        if(done and imageShown):
            # Replace background
            background = pygame.image.load(fileName).convert()
            background = pygame.transform.scale(background, (480,480))
        if(done and not imageShown):
            # Replace image 
            image = pygame.image.load(fileName).convert() 
            image = pygame.transform.scale(image, (480,480))
            image.set_alpha(0)
        if showImage:
            showImage = False
        else:
            showImage = True

pygame.quit()
exit()