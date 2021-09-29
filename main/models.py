from PIL.Image import Image
from django.db import models

# Create your models here.

import os
import uuid
from PIL import Image

#upload_to can be str or function that has 2 args:
# * instance (of model)
# * filename (original filename of uploaded file)
def uuid_name(instance, filename):
    extension = filename.split(".")[-1] if "." in filename else ""
    return "uploads/{uuid}.{ext}".format(uuid=str(uuid.uuid4()), ext=extension)


class ImageModel(models.Model):
    file = models.ImageField(upload_to=uuid_name)
    converted = models.BooleanField(default=False, null=False)
    original_image = models.ForeignKey(
        'self', on_delete=models.CASCADE, default=None,
        null=True)  #used for relating transformed pics to originals


    def get_PIL_Image(self) -> Image:
        '''Returns PIL Image created from the file attribute'''
        return Image.open(self.file.path)

    def mark_as_converted(self):
        '''Marks image and its parents as already used'''
        self.converted = True
        if self.original_image:
            self.original_image.converted = True

    def delete(self, *args, **kwargs):
        #tried doing it by os.path.exist(), but using exceptions might be
        # better idea(file might exist while checking its existence,
        # but be missed when trying to delete it)
        try:
            os.remove(self.file.path)
        except Exception as e:
            print(e)
        super().delete(*args, **kwargs)  #calling default delete handler
