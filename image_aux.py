import imghdr
import os
from PIL import Image
import urllib2 as urllib
import io
import cStringIO


class ImageAux:

    def __init__(self, image_url):
        response = urllib.urlopen(image_url)
        response_data = response.read()

        image_file = io.BytesIO(response_data)
        self.img = Image.open(image_file)

        data = cStringIO.StringIO(response_data)
        self.img_ext = imghdr.what(data)

    def crop_image(self, image_number, target_image_name):

        image_copy = self.img

        if image_number == 1:
            img = image_copy.crop((0, 0, 100, 100))
        elif image_number == 2:
            img = image_copy.crop((100, 0, 200, 100))
        elif image_number == 3:
            img = image_copy.crop((200, 0, 300, 100))
        elif image_number == 4:
            img = image_copy.crop((0, 100, 100, 200))
        elif image_number == 5:
            img = image_copy.crop((100, 100, 200, 200))
        elif image_number == 6:
            img = image_copy.crop((200, 100, 300, 200))
        elif image_number == 7:
            img = image_copy.crop((0, 200, 100, 300))
        elif image_number == 8:
            img = image_copy.crop((100, 200, 200, 300))
        elif image_number == 9:
            img = image_copy.crop((200, 200, 300, 300))
        else:
            raise Exception('Image number %s is invalid!\n' % image_number)

        img.save(target_image_name + "." + self.img_ext)

    def generate_images(self):

        if not os.path.exists("temp"):
            os.makedirs("temp")

        self.crop_image(1, "temp/image1")
        self.crop_image(2, "temp/image2")
        self.crop_image(3, "temp/image3")
        self.crop_image(4, "temp/image4")
        self.crop_image(5, "temp/image5")
        self.crop_image(6, "temp/image6")
        self.crop_image(7, "temp/image7")
        self.crop_image(8, "temp/image8")
        self.crop_image(9, "temp/image9")

    def get_image(self, image_number):
        return open('temp/image%s.%s' % (image_number, self.img_ext)), 'image%s.%s' % (image_number, self.img_ext)

