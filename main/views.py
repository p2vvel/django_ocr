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

from .utils import transform_image, save_image, problem_handler


def index_view(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save()
            request.session["uploaded_img_key"] = img.pk
            return redirect("preview")
    elif request.method == "GET":
        #removing info about previously converted images
        request.session.pop("uploaded_img_key", None)
        request.session.pop("result_img_key", None)
        form = ImageForm()
    context = {"form": form}
    return render(request, "index.html", context)


def show_preview_page(request):
    '''Renders preview page that allows user for simple transforming image before OCRing it'''
    img = ImageModel.objects.get(pk=request.session["uploaded_img_key"])

    #creating rotated img, because ive lost whole day trying to rotate it properly without destroying layout :((((
    temp = Image.open(img.file.path)
    temp = temp.rotate(-90, expand=True)
    rotated_image = save_image(temp, parent=img)
    # rotated_image = None

    context = {
        "image": img,
        "form": TransformationFrom(),
        "rotated_image": rotated_image
    }

    return render(request, "preview.html", context)


def process_image_transformation(request):
    '''Takes care of validating users transforation input and sends transformated img to result page that later OCR it'''
    form = TransformationFrom(request.POST)
    if form.is_valid():
        img_model = ImageModel.objects.get(
            pk=request.session["uploaded_img_key"])
        img = img_model.get_PIL_Image()

        #transform image and save it
        new_img = transform_image(img, **form.cleaned_data)
        new_img_model = save_image(new_img, parent=img_model)

        request.session["chosen_language"] = form.cleaned_data["language"]

        request.session["result_img_key"] = new_img_model.pk
        return redirect("results")


@problem_handler
def image_preview(request):
    if request.method == "POST":
        return process_image_transformation(request)
    elif request.method == "GET":
        return show_preview_page(request)


@problem_handler
def results(request):
    chosen_language = request.session.get("chosen_language", "eng")
    image_model = ImageModel.objects.get(pk=request.session["result_img_key"])

    image_model.mark_as_converted()
    image = image_model.get_PIL_Image()
    results = pytesseract.image_to_string(image, lang=chosen_language)

    context = {"image": image_model, "results": results}
    return render(request, "results.html", context)