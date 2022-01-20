from django.shortcuts import render, get_object_or_404
from .models import Note

# Create your views here.

def note_list(request):
    notes = Note.objects.filter(status=1)
    notes_count = Note.objects.filter(status=1).count()
    return render(request, 'note_list.html', {'notes': notes, 'notes_count': notes_count})

def note_detail(request, note_slug):
    note = get_object_or_404(Note, slug=note_slug, status=1)
    return render(request, 'note_detail.html', {'note': note})