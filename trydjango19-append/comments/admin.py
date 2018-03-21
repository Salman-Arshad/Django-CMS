from django.contrib import admin
from .models import Comment
# Register your models here.
class Commentadmin(admin.ModelAdmin):
    list_display = ['object_id','content_object','content','user']
    search_fields = ['user']

admin.site.register(Comment,Commentadmin)