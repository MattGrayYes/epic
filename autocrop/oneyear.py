import pygame
import glob
import os.path
import json
import datetime
import requests
import io
from urllib.request import urlopen
import time
import math

def get_epic_images_json(date = ""):
    # Call the epic api
    response = requests.get("https://epic.gsfc.nasa.gov/api/natural/date" + date)
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
        pygame.image.save(image, "./year/"+os.path.basename(imageurl))
        print("Downloaded {}".format(imageurl))
    print("photos saved")

urllist = []
for x in range(1,13):
    print(x)
    images = get_epic_images_json("/2022-{:02d}-10".format(x))
    urls = create_image_urls(images)
    urllist.append(urls[0])
    with open("year/2022-{:02d}-10.txt".format(x), 'w') as f:
        f.write(json.dumps(images[0], indent=4))
    x = images[0]['dscovr_j2000_position']['x']
    y = images[0]['dscovr_j2000_position']['y']
    z = images[0]['dscovr_j2000_position']['z']
    distance = math.sqrt((x*x)+(y*y)+(z*z))
    print("{};{}".format(images[0]['date'],distance))
    #print("{},{},{} = {}".format(x,y,z,distance))
#save_photos(urllist)