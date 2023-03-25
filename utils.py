import urllib.request
import cv2
import numpy as np

from logger import logger

def phash(cv_image):
    # imgg = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY);
    imgg = cv_image
    h=cv2.img_hash.pHash(imgg) # 8-byte hash
    pH=int.from_bytes(h.tobytes(), byteorder='big', signed=True)
    return pH

def url2img(url):
    if '.gifv' in url:
      ret, frame = cv2.VideoCapture(url.replace('.gifv', '.mp4')).read()
      return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
    if '.gif' in url:
      ret, frame = cv2.VideoCapture(url).read()
      return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);

    req = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    # return cv2.imdecode(arr, -1)
    return cv2.imdecode(arr, 0)

def phash_from_url(url):
    try:
        img = url2img(url)
    except BaseException as err:
        logger.error(f'Error getting {url}: {err}')
        return
    return phash(img)
