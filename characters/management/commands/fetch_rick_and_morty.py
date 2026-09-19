import requests
from django.core.management.base import BaseCommand, CommandError
from django.utils.dateparse import parse_datetime

from characters.models import Character, Episode, Location

BASE_URL = 'https://rickandmortyapi.com/api'
REQUEST_TIMEOUT = 10


def extract_id(url):
    if not url:
        return None
    return int(url.rstrip('/').split('/')[-1])


def parse_api_datetime(value):
    return parse_datetime(value) if value else None


class Command(BaseCommand):
    help = 'Импортирует персонажей, локации и эпизоды из Rick and Morty API.'

    def handle(self, *args, **options):
        self.import_locations()
        self.import_episodes()
        self.import_characters()
        self.stdout.write(self.style.SUCCESS('Done!'))

    def get_json(self, url):
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.Timeout:
            raise CommandError('API не ответил вовремя (timeout). Попробуйте позже.')
        except requests.ConnectionError:
            raise CommandError('Не удалось подключиться к API. Проверьте интернет.')
        except requests.HTTPError as exc:
            raise CommandError(f'API вернул HTTP-ошибку: {exc}')
        except ValueError:
            raise CommandError('API вернул некорректный JSON.')

    def fetch_all(self, endpoint):
        url = f'{BASE_URL}/{endpoint}'
        while url:
            data = self.get_json(url)
            for item in data['results']:
                yield item
            url = data['info']['next']

    def report(self, label, created, updated):
        self.stdout.write(f'{label} found: {created + updated}')
        self.stdout.write(f'Created: {created}')
        self.stdout.write(f'Updated: {updated}')

    def import_locations(self):
        self.stdout.write('Fetching locations...')
        created = updated = 0
        for loc in self.fetch_all('location'):
            _, was_created = Location.objects.update_or_create(
                api_id=loc['id'],
                defaults={
                    'name': loc['name'],
                    'type': loc['type'],
                    'dimension': loc['dimension'],
                    'url': loc['url'],
                    'created': parse_api_datetime(loc.get('created')),
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1
        self.report('Locations', created, updated)

    def import_episodes(self):
        self.stdout.write('Fetching episodes...')
        created = updated = 0
        for ep in self.fetch_all('episode'):
            _, was_created = Episode.objects.update_or_create(
                api_id=ep['id'],
                defaults={
                    'name': ep['name'],
                    'air_date': ep['air_date'],
                    'episode_code': ep['episode'],
                    'url': ep['url'],
                    'created': parse_api_datetime(ep.get('created')),
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1
        self.report('Episodes', created, updated)

    def import_characters(self):
        self.stdout.write('Fetching characters...')
        locations = {loc.api_id: loc for loc in Location.objects.all()}
        episodes = {ep.api_id: ep for ep in Episode.objects.all()}

        created = updated = 0
        for char in self.fetch_all('character'):
            character, was_created = Character.objects.update_or_create(
                api_id=char['id'],
                defaults={
                    'name': char['name'],
                    'status': char['status'],
                    'species': char['species'],
                    'type': char['type'],
                    'gender': char['gender'],
                    'image': char['image'],
                    'origin': locations.get(extract_id(char['origin']['url'])),
                    'location': locations.get(extract_id(char['location']['url'])),
                    'created': parse_api_datetime(char.get('created')),
                },
            )
            episode_ids = [extract_id(url) for url in char['episode']]
            character.episodes.set(
                episodes[eid] for eid in episode_ids if eid in episodes
            )
            if was_created:
                created += 1
            else:
                updated += 1
        self.report('Characters', created, updated)
