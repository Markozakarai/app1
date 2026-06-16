from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('about-instructor/', views.about_instructor, name='about_instructor'),
]
