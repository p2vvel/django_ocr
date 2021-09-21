from PIL.Image import Image
from django.db import models

# Create your models here.

import os
import uuid


#upload_to can be str or function that has 2 args:
# * instance (of model)
# * filename (original filename of uploaded file)
def uuid_name(instance, filename):
    extension = filename.split(".")[-1] if "." in filename else ""
    return "uploads/{uuid}.{ext}".format(uuid=str(uuid.uuid4()), ext=extension)


class ImageModel(models.Model):
    file = models.ImageField(upload_to=uuid_name)
    original_image = models.ForeignKey(
        'self', on_delete=models.DO_NOTHING, default=None,
        null=True)  #used for relating transformed pics to originals

    def delete(self, *args, **kwargs):
        #tried doing it by path.exist but read using exceptions might be
        # better idea(file might exist while checking its existence,
        # but be missed when trying to delete it)
        try:
            os.remove(self.file.path)
        except Exception as e:
            print(e)
        super().delete(*args, **kwargs)  #calling default delete handler
