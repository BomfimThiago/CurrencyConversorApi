# Generated by Django 4.1.10 on 2023-08-07 18:19
import uuid

from django.db import migrations, models

import core.models.user.managers


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="Email address"
                    ),
                ),
                (
                    "full_name",
                    models.CharField(blank=True, max_length=60, verbose_name="Full name"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is active"),
                ),
                (
                    "is_staff",
                    models.BooleanField(default=False, verbose_name="Is staff"),
                ),
                (
                    "is_superuser",
                    models.BooleanField(default=False, verbose_name="Is admin"),
                ),
                (
                    "date_joined",
                    models.DateTimeField(auto_now_add=True, verbose_name="Date joined"),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            managers=[
                ("objects", core.models.user.managers.UserManager()),
            ],
        ),
    ]