from django.conf import settings
from django.db import models


class Conversation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversations')
    subject = models.CharField('الموضوع', max_length=255, default='محادثة عامة')
    is_closed = models.BooleanField('مغلقة', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'محادثة'
        verbose_name_plural = 'المحادثات'
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.user.full_name} - {self.subject}'

    def unread_count_for_user(self, user):
        if user.is_staff:
            return self.messages.filter(is_read=False, is_from_admin=False).count()
        return self.messages.filter(is_read=False, is_from_admin=True).count()


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField('المحتوى', blank=True)
    image = models.ImageField('صورة', upload_to='chat/', blank=True, null=True)
    is_from_admin = models.BooleanField('من الإدارة', default=False)
    is_read = models.BooleanField('مقروءة', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'رسالة'
        verbose_name_plural = 'الرسائل'
        ordering = ['created_at']

    def __str__(self):
        return f'رسالة من {self.sender.full_name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.conversation.save(update_fields=['updated_at'])


class ContactMessage(models.Model):
    name = models.CharField('الاسم', max_length=255)
    email = models.EmailField('البريد الإلكتروني')
    phone = models.CharField('رقم الهاتف', max_length=20, blank=True)
    subject = models.CharField('الموضوع', max_length=255)
    message = models.TextField('الرسالة')
    is_read = models.BooleanField('مقروءة', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'رسالة تواصل'
        verbose_name_plural = 'رسائل التواصل'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.subject}'
