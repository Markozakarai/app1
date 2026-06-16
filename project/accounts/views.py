from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

from courses.models import CourseSubscription, Certificate
from .forms import RegisterForm, LoginForm, ProfileForm

User = get_user_model()


def register_view(request):
    if request.user.is_authenticated:
        return redirect('pages:home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'تم إنشاء حسابك بنجاح! مرحباً بك.')
            return redirect('pages:home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('pages:home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_active_account:
                messages.error(request, 'حسابك معطّل. يرجى التواصل مع الإدارة.')
                return render(request, 'accounts/login.html', {'form': form})
            login(request, user)
            messages.success(request, f'مرحباً {user.full_name}!')
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('pages:home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'تم تسجيل الخروج بنجاح.')
    return redirect('pages:home')


@login_required
def profile_view(request):
    from .models import Profile
    profile, _ = Profile.objects.get_or_create(user=request.user)

    subscriptions = CourseSubscription.objects.filter(user=request.user).select_related('course')
    certificates = Certificate.objects.filter(user=request.user).select_related('course')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث الملف الشخصي بنجاح.')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile, user=request.user)

    return render(request, 'accounts/profile.html', {
        'form': form,
        'subscriptions': subscriptions,
        'certificates': certificates,
    })
