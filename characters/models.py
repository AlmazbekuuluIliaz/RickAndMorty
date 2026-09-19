from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.db import models

NOTE_MAX_LENGTH = 1000


class Location(models.Model):
    api_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255, db_index=True)
    type = models.CharField(max_length=255, blank=True)
    dimension = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['api_id']
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.name


class Episode(models.Model):
    api_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255, db_index=True)
    air_date = models.CharField(max_length=100, blank=True)
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
    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='notes',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notes',
    )
    text = models.TextField(validators=[MaxLengthValidator(NOTE_MAX_LENGTH)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'

    def __str__(self):
        return f'Note #{self.pk} for {self.character.name}'
