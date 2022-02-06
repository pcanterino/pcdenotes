from django.contrib import admin
from .models import Note

# Register your models here.

class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'status',)
    list_filter = ('status',)
    search_fields = ('title', 'content',)
    prepopulated_fields = {'slug': ('title',)}

    def get_form(self, request, obj=None, **kwargs):
        form = super(NoteAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['author'].initial = request.user
        return form

admin.site.register(Note, NoteAdmin)