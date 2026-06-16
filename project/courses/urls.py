from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='list'),
    # استخدام str بدلاً من slug لدعم الـ slugs العربية (Unicode).
    path('<str:slug>/', views.course_detail, name='detail'),
    path('<str:slug>/subscribe/', views.subscribe, name='subscribe'),
    path('<str:slug>/learn/', views.learn_course, name='learn'),
    path('<str:slug>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson'),
]
