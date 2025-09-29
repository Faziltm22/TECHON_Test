from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book, PasswordResetOTP


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("is_staff", "is_active",)
    search_fields = ("email",)
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active")}
        ),
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date", "user")
    search_fields = ("title", "author")
    list_filter = ("published_date",)


@admin.register(PasswordResetOTP)
class PasswordResetOTPAdmin(admin.ModelAdmin):
    list_display = ("user", "otp", "created_at", "is_valid_status")
    search_fields = ("user__email", "otp")
    list_filter = ("created_at",)

    def is_valid_status(self, obj):
        return obj.is_valid()
    is_valid_status.boolean = True  
    is_valid_status.short_description = "Valid?"



admin.site.register(CustomUser, CustomUserAdmin)
