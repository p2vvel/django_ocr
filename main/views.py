from django import http
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from .forms import FileForm
from django.shortcuts import redirect, render


from PIL import Image
import pytesseract

# Create your views here.

from .models import FileModel

def index_view(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            x = form.save()
            # print("SAVED FILE: %s" % request.FILES["file"])
            # print("SAVED: %s" % x)
            request.session["uploaded_image"] = x.pk
            print(x.pk)
            return redirect("results")
    # else:
    files = FileModel.objects.all()
    context = {"form": FileForm(), "files": files}
    return render(request, "index.html", context)


def convert_image_to_text(request):
    try:
        image = FileModel.objects.get(pk=request.session.get("uploaded_image")) #fetching last picture
        del request.session["uploaded_image"]
        img = Image.open(image.file)
        result = pytesseract.image_to_string(img)
        # return HttpResponse(image.pk)
        return HttpResponse(result)
    except Exception as e:
        return redirect("index")
        # return HttpResponse("Bye")