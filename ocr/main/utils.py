from .forms import ImageForm, TransformationFrom
from django.shortcuts import redirect, render
from django.contrib import messages

from io import BytesIO
from django.core.files import File
from PIL import Image
import pytesseract
import uuid
from .models import ImageModel


def transform_image(img: Image, rotation, mirror_x, mirror_y, *args,
                    **kwargs) -> Image:
    '''Transforming image (rotating, flipping X and Y axis)'''
    if int(rotation) != 0:
        angle = int(rotation)
        img = img.rotate(
            360 - angle, expand=True
        )  #Image.rotate() rotates image counterclockwise (thats why 360-angle)
    if mirror_x:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    if mirror_y:
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    return img


def save_image(img: Image, parent: ImageModel = None) -> ImageModel:
    '''Saves PIL image using my data model with ImageField'''
    new_img = ImageModel.objects.create(original_image=parent)  #file model
    buffer = BytesIO()
    img.save(buffer, "PNG")  #saves PIL image into buffer
    new_img.file.save(str(uuid.uuid4()) + ".png",
                      File(buffer))  #saves image buffer on local disk
    return new_img


def problem_handler(func):
    '''Decorator written to help handling errors in preview and results views'''
    def wrapper(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except (KeyError, ImageModel.DoesNotExist):
            messages.warning(request, "Choose file!")
            return redirect("index")  #no image to ocr
        except Exception as e:
            print("ERROR: %s" % e)
            messages.error(request, "Unexpected Error :((")
            return redirect("index")

    return wrapper