from django import forms
from django.core.exceptions import ValidationError

from .models import Message, ContactMessage


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'image']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'wa-text-input',
                'placeholder': 'اكتب رسالة...',
                'autocomplete': 'off',
            }),
            'image': forms.FileInput(attrs={
                'class': 'd-none',
                'accept': 'image/*',
                'id': 'chat-image-input',
            }),
        }

    def clean(self):
        cleaned = super().clean()
        content = (cleaned.get('content') or '').strip()
        image = cleaned.get('image')
        if not content and not image:
            raise ValidationError('اكتب رسالة أو أرفق صورة.')
        cleaned['content'] = content
        return cleaned


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الاسم'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الهاتف'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الموضوع'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'رسالتك'}),
        }
