from django.urls import path, include
from .views import *


urlpatterns = [
    path('', homepage, name='homepage'),
    path('resume/', resume, name='resume'),
]