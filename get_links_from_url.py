import  re
import  urllib2
import requests
from PIL import Image
from io import BytesIO


def print_list(list):
    for i,j in enumerate(list):
        print i,j

def get_base_url():
    url = raw_input('Enter the base URL :')
    data = urllib2.urlopen(url).read()
    print url, data
    return url, data

def get_hyperlinks(url, source):
    urlPat = re.compile(r'media.+medium1.+jpg')
    result = re.findall(urlPat, source)
    urlList = [a for a in result]
    return "ok"

def get_image_size(url):
    data = requests.get(url).content
    im = Image.open(BytesIO(data))
    return im.size



if  __name__  ==  '__main__':
    url, source = get_base_url()
    urlList = get_hyperlinks(url, source)
    width, height = get_image_size(url)
    print width, height
    print url, data
