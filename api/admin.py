from django.contrib import admin

from api.models import Prompts


@admin.register(Prompts)
class PromptsAdmin(admin.ModelAdmin):
    list_display = ('prompt', 'created_at', 'updated_at')
    search_fields = ('prompt',)
