from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone

from .models import Course, CourseSubscription, PaymentProof
from .forms import SubscriptionForm


def course_list(request):
    courses = Course.objects.filter(is_published=True)
    return render(request, 'courses/list.html', {'courses': courses})


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    subscription = None
    if request.user.is_authenticated:
        subscription = CourseSubscription.objects.filter(user=request.user, course=course).first()
    return render(request, 'courses/detail.html', {
        'course': course,
        'subscription': subscription,
    })


@login_required
def subscribe(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    existing = CourseSubscription.objects.filter(user=request.user, course=course).first()

    if existing and existing.status == 'approved':
        messages.info(request, 'أنت مشترك بالفعل في هذا الكورس.')
        return redirect('courses:learn', slug=slug)

    if existing and existing.status == 'pending':
        messages.info(request, 'طلب اشتراكك قيد المراجعة.')
        return redirect('courses:detail', slug=slug)

    if request.method == 'POST':
        form = SubscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            if existing:
                existing.status = 'pending'
                existing.save()
                subscription = existing
                if hasattr(subscription, 'payment_proof'):
                    subscription.payment_proof.delete()
            else:
                subscription = CourseSubscription.objects.create(
                    user=request.user,
                    course=course,
                    status='pending',
                )
            payment = form.save(commit=False)
            payment.subscription = subscription
            payment.save()
            messages.success(
                request,
                'تم استلام طلب الاشتراك بنجاح، سيتم مراجعة الدفع والتواصل معك عبر واتساب لتفعيل الكورس.',
            )
            return redirect('courses:detail', slug=slug)
    else:
        initial = {
            'full_name': request.user.full_name,
            'phone': request.user.phone,
        }
        form = SubscriptionForm(initial=initial)

    return render(request, 'courses/subscribe.html', {'course': course, 'form': form})


@login_required
def learn_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    subscription = CourseSubscription.objects.filter(
        user=request.user, course=course, status='approved'
    ).first()

    if not subscription and not request.user.is_staff:
        messages.error(request, 'يجب الاشتراك في الكورس أولاً.')
        return redirect('courses:detail', slug=slug)

    sections = course.sections.prefetch_related('lessons__files').all()
    return render(request, 'courses/learn.html', {
        'course': course,
        'sections': sections,
        'subscription': subscription,
    })


@login_required
def lesson_detail(request, slug, lesson_id):
    course = get_object_or_404(Course, slug=slug)
    subscription = CourseSubscription.objects.filter(
        user=request.user, course=course, status='approved'
    ).first()

    if not subscription and not request.user.is_staff:
        messages.error(request, 'يجب الاشتراك في الكورس أولاً.')
        return redirect('courses:detail', slug=slug)

    from .models import Lesson
    lesson = get_object_or_404(Lesson, id=lesson_id, section__course=course)
    return render(request, 'courses/lesson.html', {
        'course': course,
        'lesson': lesson,
    })
