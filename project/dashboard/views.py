from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone

from courses.models import (
    Course, CourseSection, Lesson, LessonFile,
    CourseSubscription, Certificate, Testimonial,
)
from courses.forms import CourseForm, SectionForm, LessonForm, LessonFileForm, CertificateForm
from messaging.models import ContactMessage

User = get_user_model()


def staff_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            messages.error(request, 'غير مصرح لك بالوصول إلى لوحة التحكم.')
            return redirect('pages:home')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@staff_required
def dashboard_home(request):
    stats = {
        'users_count': User.objects.count(),
        'courses_count': Course.objects.count(),
        'pending_subscriptions': CourseSubscription.objects.filter(status='pending').count(),
        'contact_messages': ContactMessage.objects.filter(is_read=False).count(),
    }
    recent_subscriptions = CourseSubscription.objects.select_related('user', 'course')[:5]
    return render(request, 'dashboard/home.html', {
        'stats': stats,
        'recent_subscriptions': recent_subscriptions,
    })


# Users management
@login_required
@staff_required
def users_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/users/list.html', {'users': users})


@login_required
@staff_required
def user_toggle(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user != request.user:
        user.is_active_account = not user.is_active_account
        user.save(update_fields=['is_active_account'])
        status = 'تفعيل' if user.is_active_account else 'تعطيل'
        messages.success(request, f'تم {status} حساب {user.full_name}.')
    return redirect('dashboard:users_list')


@login_required
@staff_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user != request.user and not user.is_superuser:
        name = user.full_name
        user.delete()
        messages.success(request, f'تم حذف المستخدم {name}.')
    return redirect('dashboard:users_list')


# Courses management
@login_required
@staff_required
def courses_list(request):
    courses = Course.objects.all()
    return render(request, 'dashboard/courses/list.html', {'courses': courses})


@login_required
@staff_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إضافة الكورس بنجاح.')
            return redirect('dashboard:courses_list')
    else:
        form = CourseForm()
    return render(request, 'dashboard/courses/form.html', {'form': form, 'title': 'إضافة كورس'})


@login_required
@staff_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث الكورس بنجاح.')
            return redirect('dashboard:courses_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'dashboard/courses/form.html', {'form': form, 'title': 'تعديل كورس', 'course': course})


@login_required
@staff_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'تم حذف الكورس.')
    return redirect('dashboard:courses_list')


@login_required
@staff_required
def course_sections(request, pk):
    course = get_object_or_404(Course, pk=pk)
    sections = course.sections.prefetch_related('lessons').all()
    section_form = SectionForm()
    return render(request, 'dashboard/courses/sections.html', {
        'course': course,
        'sections': sections,
        'section_form': section_form,
    })


@login_required
@staff_required
def section_create(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.course = course
            section.save()
            messages.success(request, 'تم إضافة الأسبوع بنجاح.')
    return redirect('dashboard:course_sections', pk=course_pk)


@login_required
@staff_required
def section_delete(request, pk):
    section = get_object_or_404(CourseSection, pk=pk)
    course_pk = section.course.pk
    section.delete()
    messages.success(request, 'تم حذف الأسبوع.')
    return redirect('dashboard:course_sections', pk=course_pk)


@login_required
@staff_required
def lesson_create(request, section_pk):
    section = get_object_or_404(CourseSection, pk=section_pk)
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.section = section
            lesson.save()
            messages.success(request, 'تم إضافة الدرس بنجاح.')
            return redirect('dashboard:course_sections', pk=section.course.pk)
    else:
        form = LessonForm()
    return render(request, 'dashboard/courses/lesson_form.html', {
        'form': form,
        'section': section,
        'title': 'إضافة درس',
    })


@login_required
@staff_required
def lesson_edit(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث الدرس.')
            return redirect('dashboard:course_sections', pk=lesson.section.course.pk)
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'dashboard/courses/lesson_form.html', {
        'form': form,
        'section': lesson.section,
        'lesson': lesson,
        'title': 'تعديل درس',
    })


@login_required
@staff_required
def lesson_delete(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    course_pk = lesson.section.course.pk
    lesson.delete()
    messages.success(request, 'تم حذف الدرس.')
    return redirect('dashboard:course_sections', pk=course_pk)


@login_required
@staff_required
def lesson_file_add(request, lesson_pk):
    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    if request.method == 'POST':
        form = LessonFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.lesson = lesson
            f.save()
            messages.success(request, 'تم رفع الملف.')
    return redirect('dashboard:course_sections', pk=lesson.section.course.pk)


# Subscriptions
@login_required
@staff_required
def subscriptions_list(request):
    status = request.GET.get('status', '')
    subs = CourseSubscription.objects.select_related('user', 'course', 'payment_proof')
    if status:
        subs = subs.filter(status=status)
    return render(request, 'dashboard/subscriptions/list.html', {
        'subscriptions': subs,
        'current_status': status,
    })


@login_required
@staff_required
def subscription_approve(request, pk):
    sub = get_object_or_404(CourseSubscription, pk=pk)
    sub.status = 'approved'
    sub.approved_at = timezone.now()
    sub.save()
    messages.success(request, f'تم تفعيل اشتراك {sub.user.full_name} في {sub.course.title}.')
    return redirect('dashboard:subscriptions_list')


@login_required
@staff_required
def subscription_reject(request, pk):
    sub = get_object_or_404(CourseSubscription, pk=pk)
    sub.status = 'rejected'
    sub.save()
    messages.warning(request, f'تم رفض اشتراك {sub.user.full_name}.')
    return redirect('dashboard:subscriptions_list')


# Certificates
@login_required
@staff_required
def certificates_list(request):
    certificates = Certificate.objects.select_related('user', 'course').all()
    return render(request, 'dashboard/certificates/list.html', {'certificates': certificates})


@login_required
@staff_required
def certificate_create(request):
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم رفع الشهادة بنجاح.')
            return redirect('dashboard:certificates_list')
    else:
        form = CertificateForm()
    return render(request, 'dashboard/certificates/form.html', {'form': form, 'title': 'رفع شهادة'})


@login_required
@staff_required
def certificate_delete(request, pk):
    cert = get_object_or_404(Certificate, pk=pk)
    cert.delete()
    messages.success(request, 'تم حذف الشهادة.')
    return redirect('dashboard:certificates_list')


@login_required
@staff_required
def contact_messages_list(request):
    msgs = ContactMessage.objects.all()
    return render(request, 'dashboard/messages/contact.html', {'contact_messages': msgs})
