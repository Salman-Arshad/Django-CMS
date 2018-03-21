from django.conf.urls import url,include
from django.contrib import admin
from . import views
from django.conf.urls import handler404,handler400


urlpatterns = [
    url(r'^$', views.post_list,name="list"),
    url(r'^ajax-posts/$', views.post_ajax,name='ajax'),
    url(r'^drafts/$',views.drafts,name="drafts"),
    url(r'^create/$', views.post_create),
    url(r'^(?P<slug>[\w-]+)/$', views.post_detail,name="detail"),
    url(r'^(?P<slug>[\w-]+)/edit$', views.post_update,name='update'),
    url(r'^(?P<slug>[\w-]+)/delete$', views.post_delete,name="delete"),


    #url(r'^user/',views.userAuth,name = "userauth")

]

