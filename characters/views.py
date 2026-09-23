from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import NoteForm, RegisterForm
from .models import Character, Episode, Location, Note

CHARACTERS_PER_PAGE = 20
LOCATIONS_PER_PAGE = 20
EPISODES_PER_PAGE = 20


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Аккаунт создан. Добро пожаловать!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def home(request):
    context = {
        'characters_count': Character.objects.count(),
        'locations_count': Location.objects.count(),
        'episodes_count': Episode.objects.count(),
        'notes_count': Note.objects.count(),
    }
    return render(request, 'home.html', context)


def character_list(request):
    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '')
    species = request.GET.get('species', '')

    characters = Character.objects.all()
    if search:
        characters = characters.filter(name__icontains=search)
    if status:
        characters = characters.filter(status=status)
    if species:
        characters = characters.filter(species=species)

    paginator = Paginator(characters, CHARACTERS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))

    params = request.GET.copy()
    params.pop('page', None)

    context = {
        'page_obj': page_obj,
        'search': search,
        'status': status,
        'species': species,
        'status_choices': Character.STATUS_CHOICES,
        'species_options': (
            Character.objects.exclude(species='')
            .values_list('species', flat=True)
            .distinct()
            .order_by('species')
        ),
        'querystring': params.urlencode(),
    }
    return render(request, 'characters/character_list.html', context)


def _character_detail_context(character, form):
    return {
        'character': character,
        'episodes': character.episodes.all(),
        'notes': character.notes.select_related('author'),
        'form': form,
    }


def character_detail(request, pk):
    character = get_object_or_404(
        Character.objects.select_related('origin', 'location').prefetch_related('episodes'),
        pk=pk,
    )
    context = _character_detail_context(character, NoteForm())
    return render(request, 'characters/character_detail.html', context)


@login_required
@require_POST
def note_create(request, pk):
    character = get_object_or_404(
        Character.objects.select_related('origin', 'location').prefetch_related('episodes'),
        pk=pk,
    )
    form = NoteForm(request.POST)
    if form.is_valid():
        note = form.save(commit=False)
        note.character = character
        note.author = request.user
        note.save()
        messages.success(request, 'Заметка добавлена.')
        return redirect('character_detail', pk=character.pk)

    context = _character_detail_context(character, form)
    return render(request, 'characters/character_detail.html', context)


@login_required
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk, author=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заметка обновлена.')
            return redirect('character_detail', pk=note.character_id)
    else:
        form = NoteForm(instance=note)
    return render(request, 'characters/note_edit.html', {'form': form, 'note': note})


@login_required
@require_POST
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, author=request.user)
    character_pk = note.character_id
    note.delete()
    messages.success(request, 'Заметка удалена.')
    return redirect('character_detail', pk=character_pk)


def location_list(request):
    search = request.GET.get('search', '').strip()
    loc_type = request.GET.get('type', '')
    dimension = request.GET.get('dimension', '')

    locations = Location.objects.all()
    if search:
        locations = locations.filter(name__icontains=search)
    if loc_type:
        locations = locations.filter(type=loc_type)
    if dimension:
        locations = locations.filter(dimension=dimension)

    paginator = Paginator(locations, LOCATIONS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))

    params = request.GET.copy()
    params.pop('page', None)

    context = {
        'page_obj': page_obj,
        'search': search,
        'type': loc_type,
        'dimension': dimension,
        'type_options': (
            Location.objects.exclude(type='')
            .values_list('type', flat=True)
            .distinct()
            .order_by('type')
        ),
        'dimension_options': (
            Location.objects.exclude(dimension='')
            .values_list('dimension', flat=True)
            .distinct()
            .order_by('dimension')
        ),
        'querystring': params.urlencode(),
    }
    return render(request, 'locations/location_list.html', context)


def location_detail(request, pk):
    location = get_object_or_404(Location, pk=pk)
    context = {
        'location': location,
        'residents': location.residents.all(),
    }
    return render(request, 'locations/location_detail.html', context)


def episode_list(request):
    search = request.GET.get('search', '').strip()

    episodes = Episode.objects.annotate(characters_count=Count('characters')).order_by('api_id')
    if search:
        episodes = episodes.filter(
            Q(name__icontains=search) | Q(episode_code__icontains=search)
        )

    paginator = Paginator(episodes, EPISODES_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))

    params = request.GET.copy()
    params.pop('page', None)

    context = {
        'page_obj': page_obj,
        'search': search,
        'querystring': params.urlencode(),
    }
    return render(request, 'episodes/episode_list.html', context)


def episode_detail(request, pk):
    episode = get_object_or_404(
        Episode.objects.prefetch_related('characters'),
        pk=pk,
    )
    context = {
        'episode': episode,
        'characters': episode.characters.all(),
    }
    return render(request, 'episodes/episode_detail.html', context)
