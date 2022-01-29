from django.urls import path, re_path
from . import views

app_name = 'notes'

urlpatterns=[
    path('', views.note_list, name='note_list'),
    re_path('^notes/?$', views.note_redirect, name='note_redirect'),
    path('notes/<slug:note_slug>', views.note_detail, name='note_detail'),
]