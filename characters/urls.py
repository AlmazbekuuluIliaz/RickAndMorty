from django.urls import path

from . import views

# Пока без app_name: главная — общепроектная страница, и в base.html на неё
# удобно ссылаться коротким {% url 'home' %}. Когда добавим список персонажей,
# локаций и эпизодов, можно будет ввести пространство имён.
urlpatterns = [
    path('', views.home, name='home'),
    path('characters/', views.character_list, name='character_list'),
]
