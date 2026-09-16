from django.contrib import admin

from .models import Character, Episode, Location, Note


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('api_id', 'name', 'type', 'dimension')
    search_fields = ('name', 'type', 'dimension')
    list_filter = ('type', 'dimension')
    ordering = ('api_id',)
    readonly_fields = ('created', 'updated_at')


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('api_id', 'episode_code', 'name', 'air_date')
    search_fields = ('name', 'episode_code')
    list_filter = ('air_date',)
    ordering = ('api_id',)
    readonly_fields = ('created', 'updated_at')


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('api_id', 'name', 'status', 'species', 'gender')
    search_fields = ('name', 'species', 'type')
    list_filter = ('status', 'species', 'gender')
    ordering = ('api_id',)
    # select_related убирает лишние SQL-запросы к Location в списке admin
    # (origin и location — это ForeignKey).
    list_select_related = ('origin', 'location')
    # autocomplete подгружает локации по поиску, а не грузит все сразу
    # (работает, т.к. у LocationAdmin задан search_fields).
    autocomplete_fields = ('origin', 'location')
    # filter_horizontal — удобный двухпанельный виджет для M2M с эпизодами.
    filter_horizontal = ('episodes',)
    readonly_fields = ('created', 'updated_at')


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'character', 'author', 'created_at')
    search_fields = ('text', 'character__name')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    list_select_related = ('character', 'author')
    autocomplete_fields = ('character', 'author')
    readonly_fields = ('created_at', 'updated_at')
