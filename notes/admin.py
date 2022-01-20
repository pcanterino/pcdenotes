from django.contrib import admin
from .models import Note

# Register your models here.

class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'status',)
    list_filter = ('status',)
    search_fields = ('title', 'content',)


admin.site.register(Note, NoteAdmin)