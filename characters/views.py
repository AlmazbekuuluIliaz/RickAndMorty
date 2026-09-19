from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Character, Episode, Location, Note

# Сколько персонажей показывать на одной странице списка (ТЗ, п.5.3).
CHARACTERS_PER_PAGE = 20


def home(request):
    """Главная страница: краткая статистика по проекту (ТЗ, п.5.2).

    count() выполняет лёгкий SQL COUNT(*) и не тянет объекты в память —
    именно то, что нужно для чисел на странице (см. ТЗ, п.8).
    """
    context = {
        'characters_count': Character.objects.count(),
        'locations_count': Location.objects.count(),
        'episodes_count': Episode.objects.count(),
        'notes_count': Note.objects.count(),
    }
    return render(request, 'home.html', context)


def character_list(request):
    """Список персонажей с пагинацией (ТЗ, п.5.3).

    Пока без поиска и фильтров — их добавим следующими шагами. Сейчас
    задача проще: показать всех персонажей карточками, разбив на страницы.
    """
    # Порядок берётся из Meta.ordering модели (['api_id']), сортировать
    # отдельно не нужно.
    characters = Character.objects.all()

    paginator = Paginator(characters, CHARACTERS_PER_PAGE)
    # get_page безопаснее page(): некорректный или отсутствующий номер он
    # аккуратно сведёт к первой/последней странице, а не бросит исключение.
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'characters/character_list.html', {'page_obj': page_obj})
