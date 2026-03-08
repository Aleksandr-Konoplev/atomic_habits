# Atomic Habits

**Atomic Habits** – это Django‑приложение для управления привычками и задачами, предоставляющее REST‑API на базе Django REST Framework.

## Технологический стек
- **Python 3.14+**
- **Django 6.0.3**
- **Django REST Framework 3.16.1**
- **Celery 5.x** (фоновые задачи)
- **Redis** (брокер для Celery)
- **PostgreSQL** (основная БД)
- **JWT** (аутентификация через `djangorestframework-simplejwt`)
- **drf‑yasg** (Swagger / Redoc)
- **Poetry** (управление зависимостями)

## Возможности
- Регистрация и аутентификация пользователей через JWT.
- CRUD‑операции над привычками (приватные и публичные).
- Валидация длительности (≤ 120 сек) и периодичности (≤ 7 дней).
- Привязка приятных привычек/наград.
- Планировщик напоминаний через Celery, отправка сообщений в Telegram.
- **Celery Beat**: периодическое выполнение задачи `send_habit_reminders` каждую минуту.

## Установка
```bash
# Клонировать репозиторий
git clone <repo-url>
cd atomic_habits

# Установить зависимости через poetry
poetry install

# Скопировать пример файла переменных окружения и отредактировать
cp .env.example .env
# Отредактируйте .env, указав свои параметры БД и Telegram‑бота
```

## Переменные окружения (`.env`)
```dotenv
DEBUG=True                  # режим разработки
SECRET_KEY=your-secret-key
NAME=atomic_habits          # имя базы данных PostgreSQL
USER=postgres               # пользователь БД
PASSWORD=postgres           # пароль БД
HOST=localhost              # хост БД
PORT=5432                   # порт БД
TG_BOT_TOKEN=your_telegram_bot_token
```

## Запуск проекта
```bash
# Миграции базы
python manage.py migrate

# Создать суперпользователя (опционально)
python manage.py createsuperuser

# Запустить dev‑сервер Django
python manage.py runserver

# Запустить Celery worker (в отдельном терминале)
celery -A config.celery.app worker -l info

# Запустить Celery Beat (планировщик задач)
celery -A config.celery.app beat -l info
```

## Структура проекта
```
atomic_habits/                     # корневая директория проекта
├─ .git/                           # Git‑репозиторий
├─ .venv/                          # виртуальное окружение (не включено в репозиторий)
├─ .idea/                          # конфигурация PyCharm
├─ .gitignore
├─ .flake8
├─ README.md                       # этот файл
├─ pyproject.toml                  # конфигурация Poetry
├─ poetry.lock
├─ requirements.txt                # для совместимости с pip
├─ manage.py                       # точка входа Django
├─ config/                         # настройки Django проекта
│   ├─ __init__.py
│   ├─ asgi.py
│   ├─ wsgi.py
│   ├─ settings.py                 # основные настройки (DATABASES, INSTALLED_APPS, JWT, Celery)
│   ├─ celery.py                   # конфигурация Celery
│   └─ urls.py                     # корневой URL‑router
├─ habits/                         # приложение «привычки»
│   ├─ __init__.py
│   ├─ apps.py
│   ├─ admin.py
│   ├─ models.py                   # модели Habit, HabitLog и др.
│   ├─ serializers.py              # DRF‑сериализаторы
│   ├─ views.py                    # ViewSets / API‑эндпоинты
│   ├─ urls.py                     # URL‑router для habits
│   ├─ validators.py               # валидация полей
│   ├─ paginators.py               # пагинация ответов
│   ├─ tasks.py                    # фоновые задачи (Celery)
│   ├─ tests.py                    # тесты приложения habits
│   └─ migrations/                 # миграции Django
├─ users/                          # приложение «пользователи»
│   ├─ __init__.py
│   ├─ apps.py
│   ├─ admin.py
│   ├─ models.py                   # кастомная модель User
│   ├─ serializers.py              # сериализаторы для регистрации и профиля
│   ├─ views.py                    # API‑эндпоинты (регистрация, аутентификация, профиль)
│   ├─ urls.py                     # URL‑router для users
│   ├─ paginators.py
│   ├─ tests.py                    # тесты приложения users
│   └─ migrations/                 # миграции пользователей
└─ media/                          # статические файлы (аватарки пользователей и пр.)
    └─ users/avatars/default_ava.png
```

