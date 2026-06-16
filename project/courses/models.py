from django.conf import settings
from django.db import models
from django.urls import reverse


class Course(models.Model):
    title = models.CharField('اسم الكورس', max_length=255)
    slug = models.SlugField(unique=True, allow_unicode=True)
    cover_image = models.ImageField('صورة الغلاف', upload_to='courses/covers/')
    short_description = models.TextField('وصف مختصر')
    full_description = models.TextField('وصف كامل')
    price = models.DecimalField('السعر', max_digits=10, decimal_places=2)
    duration = models.CharField('مدة الكورس', max_length=100)
    lesson_count = models.PositiveIntegerField('عدد الدروس', default=0)
    skills = models.TextField('المهارات', help_text='افصل بين المهارات بفاصلة')
    projects = models.TextField('المشاريع', help_text='افصل بين المشاريع بفاصلة')
    is_published = models.BooleanField('منشور', default=True)
    is_featured = models.BooleanField('مميز', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'كورس'
        verbose_name_plural = 'الكورسات'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'slug': self.slug})

    def get_skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]

    def get_projects_list(self):
        return [p.strip() for p in self.projects.split(',') if p.strip()]

    def update_lesson_count(self):
        count = Lesson.objects.filter(section__course=self).count()
        self.lesson_count = count
        self.save(update_fields=['lesson_count'])


class CourseSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField('عنوان الأسبوع', max_length=255)
    order = models.PositiveIntegerField('الترتيب', default=0)

    class Meta:
        verbose_name = 'أسبوع'
        verbose_name_plural = 'الأسابيع'
        ordering = ['order']

    def __str__(self):
        return f'{self.course.title} - {self.title}'


class Lesson(models.Model):
    LESSON_TYPES = [
        ('video', 'فيديو'),
        ('pdf', 'PDF'),
        ('assignment', 'واجب'),
        ('file', 'ملف'),
    ]

    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField('عنوان الدرس', max_length=255)
    lesson_type = models.CharField('نوع الدرس', max_length=20, choices=LESSON_TYPES, default='video')
    video = models.FileField('فيديو', upload_to='courses/videos/', blank=True, null=True)
    video_url = models.URLField('رابط فيديو خارجي', blank=True)
    description = models.TextField('وصف الدرس', blank=True)
    order = models.PositiveIntegerField('الترتيب', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'درس'
        verbose_name_plural = 'الدروس'
        ordering = ['order']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.section.course.update_lesson_count()


class LessonFile(models.Model):
    FILE_TYPES = [
        ('pdf', 'PDF'),
        ('other', 'ملف إضافي'),
    ]

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='files')
    title = models.CharField('اسم الملف', max_length=255)
    file = models.FileField('الملف', upload_to='courses/files/')
    file_type = models.CharField('نوع الملف', max_length=10, choices=FILE_TYPES, default='pdf')

    class Meta:
        verbose_name = 'ملف درس'
        verbose_name_plural = 'ملفات الدروس'

    def __str__(self):
        return self.title


class CourseSubscription(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد المراجعة'),
        ('approved', 'مفعّل'),
        ('rejected', 'مرفوض'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscriptions')
    status = models.CharField('الحالة', max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField('ملاحظات الإدارة', blank=True)

    class Meta:
        verbose_name = 'اشتراك'
        verbose_name_plural = 'الاشتراكات'
        unique_together = ['user', 'course']
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.full_name} - {self.course.title}'

    def get_status_display_ar(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)

    @property
    def is_active(self):
        return self.status == 'approved'


class PaymentProof(models.Model):
    subscription = models.OneToOneField(CourseSubscription, on_delete=models.CASCADE, related_name='payment_proof')
    full_name = models.CharField('الاسم', max_length=255)
    phone = models.CharField('رقم الهاتف', max_length=20)
    proof_image = models.ImageField('إثبات الدفع', upload_to='payments/')
    notes = models.TextField('ملاحظات', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'إثبات دفع'
        verbose_name_plural = 'إثباتات الدفع'

    def __str__(self):
        return f'دفع {self.full_name} - {self.subscription.course.title}'


class Certificate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    file = models.FileField('ملف الشهادة', upload_to='certificates/')
    completion_date = models.DateField('تاريخ الإكمال')
    instructor_name = models.CharField('اسم المدرب', max_length=255, default='ماركو زكريا')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'شهادة'
        verbose_name_plural = 'الشهادات'
        unique_together = ['user', 'course']

    def __str__(self):
        return f'شهادة {self.user.full_name} - {self.course.title}'


class Testimonial(models.Model):
    student_name = models.CharField('اسم الطالب', max_length=255)
    student_title = models.CharField('المسمى', max_length=255, blank=True)
    content = models.TextField('الرأي')
    rating = models.PositiveIntegerField('التقييم', default=5)
    avatar = models.ImageField('الصورة', upload_to='testimonials/', blank=True, null=True)
    is_active = models.BooleanField('نشط', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'رأي طالب'
        verbose_name_plural = 'آراء الطلاب'

    def __str__(self):
        return self.student_name
