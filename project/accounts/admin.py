from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['full_name', 'email', 'phone', 'is_active_account', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_active_account', 'is_active']
    search_fields = ['full_name', 'email', 'phone']
    ordering = ['-date_joined']
    inlines = [ProfileInline]

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('المعلومات الشخصية', {'fields': ('full_name', 'phone')}),
        ('الصلاحيات', {'fields': ('is_active', 'is_active_account', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone', 'password1', 'password2'),
        }),
    )
