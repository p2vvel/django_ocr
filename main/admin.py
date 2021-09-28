from django.contrib import admin
from django.contrib.admin.decorators import display


# Register your models here.
from .models import ImageModel
from django.utils.html import format_html

class ImageModelAdmin(admin.ModelAdmin):
    def img_tag(self, obj):
        return  format_html("<img src=%s style='max-height: 200px; max-width: 100%%;'>" % obj.file.url)
    
    list_display = ("img_tag",)
    list_filter = (('original_image', admin.EmptyFieldListFilter),)

    # display = ("img_tag")
    readonly_fields = ("img_tag", )


admin.site.register(ImageModel, ImageModelAdmin)