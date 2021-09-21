from django import http
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from .forms import ImageForm, TransformationFrom
from django.shortcuts import redirect, render

from io import BytesIO
from django.core.files import File

from PIL import Image
import pytesseract
import uuid

# Create your views here.

from .models import ImageModel


def index_view(request):

    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save()
            request.session["img_key"] = img.pk
            return redirect("preview")
    else:
        form = ImageForm()

    context = {"form": form}
    return render(request, "index.html", context)


def image_preview(request):
    img = ImageModel.objects.get(pk=request.session.get("img_key"))
    context = {"image": img, "form": TransformationFrom()}
    return render(request, "preview.html", context)


def save_image(img: Image, parent: ImageModel = None) -> ImageModel:
    '''Saves PIL image using my data model with ImageField'''
    new_img = ImageModel.objects.create(original_image=parent)  #file model
    buffer = BytesIO()
    img.save(buffer, "PNG")  #saves PIL image into buffer
    new_img.file.save(str(uuid.uuid4()) + ".png",
                      File(buffer))  #saves image buffer on local disk
    return new_img


def convert_image_to_text(request):
    if request.method == "POST":
        form = ImageForm(request.POST)
        if form.is_valid():
            form.save()
            x = form.cleaned_data()
        return render(request, "results.html")
    else:
        return redirect(request, "index")