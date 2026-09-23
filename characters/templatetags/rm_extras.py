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


LOCATION_TYPE_RU = {
    'Acid Plant': 'Кислотный завод',
    'Arcade': 'Аркада',
    'Artificially generated world': 'Искусственный мир',
    'Asteroid': 'Астероид',
    'Base': 'База',
    'Box': 'Коробка',
    'Cluster': 'Скопление',
    'Consciousness': 'Сознание',
    'Convention': 'Конференция',
    'Country': 'Страна',
    'Customs': 'Таможня',
    'Daycare': 'Детский сад',
    'Death Star': 'Звезда Смерти',
    'Diegesis': 'Диегезис',
    'Dimension': 'Измерение',
    'Dream': 'Сон',
    'Dwarf planet (Celestial Dwarf)': 'Карликовая планета',
    'Elemental Rings': 'Стихийные кольца',
    'Fantasy town': 'Фэнтезийный город',
    'Game': 'Игра',
    'Hell': 'Ад',
    'Human': 'Человек',
    'Liquid': 'Жидкость',
    'Machine': 'Машина',
    'Memory': 'Воспоминание',
    'Menagerie': 'Зверинец',
    'Microverse': 'Микровселенная',
    'Miniverse': 'Минивселенная',
    'Mount': 'Гора',
    'Nightmare': 'Кошмар',
    'Non-Diegetic Alternative Reality': 'Недиегетическая реальность',
    'Planet': 'Планета',
    'Police Department': 'Полицейский участок',
    'Quadrant': 'Квадрант',
    'Quasar': 'Квазар',
    'Reality': 'Реальность',
    'Resort': 'Курорт',
    'Spa': 'Спа',
    'Space': 'Космос',
    'Space station': 'Космическая станция',
    'Spacecraft': 'Космический корабль',
    'TV': 'Телевизор',
    'Teenyverse': 'Крошечная вселенная',
    'Woods': 'Лес',
    'unknown': 'Неизвестно',
}


@register.filter
def status_ru(value):
    return STATUS_RU.get(value, value or 'Неизвестно')


@register.filter
def species_ru(value):
    return SPECIES_RU.get(value, value)


@register.filter
def location_type_ru(value):
    return LOCATION_TYPE_RU.get(value, value)


@register.filter
def dimension_ru(value):
    if value == 'unknown':
        return 'Неизвестно'
    return value
