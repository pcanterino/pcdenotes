from django.db import models
from django.db.models import Count
from django.db.models.functions import ExtractYear, ExtractMonth, Coalesce
from django.db.models.signals import pre_save

from django.dispatch import receiver
from django.contrib.auth.models import User
from django.urls import reverse

from datetime import datetime

# Create your models here.

NOTE_STATUS = ((0, "Draft"),
               (1, "Published"))            

class NoteQuerySet(models.QuerySet):
    pass

class NoteManager(models.Manager):
    def all_published(self):
        return super().get_queryset().filter(status=1).annotate(publication_date=Coalesce('published_at', 'created_at')).order_by('-publication_date')

    def all(self):
        return super().all().annotate(publication_date=Coalesce('published_at', 'created_at')).order_by('-publication_date')

    def per_year(self, year):
        return self.all_published().filter(publication_date__year=year)

    def per_month(self, year, month):
        return self.per_year(year).filter(publication_date__month=month)

    def years(self):
        return self.all_published().annotate(published_year=ExtractYear('publication_date')).values_list('published_year', flat=True).distinct().order_by('published_year')

    def years_with_total(self):
        return self.all_published().annotate(published_year=ExtractYear('publication_date')).values('published_year').annotate(total=Count('id')).order_by('published_year').values('published_year', 'total').distinct()

    def months(self, year):
        return self.per_year(year).annotate(published_month=ExtractMonth('publication_date')).values_list('published_month', flat=True).distinct().order_by('published_month')

    def months_with_total(self, year):
        return self.per_year(year).annotate(published_month=ExtractMonth('publication_date')).values('published_month').annotate(total=Count('id')).order_by('published_month').values('published_month', 'total').distinct()

class Note(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes_posted')
    content = models.TextField()
    status = models.IntegerField(choices=NOTE_STATUS, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, editable=False)

    objects = NoteManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("notes:note_detail", kwargs={"note_slug": self.slug})

    def is_draft(self):
        return self.status == 0

    def is_published(self):
        return self.status == 1

@receiver(pre_save, sender=Note)
def note_pre_save(sender, instance, **kwargs):
    if instance.pk is None:
        if instance.status == 1:
            instance.published_at = datetime.now()
    else:
        old_instance = Note.objects.get(pk=instance.pk)
        
        if old_instance.status == 0 and instance.status == 1:
            instance.published_at = datetime.now()