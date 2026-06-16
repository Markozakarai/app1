from django.shortcuts import render, redirect
from django.contrib import messages

from courses.models import Course, Testimonial
from messaging.forms import ContactForm


def home(request):
    latest_courses = Course.objects.filter(is_published=True)[:6]
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    contact_form = ContactForm()
    return render(request, 'pages/home.html', {
        'latest_courses': latest_courses,
        'testimonials': testimonials,
        'contact_form': contact_form,
    })


def about_instructor(request):
    return render(request, 'pages/about_instructor.html')
