from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm

from core.models import User


class UserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class UserChangeForm(DjangoUserChangeForm):
    class Meta:
        model = User
        fields = ("email",)


class UserAdmin(DjangoUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        "email",
        "full_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )
    list_filter = ("is_active", "is_staff", "is_superuser")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "full_name",
                    "picture",
                )
            },
        ),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Meta", {"fields": ("date_joined",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "picture",
                ),
            },
        ),
    )
    readonly_fields = ("date_joined",)
    search_fields = ("email", "full_name")
    ordering = ("email",)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
