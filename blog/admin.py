from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from.models import User, Blog,Comment

class BlogAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    empty_value_display = '-empty-'
    list_display = ('title', 'author', 'created_at', 'updated_at', 'published')
    list_filter = ('status',)
    ordering = ('created_at',)
    search_fields = ('title','content')

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "is_active", "is_superuser")
    list_filter = ("email", "is_active", "is_superuser")
    search_fields = ("email",)
    ordering = ("-created_at",)
    fieldsets = (
        ("Authentications", {"fields": ("email", "password", "username")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active")}),
        ("Group Permission", {"fields": ("groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "phone",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                ),
            },
        ),
    )

admin.site.register(User,CustomUserAdmin)
admin.site.register(Blog,BlogAdmin)
admin.site.register(Comment)


# Register your models here.
