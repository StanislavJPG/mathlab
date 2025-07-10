from django.contrib import admin
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from server.apps.complaints.models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'category', 'content_object', 'content_type')
    search_fields = (
        'id',
        'uuid',
        'content_object',
    )
    list_filter = ('processed', 'counter', 'category')
    readonly_fields = ('counter', 'complained_object_url')

    @admin.display(description=_('🤬 URL of complained object'))
    def complained_object_url(self, instance):
        co = instance.content_object
        ct = instance.content_type
        url = reverse_lazy(f'admin:{ct.app_label}_{ct.model}_change', args=(co.id,))
        return mark_safe(f'<a href="{url}" target="_blank">{co}</a>')
