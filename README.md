# Rick and Morty

Каталог персонажей, локаций и эпизодов сериала «Рик и Морти».
Данные берутся из [Rick and Morty API](https://rickandmortyapi.com/).
Есть поиск и фильтры, а авторизованные пользователи могут оставлять заметки к персонажам.

## Требования

- Python 3.12
- Django 6.1 (остальные зависимости — в requirements.txt)

## Запуск

1. Создать и активировать виртуальное окружение:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   На Linux/macOS активация: `source venv/bin/activate`

2. Установить зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Создать файл `.env` (можно скопировать из `.env.example`) и указать секретный ключ:

   ```env
   DJANGO_SECRET_KEY=любой-секретный-ключ
   ```

4. Создать и применить миграции:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Загрузить данные из API:

   ```bash
   python manage.py fetch_rick_and_morty
   ```

6. Создать суперпользователя для входа в админку:

   ```bash
   python manage.py createsuperuser
   ```

   Тестового суперпользователя в проекте нет, логин и пароль задаются при создании.

7. Запустить сервер:

   ```bash
   python manage.py runserver
   ```

   Сайт: http://127.0.0.1:8000/, админка: http://127.0.0.1:8000/admin/

## Основные URL

- `/` — главная
- `/characters/` — список персонажей
- `/characters/<id>/` — персонаж и заметки к нему
- `/locations/` — список локаций
- `/locations/<id>/` — локация
- `/episodes/` — список эпизодов
- `/episodes/<id>/` — эпизод
- `/accounts/register/` — регистрация
- `/accounts/login/` — вход
- `/accounts/logout/` — выход
- `/admin/` — админка
