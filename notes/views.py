from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from pcdenotes.settings import NOTES_PER_PAGE
from .models import Note

# Create your views here.

def note_list(request):
    notes = Note.objects.filter(status=1)
    notes_count = Note.objects.filter(status=1).count()
    paginator = Paginator(notes, NOTES_PER_PAGE)

    page_number = 1

    try:
        page_number = int(request.GET.get('page'))
    except:
        pass

    page_count = paginator.num_pages
    
    notes_page = paginator.get_page(page_number)

    return render(request, 'note_list.html', {'notes_page': notes_page, 'notes_count': notes_count, 'pages': paginator, 'page_number': page_number, 'page_count': page_count})

def note_detail(request, note_slug):
    note = get_object_or_404(Note, slug=note_slug, status=1)
    return render(request, 'note_detail.html', {'note': note})