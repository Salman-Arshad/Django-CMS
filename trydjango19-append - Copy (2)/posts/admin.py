from django.contrib import admin
from .models import Post
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ["id","title", "slug","content"]
    list_filter = ["title","updated","timestamp"]
    search_fields = ['title']

    class Meta:
        model = Post

admin.site.register(Post,PostAdmin)
