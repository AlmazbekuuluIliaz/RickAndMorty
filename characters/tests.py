from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import NoteForm
from .models import Character, Note

User = get_user_model()


class CharacterCreationTests(TestCase):
    def test_create_character(self):
        character = Character.objects.create(
            api_id=1, name='Rick Sanchez',
            status='Alive', species='Human',
        )
        self.assertEqual(Character.objects.count(), 1)
        self.assertEqual(character.name, 'Rick Sanchez')
        self.assertEqual(str(character), 'Rick Sanchez')


class CharacterListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.rick = Character.objects.create(api_id=1, name='Rick Sanchez')
        cls.morty = Character.objects.create(api_id=2, name='Morty Smith')

    def test_list_shows_all_characters(self):
        response = self.client.get(reverse('character_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 2)

    def test_search_by_name(self):
        response = self.client.get(
            reverse('character_list'), {'search': 'rick'}
        )
        self.assertEqual(list(response.context['page_obj']), [self.rick])


class NoteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.character = Character.objects.create(api_id=1, name='Rick')
        cls.user = User.objects.create_user('user', password='pass12345')

    def test_create_note(self):
        self.client.force_login(self.user)
        url = reverse('note_create', args=[self.character.pk])
        response = self.client.post(url, {'text': 'Умный дед'})
        self.assertRedirects(
            response, reverse('character_detail', args=[self.character.pk])
        )
        note = Note.objects.get()
        self.assertEqual(note.text, 'Умный дед')
        self.assertEqual(note.author, self.user)
        self.assertEqual(note.character, self.character)

    def test_delete_note(self):
        note = Note.objects.create(
            character=self.character, author=self.user, text='bye'
        )
        self.client.force_login(self.user)
        url = reverse('note_delete', args=[note.pk])
        response = self.client.post(url)
        self.assertRedirects(
            response, reverse('character_detail', args=[self.character.pk])
        )
        self.assertEqual(Note.objects.count(), 0)

    def test_empty_note_is_rejected(self):
        form = NoteForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)


class NotFoundTests(TestCase):
    def test_character_detail_404(self):
        response = self.client.get(reverse('character_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_location_detail_404(self):
        response = self.client.get(reverse('location_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_episode_detail_404(self):
        response = self.client.get(reverse('episode_detail', args=[999]))
        self.assertEqual(response.status_code, 404)
