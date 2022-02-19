from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

NOTE_STATUS = ((0, "Draft"),
               (1, "Published"))            

class Note(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes_posted')
    content = models.TextField()
    status = models.IntegerField(choices=NOTE_STATUS, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
