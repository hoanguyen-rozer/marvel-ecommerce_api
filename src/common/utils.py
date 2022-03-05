import os.path
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile


def generate_thumbnail(original_image, thumbnail_image):
    thumbnail_size = (128, 128)
    outfile = os.path.splitext(os.path.basename(original_image.name))[0] + '.thumbnail'
    try:
        with Image.open(original_image) as im:
            im.thumbnail(thumbnail_size)
            image_io = BytesIO()
            im.save(image_io, im.format)
            # im.save(outfile, im.format)
            filename = os.path.splitext(os.path.basename(original_image.name))[0] + '_thumbnail.' + im.format.lower()
            print('FILENAME: ', filename, type(im), im)
            thumbnail_image = ContentFile(image_io.getvalue(), filename)
    except IOError as e:
        print("Could not create a thumbnail for ", original_image)
        print(e)
