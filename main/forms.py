from .models import FileModel
from django import forms


class FileForm(forms.ModelForm):
    
    class Meta:
        model = FileModel
        fields = "__all__"
    # file = forms.FileField()