from django import forms
from .models import PaymentProof, CourseSubscription


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = PaymentProof
        fields = ['full_name', 'phone', 'proof_image', 'notes']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الاسم'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الهاتف'}),
            'proof_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'ملاحظات اختيارية'}),
        }
        labels = {
            'full_name': 'الاسم',
            'phone': 'رقم الهاتف',
            'proof_image': 'صورة إثبات الدفع',
            'notes': 'ملاحظات',
        }


class CourseForm(forms.ModelForm):
    class Meta:
        from .models import Course
        model = Course
        fields = [
            'title', 'slug', 'cover_image', 'short_description', 'full_description',
            'price', 'duration', 'skills', 'projects', 'is_published', 'is_featured',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'full_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'projects': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SectionForm(forms.ModelForm):
    class Meta:
        from .models import CourseSection
        model = CourseSection
        fields = ['title', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class LessonForm(forms.ModelForm):
    class Meta:
        from .models import Lesson
        model = Lesson
        fields = ['title', 'lesson_type', 'video', 'video_url', 'description', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'lesson_type': forms.Select(attrs={'class': 'form-select'}),
            'video': forms.FileInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class LessonFileForm(forms.ModelForm):
    class Meta:
        from .models import LessonFile
        model = LessonFile
        fields = ['title', 'file', 'file_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'file_type': forms.Select(attrs={'class': 'form-select'}),
        }


class CertificateForm(forms.ModelForm):
    class Meta:
        from .models import Certificate
        model = Certificate
        fields = ['user', 'course', 'file', 'completion_date', 'instructor_name']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'completion_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'instructor_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
