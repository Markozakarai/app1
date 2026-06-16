from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('users/', views.users_list, name='users_list'),
    path('users/<int:pk>/toggle/', views.user_toggle, name='user_toggle'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('courses/', views.courses_list, name='courses_list'),
    path('courses/add/', views.course_create, name='course_create'),
    path('courses/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),
    path('courses/<int:pk>/sections/', views.course_sections, name='course_sections'),
    path('courses/<int:course_pk>/sections/add/', views.section_create, name='section_create'),
    path('sections/<int:pk>/delete/', views.section_delete, name='section_delete'),
    path('sections/<int:section_pk>/lessons/add/', views.lesson_create, name='lesson_create'),
    path('lessons/<int:pk>/edit/', views.lesson_edit, name='lesson_edit'),
    path('lessons/<int:pk>/delete/', views.lesson_delete, name='lesson_delete'),
    path('lessons/<int:lesson_pk>/files/add/', views.lesson_file_add, name='lesson_file_add'),
    path('subscriptions/', views.subscriptions_list, name='subscriptions_list'),
    path('subscriptions/<int:pk>/approve/', views.subscription_approve, name='subscription_approve'),
    path('subscriptions/<int:pk>/reject/', views.subscription_reject, name='subscription_reject'),
    path('certificates/', views.certificates_list, name='certificates_list'),
    path('certificates/add/', views.certificate_create, name='certificate_create'),
    path('certificates/<int:pk>/delete/', views.certificate_delete, name='certificate_delete'),
    path('contact-messages/', views.contact_messages_list, name='contact_messages'),
]
