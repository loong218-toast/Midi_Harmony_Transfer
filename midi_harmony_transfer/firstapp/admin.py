from django.contrib import admin
from .models import midi_data
# Register your models here.
class midi_dataAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'completed')

admin.site.register(midi_data, midi_dataAdmin)