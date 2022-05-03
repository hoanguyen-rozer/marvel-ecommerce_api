import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models


class CoreModel(models.Model):
    """
    Abstract class contain common fields about time
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Attachment(CoreModel):
    """
    Class contain common fields of media files, specifically images
    """
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True)
    original = models.ImageField(upload_to='originals/')

    def save(self, *args, **kwargs):
        self.generate_thumbnail()
        super(Attachment, self).save(*args, **kwargs)

    def generate_thumbnail(self):
        """
        Generate thumbnail file with size 128x128
        """
        thumbnail_size = (128, 128)
        outfile = os.path.splitext(os.path.basename(self.original.name))[0] + '.thumbnail'
        try:
            # Read image
            with Image.open(self.original) as im:
                im.thumbnail(thumbnail_size)
                image_io = BytesIO()
                im.save(image_io, im.format)
                # im.save(outfile, im.format)

                # Create thumbnail filename by way add '_thumbnail' suffix to original filename
                filename = os.path.splitext(os.path.basename(self.original.name))[0] + '_thumbnail.' + im.format.lower()
                # Set thumbnail attribute with ContentFile
                self.thumbnail = ContentFile(image_io.getvalue(), filename)
        except IOError as e:
            print("Could not create a thumbnail for ", self.original)
            print(e)


class Location(models.Model):
    """
    Generic class contain fields about location in map
    """
    lat = models.FloatField()
    lng = models.FloatField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip = models.CharField(max_length=10)
