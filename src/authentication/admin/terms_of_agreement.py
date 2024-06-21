from django.contrib import admin
from django.contrib.admin import display

from authentication.models import TermsOfAgreement, UserTermsOfAgreement


class TermsOfAgreementAdmin(admin.ModelAdmin):
    list_display = ("id", "terms_of_agreement", "created")
    list_filter = ("id",)
    search_fields = ("id", "terms_of_agreement", "created")
    ordering = ("id",)


admin.site.register(TermsOfAgreement, TermsOfAgreementAdmin)


class UserTermsOfAgreementAdmin(admin.ModelAdmin):
    list_display = ("user", "get_terms_of_agreement_id")
    list_filter = ("user",)
    search_fields = ("user", "terms_of_agreement")
    ordering = ("user",)

    @display(ordering="id", description="Terms of Agreement ID")
    def get_terms_of_agreement_id(self, obj):
        return obj.terms_of_agreement.id


admin.site.register(UserTermsOfAgreement, UserTermsOfAgreementAdmin)
