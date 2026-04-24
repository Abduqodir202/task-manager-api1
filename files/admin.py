from django.contrib import admin

from files.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass