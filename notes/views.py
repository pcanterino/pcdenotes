from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models.functions import ExtractYear, ExtractMonth

from pcdenotes.settings import NOTES_PER_PAGE
from .models import Note

# Create your views here.

def note_list(request):
    notes = Note.objects.all() if request.user.is_staff else Note.objects.all_published()

    notes_count = notes.count()
    paginator = Paginator(notes, NOTES_PER_PAGE)

    page_number = 1

    try:
        page_number = int(request.GET.get('page'))
    except:
        pass

    page_count = paginator.num_pages
    
    notes_page = paginator.get_page(page_number)

    return render(request, 'note_list.html', {'notes_page': notes_page, 'notes_count': notes_count, 'pages': paginator, 'page_number': page_number, 'page_count': page_count})

def note_redirect(request):
    return redirect('notes:note_list', permanent=True)

def note_detail(request, note_slug):
    note = get_object_or_404(Note, slug=note_slug) if request.user.is_staff else get_object_or_404(Note, slug=note_slug, status=1)
    return render(request, 'note_detail.html', {'note': note})

def archive_main(request):
    notes_years = Note.objects.years_with_total()
    return render(request, 'archive_main.html', {'years': notes_years})

def archive_year(request, archive_year):
    notes_months = Note.objects.months_with_total(archive_year)
    return render(request, 'archive_year.html', {'year': archive_year, 'months': notes_months})

def archive_month(request, archive_year, archive_month):
    notes = Note.objects.per_month(archive_year, archive_month)
    return render(request, 'archive_month.html', {'year': archive_year, 'month': archive_month, 'notes': notes})