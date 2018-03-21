from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from posts.models import Post
from django.db.models.signals import pre_save,pre_delete
from froala_editor.fields import FroalaField
# Create your models here.


class Comment(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
    #post        = models.ForeignKey(Post)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    content     = models.TextField()
    timestamp   = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)
def pre_comment_save_reciever(sender,instance ,*args,**kwargs):
        data = instance.content_object
        data.comments+=1
        data.save()

def pre_commment_delete_reciever(sender,instance,*args,**kwargs) :
    data = instance.content_object
    if data.comments is not 0:
        data.comments-=1
    data.save()

pre_save.connect(pre_comment_save_reciever,sender=Comment)
pre_delete.connect(pre_commment_delete_reciever,sender=Comment)


