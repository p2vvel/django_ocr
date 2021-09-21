from .models import ImageModel
from django import forms


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = "__all__"



rotate_options = (
    (0, "No rotation"),
    (90, "Rotate right"),
    (270, "Rotate left"),
    (180, "Upside down"),
)


class TransformationFrom(forms.Form):
    rotation = forms.ChoiceField(choices=rotate_options, label="Rotation", initial="0", widget=forms.RadioSelect)
    mirror_x = forms.BooleanField(label="Mirror X", initial=False, required=False)
    mirror_y = forms.BooleanField(label="Mirror Y", initial=False, required=False)