## API (коротко)
### Пользователи (`users/`)
| Метод | URL | Описание |
|------|-----|----------|
| `POST` | `/users/register/` | Регистрация нового пользователя (email + password). |
| `POST` | `/users/login/` | Получить JWT (access и refresh). |
| `POST` | `/users/token/refresh/` | Обновить access‑токен. |
| `GET`  | `/users/list/` | Список всех пользователей (только админ). |
| `GET`  | `/users/<int:pk>/detail/` | Получить данные пользователя. |
| `PATCH`| `/users/<int:pk>/update/` | Обновить данные пользователя (только владелец). |
| `DELETE`| `/users/<int:pk>/delete/` | Удалить пользователя (только владелец). |

#### Пример регистрации (curl)
```bash
curl -X POST http://127.0.0.1:8000/users/register/ \
     -H "Content-Type: application/json" \
     -d '{"email":"john@example.com","password":"StrongPass123","phone_number":"+79991234567"}'
```
#### Пример логина (curl)
```bash
curl -X POST http://127.0.0.1:8000/users/login/ \
     -H "Content-Type: application/json" \
     -d '{"email":"john@example.com","password":"StrongPass123"}'
```
Ответ (JSON):
```json
{ "access": "<jwt-access-token>", "refresh": "<jwt-refresh-token>" }
```

### Привычки (`habits/`)
| Метод | URL | Описание |
|------|-----|----------|
| `POST` | `/habits/create/` | Создать новую привычку (только аутентифицированный пользователь). |
| `GET`  | `/habits/my/list/` | Список привычек текущего пользователя. |
| `GET`  | `/habits/public/list/` | Список публичных привычек всех пользователей. |
| `GET`  | `/habits/<int:pk>/detail/` | Подробности о конкретной привычке (если публична или принадлежит пользователю). |
| `PATCH`| `/habits/<int:pk>/update/` | Обновить привычку (только владелец). |
| `DELETE`| `/habits/<int:pk>/delete/` | Удалить привычку (только владелец). |

#### Пример создания привычки (curl)
```bash
curl -X POST http://127.0.0.1:8000/habits/create/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <access-token>" \
     -d '{
          "action": "Пить воду",
          "duration": 60,
          "periodicity": 1,
          "is_pleasant": false,
          "award": "Кофе после недели",
          "is_publicity": true
     }'
```
Ответ (пример):
```json
{
  "id": 1,
  "owner": 2,
  "action": "Пить воду",
  "duration": 60,
  "periodicity": 1,
  "is_pleasant": false,
  "award": "Кофе после недели",
  "is_publicity": true,
  "place": null,
  "time": null,
  "related_pleasant_habit": null
}
```

#### Пример получения списка публичных привычек (curl)
```bash
curl http://127.0.0.1:8000/habits/public/list/ -H "Authorization: Bearer <access-token>"
```

## Документация API
- Swagger UI доступен по `http://127.0.0.1:8000/swagger/`
- Redoc доступен по `http://127.0.0.1:8000/redoc/`
- Документация генерируется библиотекой **drf‑yasg**.

## Тесты
```bash
pytest                # запуск всех тестов (на данный момент пустой набор)
```

## Вклад в проект
1. Форкните репозиторий
2. Создайте ветку `feature/your-feature`
3. Сделайте изменения и запустите тесты
4. Откройте Pull Request

---
## Автор

Konoplev Aleksandr  
Email: [konoplev.a.a0000@gmail.com](mailto:konoplev.a.a0000@gmail.com)  
GitHub: https://github.com/Aleksandr-Konoplev