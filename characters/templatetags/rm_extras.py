from django import template

register = template.Library()

STATUS_RU = {
    'Alive': 'Жив',
    'Dead': 'Мёртв',
    'unknown': 'Неизвестно',
}

SPECIES_RU = {
    'Human': 'Человек',
    'Alien': 'Пришелец',
    'Humanoid': 'Гуманоид',
    'Animal': 'Животное',
    'Robot': 'Робот',
    'Mythological Creature': 'Мифическое существо',
    'Poopybutthole': 'Пупибатхол',
    'Cronenberg': 'Кроненберг',
    'Disease': 'Болезнь',
    'unknown': 'Неизвестно',
}


@register.filter
def status_ru(value):
    return STATUS_RU.get(value, value or 'Неизвестно')


@register.filter
def species_ru(value):
    return SPECIES_RU.get(value, value)
