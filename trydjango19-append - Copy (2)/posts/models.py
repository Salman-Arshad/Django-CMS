from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
import uuid
from markdown_deux import markdown
from django.utils.safestring import mark_safe
from django.core.validators import *


# Create your models here.
# MVC
class PostManager(models.Manager):
    def active(self,*args,**kwargs):
        return super(PostManager,self).filter(draft=False).filter(publish__lte = timezone.now())
    def drafts(self):
        return super(PostManager,self).filter(draft=True).filter(publish__gte=timezone.now())
def upload_location(instance,filename):
    print("%s/%s"%(instance.slug,filename))
    return "%s/%s"%(instance.slug,filename)

class Post(models.Model):
    #uuid = models.UUIDField(default=uuid.uuid4,editable=False,unique=True) this field gives a unique id id but iam usinh slugs vecause it is giving migration error
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False,auto_now_add=False,default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to=upload_location,
                              null=True,blank=True,
                              width_field="width_field",
                              height_field="height_field",

                              )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)
    objects = PostManager()

    def __str__(self):
        return self.slug

    def clean_fields(self,*args,**kwargs):
        if self.draft is True :
            if self.publish <timezone.now().date():
                raise ValidationError({'publish': ["Must be louder!", ]})

    def get_absolute_url(self):
        #print("hhahahahahahhahahhahahahaha")
        return reverse("posts:detail",kwargs={"slug":self.slug})

    class Meta: # this will display ecent posts first
        ordering = ["-timestamp", "-updated"]

# def create_slug(instance,buffer=0,new_slug=None):
#     slug = slugify(instance.title)  #SlugTesting
#     s = slugify(instance.title)
#     if new_slug is not None:
#         slug = new_slug  #SlugTesting
#         if (buffer>0):
#             slug = "%s-%s"%(slug,buffer)
#
#     qs = Post.objects.filter(slug=slug).order_by("-id")
#     exits=qs.exists()
#     if exits:
#         buffer+=1
#         return create_slug(instance,buffer,new_slug=s)
#     return slug

    def get_markdown(self):
        content = self.content
        md =  markdown(content)
        return mark_safe(md)


def create_slug(instance):
    buffer=1
    slug = slugify(instance.title)
    qs = Post.objects.filter(slug=slug).order_by("-id")
    if qs.exists():

        while True:
            s=slug
            s="%s-%s"%(s,buffer)
            qs = Post.objects.filter(slug=s).order_by("-id")
            if  not qs.exists():
                return s
            buffer+=1
    return slug



def pre_post_save_reciever(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_post_save_reciever,sender=Post)