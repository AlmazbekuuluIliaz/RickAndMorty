from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('characters/', views.character_list, name='character_list'),
    path('characters/<int:pk>/', views.character_detail, name='character_detail'),
    path('locations/', views.location_list, name='location_list'),
    path('locations/<int:pk>/', views.location_detail, name='location_detail'),
    path('episodes/', views.episode_list, name='episode_list'),
    path('episodes/<int:pk>/', views.episode_detail, name='episode_detail'),
    path('characters/<int:pk>/notes/create/', views.note_create, name='note_create'),
    path('notes/<int:pk>/edit/', views.note_update, name='note_update'),
    path('notes/<int:pk>/delete/', views.note_delete, name='note_delete'),
]
