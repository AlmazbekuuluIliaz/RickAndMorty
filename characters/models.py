from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.db import models

# Модели объявлены в таком порядке специально: Character ссылается на
# Location и Episode, поэтому те должны быть определены выше него.

# Максимальная длина текста заметки (см. ТЗ, п.6: 500–1000 символов).
NOTE_MAX_LENGTH = 1000


class Location(models.Model):
    """Локация из Rick and Morty API (планета, измерение и т.п.)."""

    # api_id — это "id" объекта в самом API. unique=True не даёт импорту
    # создать дубликат при повторном запуске команды.
    api_id = models.PositiveIntegerField(unique=True)
    # db_index — поле участвует в поиске (п.5.5), индекс ускоряет выборку.
    name = models.CharField(max_length=255, db_index=True)
    type = models.CharField(max_length=255, blank=True)
    dimension = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True)
    # created — время создания записи В САМОМ API (приходит строкой из JSON).
    created = models.DateTimeField(null=True, blank=True)
    # updated_at — наша собственная метка: когда мы последний раз обновили
    # запись у себя в БД. auto_now сам проставляет её при каждом save().
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['api_id']
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.name


class Episode(models.Model):
    """Эпизод сериала."""

    api_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255, db_index=True)
    air_date = models.CharField(max_length=100, blank=True)
    # episode_code — код вида "S01E01". В API это поле называется "episode".
    episode_code = models.CharField(max_length=20, blank=True, db_index=True)
    url = models.URLField(blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['api_id']
        verbose_name = 'Эпизод'
        verbose_name_plural = 'Эпизоды'

    def __str__(self):
        return f'{self.episode_code} — {self.name}'


class Character(models.Model):
    """Персонаж. Ссылается на локации (origin/location) и эпизоды (M2M)."""

    # Возможные значения status в API. choices дают удобный фильтр в admin
    # и валидацию, но не мешают импорту (в API бывает и пустая строка).
    STATUS_ALIVE = 'Alive'
    STATUS_DEAD = 'Dead'
    STATUS_UNKNOWN = 'unknown'
    STATUS_CHOICES = [
        (STATUS_ALIVE, 'Alive'),
        (STATUS_DEAD, 'Dead'),
        (STATUS_UNKNOWN, 'Unknown'),
    ]

    api_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True)
    species = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=50, blank=True)
    image = models.URLField(blank=True)

    # origin и location оба указывают на Location, поэтому им нужны разные
    # related_name — иначе Django не сможет построить обратные связи.
    # В API origin/location могут быть "unknown" без ссылки, поэтому
    # null/blank=True, а SET_NULL — чтобы удаление локации не удаляло персонажа.
    origin = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='origin_characters',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='residents',
    )

    # Персонаж появляется во многих эпизодах, эпизод содержит многих
    # персонажей — это связь Many-to-Many. С Episode.characters получим
    # обратный доступ.
    episodes = models.ManyToManyField(
        Episode,
        blank=True,
        related_name='characters',
    )

    created = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['api_id']
        verbose_name = 'Персонаж'
        verbose_name_plural = 'Персонажи'

    def __str__(self):
        return self.name


class Note(models.Model):
    """Пользовательская заметка о персонаже (CRUD-часть проекта)."""

    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,  # удалили персонажа — удалились и его заметки
        related_name='notes',
    )
    # author опционален: базовый вариант ТЗ работает без авторизации.
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notes',
    )
    # TextField не пустой по умолчанию (blank=False), поэтому форма не даст
    # сохранить пустой текст. MaxLengthValidator ограничивает длину сверху.
    text = models.TextField(validators=[MaxLengthValidator(NOTE_MAX_LENGTH)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # новые заметки сверху
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'

    def __str__(self):
        return f'Note #{self.pk} for {self.character.name}'
