# Atomic Habits

**Atomic Habits** – это Django‑приложение для управления привычками и задачами, предоставляющее REST‑API на базе Django REST Framework.

## Технологический стек
- **Python 3.14+**
- **Django 6.0.3**
- **Django REST Framework 3.16.1**
- **Celery 5.x** (для фоновых задач)
- **Redis** (брокер для Celery)
- **PostgreSQL** (основная БД)
- **JWT** (аутентификация через `djangorestframework-simplejwt`)
- **Poetry** (управление зависимостями)

## Установка
```bash
# Склонировать репозиторий
git clone <repo-url>
cd atomic_habits

# Установить зависимости через poetry
poetry install

# Создать файл .env (пример ниже) и выполнить миграции
cp .env.example .env
python manage.py migrate
```

## Переменные окружения (`.env`)
```
DEBUG=True
SECRET_KEY=your-secret-key
POSTGRES_DB=atomic_habits
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
REDIS_URL=redis://localhost:6379/0
```

## Запуск проекта
```bash
# Запуск dev‑сервера
python manage.py runserver

# Запуск Celery worker
celery -A config.celery.app worker -l info
```

## Структура проекта
```
atomic_habits/                     # Корневая директория проекта
├─ .git/                           # Git‑репозиторий
├─ .venv/                          # Виртуальное окружение (не включено в репозиторий)
├─ .idea/                          # Конфигурация PyCharm
├─ .gitignore
├─ .flake8
├─ README.md                       # Этот файл
├─ pyproject.toml                  # Конфигурация Poetry
├─ poetry.lock
├─ requirements.txt                # Для совместимости с pip
├─ manage.py                       # Точка входа Django
├─ draft.py / draft.json            # Вспомогательные скрипты (не влияют на приложение)
├─ config/                         # Настройки Django проекта
│   ├─ __init__.py
│   ├─ asgi.py
│   ├─ wsgi.py
│   ├─ settings.py                 # Основные настройки (DATABASES, INSTALLED_APPS, JWT, Celery)
│   ├─ celery.py                   # Конфигурация Celery
│   └─ urls.py                     # Корневой URL‑router
├─ habits/                         # Приложение «привычки»
│   ├─ __init__.py
│   ├─ apps.py
│   ├─ admin.py
│   ├─ models.py                   # Модели Habit, HabitLog и др.
│   ├─ serializers.py              # DRF‑сериализаторы
│   ├─ views.py                    # ViewSets / API‑эндпоинты
│   ├─ urls.py                     # URL‑router для habits
│   ├─ validators.py               # Валидация входных данных
│   ├─ paginators.py               # Пагинация ответов
│   ├─ tasks.py                    # Фоновые задачи (Celery)
│   ├─ tests.py                    # Тесты приложения habits
│   └─ migrations/                 # Миграции Django
├─ users/                          # Приложение «пользователи»
│   ├─ __init__.py
│   ├─ apps.py
│   ├─ admin.py
│   ├─ models.py                   # Пользовательская модель (CustomUser)
│   ├─ serializers.py              # Сериализаторы для регистрации, токенов и профиля
│   ├─ views.py                    # API‑эндпоинты (регистрация, аутентификация, профиль)
│   ├─ urls.py                     # URL‑router для users
│   ├─ paginators.py
│   ├─ tests.py                    # Тесты приложения users
│   ├─ management/                 # Пользовательские manage‑commands
│   │   ├─ __init__.py
│   │   └─ commands/
│   │       ├─ __init__.py
│   │       ├─ custom_csu.py        # Пример кастомной команды
│   │       └─ dropcreatedb.py      # Очистка базы (для разработки)
│   └─ migrations/                 # Миграции пользователей
└─ media/                          # Статические файлы (аватарки пользователей и пр.)
    └─ users/avatars/default_ava.png
```

## API (коротко)
- **/api/auth/** – аутентификация (получить JWT, обновление токенов)
- **/api/users/** – CRUD для профилей пользователей
- **/api/habits/** – управление привычками (list, create, update, delete, логирование)

Для полной документации см. `api_schema.yaml` (если присутствует) или откройте `/swagger/` (если включён `drf‑yasg`).

## Тесты
```bash
pytest                # Запуск всех тестов
```

## Вклад в проект
1. Форкните репозиторий
2. Создайте ветку `feature/your-feature`
3. Сделайте изменения и запустите тесты
4. Откройте Pull Request

---
*Данный README создан автоматически.*
