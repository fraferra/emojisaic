import subprocess
import os
import numpy
from PIL import Image, ImageFilter, ImageOps 
import urllib2
from random import randint
import io
STATIC_URL = 's3://emojimosaic/'

import tinys3

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}



def save2S3(path):
    conn = tinys3.Connection(os.environ['AWS_ACCESS_KEY_ID'],os.environ['AWS_SECRET_ACCESS_KEY'],tls=True,endpoint='s3-eu-west-1.amazonaws.com')  
    f = open(path,'rb')
    conn.upload('emojifiedimages/'+path, f, 'emojimosaic')




def distance(x, y):
    return (x[0] - y[0])**2+(x[1] - y[1])**2+(x[2] - y[2])**2

def resizeImage(image):
    original_sizes = numpy.asarray(image).shape
    ratio = float(original_sizes[1])/float(original_sizes[0])
    new_width = 1000
    new_height = int(round(ratio * new_width))
    image = numpy.asarray(image.resize((new_width, new_height), resample=Image.ANTIALIAS))
    return (new_width, new_height), image

# def resizeImage(image):
#     original_sizes = numpy.asarray(image).shape
#     ratio = float(original_sizes[1])/float(original_sizes[0])
#     if original_sizes[0]>original_sizes[1]:    
#         new_width = 1000
#         new_height = int(round(ratio * new_width))
#     else:
#         new_height = 1000
#         new_width = int(round(ratio * new_height))
#     image = numpy.asarray(image.resize((new_width, new_height), resample=Image.ANTIALIAS))
#     return (new_width, new_height), image



def modifyImage(path_original, dict_url_image, colorDict, granularity = 0.012, api = False):
    if api:
        req = urllib2.Request(path_original, headers=hdr)
        path_original_2 = io.BytesIO(urllib2.urlopen(req).read())
        m = Image.open(path_original_2).convert('RGB').filter(ImageFilter.MedianFilter(3))
        path_original = "static/images/" + path_original.split("/")[-1]
    else:
        m = Image.open(path_original).convert('RGB').filter(ImageFilter.MedianFilter(3))

    sizes, m = resizeImage(m)
    step_0 = int(round(sizes[0]*granularity))
    step_1 = int(round(sizes[1]*granularity))


    new_im = Image.new('RGB', (sizes[0],sizes[1]), color = (255, 255, 255))

    for row in range(0,sizes[0],step_0):
        for col in range(0,sizes[1],step_1):
            
            color = m[col, row]/4*4

            img = colorDict[tuple(color)]
            image_path = dict_url_image[img]

            emoji_image = Image.open(image_path).resize((int(round(step_0+step_0*0.15)),int(round(step_1+step_1*0.15))), resample=Image.ANTIALIAS)#.rotate(90)

            new_im.paste(emoji_image, (row,col))

    new_im.save(path_original, format="png")
    save2S3(path_original)
    return path_original


