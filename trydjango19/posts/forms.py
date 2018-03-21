from django import forms
from  .models import Post
from pagedown.widgets import PagedownWidget
from django.core.validators import *
from django.utils import timezone


class PostForm(forms.ModelForm):
    publish = forms.DateField(widget=forms.SelectDateWidget)
    content = forms.CharField(widget=PagedownWidget)
    draft = forms.BooleanField


    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            'draft',
            'publish'
        ]