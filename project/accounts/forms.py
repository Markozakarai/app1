from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='كلمة المرور',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'كلمة المرور'}),
    )
    password_confirm = forms.CharField(
        label='تأكيد كلمة المرور',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تأكيد كلمة المرور'}),
    )

    class Meta:
        model = User
        fields = ['full_name', 'phone', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الاسم بالكامل'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الهاتف'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('password_confirm'):
            raise forms.ValidationError('كلمتا المرور غير متطابقتين')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='البريد الإلكتروني',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}),
    )
    password = forms.CharField(
        label='كلمة المرور',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'كلمة المرور'}),
    )


class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(label='الاسم', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='البريد الإلكتروني', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='رقم الهاتف', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['avatar']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['full_name'].initial = self.user.full_name
        self.fields['email'].initial = self.user.email
        self.fields['phone'].initial = self.user.phone
        # إخفاء input الأصلي لأن بعض المتصفحات تُظهر معاينة كبيرة داخل الـ input.
        # سنستخدم زر/معاينة مخصصة في القالب.
        self.fields['avatar'].widget.attrs.update({
            'class': 'd-none',
            'accept': 'image/*',
            'id': 'avatarInput',
        })

    def save(self, commit=True):
        profile = super().save(commit=False)
        self.user.full_name = self.cleaned_data['full_name']
        self.user.email = self.cleaned_data['email']
        self.user.phone = self.cleaned_data['phone']
        self.user.save()
        profile.user = self.user
        if commit:
            profile.save()
        return profile
