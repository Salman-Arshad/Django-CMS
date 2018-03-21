from django import forms
from  .models import Post
from pagedown.widgets import PagedownWidget
from django.core.validators import *
from django.utils import timezone
from bootstrap_datepicker.widgets import DatePicker


class PostForm(forms.ModelForm):
    publish = forms.DateField(widget=forms.SelectDateWidget)
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    draft = forms.BooleanField
    image = forms.FileField


    def clean_image(self):

        image = self.cleaned_data.get('image', False)
        if image:
            if image._size > 8 * 1024 * 1024:
                raise ValidationError("Image file too large ( > 4mb )")
            return image
        else:
            image ="#"
        return image


    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            'draft',
            'publish'

        ]