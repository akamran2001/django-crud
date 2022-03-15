from django.urls import path, re_path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('edit/', views.edit, name='edit'),
    path('notes/<int:id>/', views.notes, name='notes'),
    path('notes/', views.notes),
]
