from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, request
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote_plus
from django.utils import timezone


# Create your views here.


def post_create(request):
    if not request.user.is_staff and not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None,request.FILES or None )
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        if form.errors:
            messages.error(request,"Form not submitted",extra_tags="success")
        messages.success(request,"Form Submitted")
        return HttpResponseRedirect(instance.get_absolute_url())


    context = {
        "form":form
    }
    return render(request,"post_form.html",context)


def post_detail(request, slug):

    instance = get_object_or_404(Post,slug=slug)
    if instance.publish > timezone.now().date()or instance.draft:
        if not request.user.is_superuser and not request.user.is_staff:
            raise Http404
    context ={
        'title':instance.title,
        'instance':instance,

    }
    return render(request,"detail.html",context)


def post_list(request):
    ip = get_clientIp(request)
    page_var ="page"
    if request.user.is_superuser:
        queryset_list = Post.objects.all()
    else:
        queryset_list = Post.objects.active()
    paginator = Paginator(queryset_list, 7)  # Show 25 contacts per page

    page = request.GET.get(page_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset= paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        'object_list': queryset,
        'title':'List',
        'page_var': page_var,
        'ip':ip,
    }
    return render(request, "post_list.html",context)




def post_update(request,slug=None):

    if not request.user.is_authenticated():
        raise Http404
    if not request.user.is_superuser:
        if request.user.is_staff:
            instance = get_object_or_404(Post, slug=slug)
            if not instance.user == request.user:
                raise Http404
    instance = get_object_or_404(Post,slug=slug)
    form = PostForm(request.POST or None,request.FILES or None,instance=instance,)
    if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request,"post Updated")
            return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'title':instance.title,
        'instance':instance,
        'form':form,
    }
    return render(request,"post_form.html",context)




def post_delete(request ,slug):
    instance = get_object_or_404(Post,slug=slug)
    if not request.user.is_superuser:
        if not request.user == Post.user:
            raise Http404
    instance.delete()
    messages.success(request,"Post successfully deleted",extra_tags="warning")

def drafts(request):

    page_var = "page"
    if request.user.is_superuser:
        queryset_list = Post.objects.drafts()
    elif request.user.is_staff:
        queryset_list = Post.objects.filter(draft=True).filter(publish__gte=timezone.now().date()).filter(user=request.user)
    else:
        raise Http404
    paginator = Paginator(queryset_list, 7)  # Show 25 contacts per page

    page = request.GET.get(page_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        'object_list': queryset,
        'title': 'List',
        'page_var': page_var
    }
    return render(request, "post_list.html", context)


def error404(request):
    return render(request,"404.html",{})
def error400(request):
    return render(request,"500.html",{})


def get_clientIp(request):
    """get the client ip from the request
    """
    ip= request.META['REMOTE_ADDR']
    return ip