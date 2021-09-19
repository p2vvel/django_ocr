from .forms import FileForm
from django.shortcuts import render

# Create your views here.

from .models import FileModel

def index_view(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("SAVED FILE")
    # else:
    files = FileModel.objects.all()
    context = {"form": FileForm(), "files": files}
    return render(request, "index.html", context)