from django.contrib import admin

from authentication.models import Code


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    pass
