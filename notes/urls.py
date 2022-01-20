from django.urls import path
from . import views

app_name = 'notes'

urlpatterns=[
    path('', views.note_list, name="note_list"),
    path('notes/<slug:note_slug>', views.note_detail, name="note_detail"),
]