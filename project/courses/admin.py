from django.contrib import admin
from .models import (
    Course, CourseSection, Lesson, LessonFile,
    CourseSubscription, PaymentProof, Certificate, Testimonial,
)


class SectionInline(admin.TabularInline):
    model = CourseSection
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'duration', 'lesson_count', 'is_published', 'created_at']
    list_filter = ['is_published', 'is_featured']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [SectionInline]


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0


@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    inlines = [LessonInline]


class LessonFileInline(admin.TabularInline):
    model = LessonFile
    extra = 0


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'lesson_type', 'order']
    inlines = [LessonFileInline]


@admin.register(CourseSubscription)
class CourseSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'status', 'created_at']
    list_filter = ['status']


@admin.register(PaymentProof)
class PaymentProofAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'subscription', 'created_at']


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'completion_date', 'instructor_name']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'rating', 'is_active']
