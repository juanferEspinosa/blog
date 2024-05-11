from django.shortcuts import render, reverse
from blog.models import Post



def homepage(request):
    posts = Post.objects.all()
    return render(request, 'homepage.html', context={'posts':posts})



def resume(request):
    return render(request, 'resume.html')