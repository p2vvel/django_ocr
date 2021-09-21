from functools import reduce
from django import http
from .forms import ImageForm, TransformationFrom
from django.shortcuts import redirect, render
from django.contrib import messages

from io import BytesIO
from django.core.files import File
from PIL import Image
import pytesseract
import uuid

# Create your views here.

from .models import ImageModel


def transform_image(img: Image, rotation, mirror_x, mirror_y) -> Image:
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


def index_view(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save()
            request.session["img_key"] = img.pk
            return redirect("preview")
    else:
        #removing info about previously converted images 
        # request.session.pop("img_key", None)    
        form = ImageForm()
    context = {"form": form}
    return render(request, "index.html", context)


def image_preview(request):
    try:
        if request.method == "POST":
            form = TransformationFrom(request.POST)
            if form.is_valid():
                img_model = ImageModel.objects.get(
                    pk=request.session["img_key"])
                img = img_model.get_PIL_Image()
                #transform image and save it
                new_img = transform_image(img, **form.cleaned_data)
                new_img_model = save_image(new_img, parent=img_model)
                request.session["img_key"] = new_img_model.pk
                return redirect("results")
        else:
            img = ImageModel.objects.get(pk=request.session["img_key"])
            context = {"image": img, "form": TransformationFrom()}
            return render(request, "preview.html", context)
    except (KeyError, ImageModel.DoesNotExist):
        messages.warning(request, "Choose file!")
        return redirect("index")    #no image to ocr
    except Exception as e:
        print("ERROR: %s" % e)
        messages.error(request, "Unexpected Error :((")
        return redirect("index")


def results(request):
    try:
        image_model = ImageModel.objects.get(pk=request.session["img_key"])
        image_model.mark_as_converted()
        image = image_model.get_PIL_Image()
        results = pytesseract.image_to_string(image)
        context = {"image": image_model, "results": results}
        return render(request, "results.html", context)
    except (KeyError, ImageModel.DoesNotExist):
        messages.warning(request, "Choose file!")
        return redirect("index")    #no image to ocr
    except Exception as e:
        print("ERROR: %s" % e)
        messages.error(request, "Unexpected Error :((")
        return redirect("index")