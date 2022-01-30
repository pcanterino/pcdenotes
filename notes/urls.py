from django.urls import path, re_path
from . import views

app_name = 'notes'

urlpatterns=[
    path('', views.note_list, name='note_list'),
    re_path('^notes/?$', views.note_redirect, name='note_redirect'),
    path('notes/<slug:note_slug>', views.note_detail, name='note_detail'),
    path('archive/', views.archive_main, name='archive_main'),
    path('archive/<int:archive_year>/', views.archive_year, name='archive_year'),
    path('archive/<int:archive_year>/<int:archive_month>/', views.archive_month, name='archive_month'),
]