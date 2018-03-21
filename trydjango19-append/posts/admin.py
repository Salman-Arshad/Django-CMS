from django.contrib import admin
from .models import Post
from froala_editor.widgets import FroalaEditor
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ["id","title", "slug","content"]
    list_filter = ["title","updated","timestamp"]
    search_fields = ['title']
    formfield_overrides = {
        FroalaEditor: {'content':FroalaEditor}
    }

    class Meta:
        model = Post

admin.site.register(Post,PostAdmin)
