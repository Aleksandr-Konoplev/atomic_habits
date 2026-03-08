from datetime import timedelta
from pathlib import Path
import os

from celery.schedules import crontab
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True if os.getenv('DEBUG') == 'True' else False

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Library
    'rest_framework',
    'django_filters',
    'rest_framework_simplejwt',
    'django_celery_beat',
    'corsheaders',
    # My app
    'users',
    'habits',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ---------------------------- Настройки базы данных -------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('NAME'),
        'USER': os.getenv('USER'),
        'PASSWORD': os.getenv('PASSWORD'),
        'HOST': os.getenv('HOST'),
        'PORT': os.getenv('PORT'),
    }
}

# ------------------------- Валидаторы сложности пароля ----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
# ----------------------- Модель аутентификации пользователя -----------------------
AUTH_USER_MODEL = 'users.User'
# ----------------------------------------------------------------------------------

# ---------------------------- Глобальные настройки API ----------------------------
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
# ----------------------------------------------------------------------------------

# ------------------- Настройки время жизни и обновления токена --------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}
# ----------------------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')

# ------------------------------- Настройки Celery ---------------------------------
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

CELERY_TIMEZONE = TIME_ZONE
# CELERY_TASK_TRACK_STARTED = True

# Лимит времени на выполнение задачи (в секундах)
CELERY_TASK_TIME_LIMIT = 10 * 60

# Класс планировщика, который использует Celery Beat для периодических задач
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Вызов задач
CELERY_BEAT_SCHEDULE = {
    'send-habit-reminders-every-minute': {
        'task': 'habits.tasks.send_habit_reminders',
        'schedule': crontab(),  # каждую минуту
    },
}
# ----------------------------------------------------------------------------------

# -------------------------------- Настройки Cors ----------------------------------
# Адреса разрешённых фронтенд-серверов
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
]

# Разрешённые адреса не блокируемые CSRF-защитой (фронт и бэк)
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
]

CORS_ALLOW_ALL_ORIGINS = False
# ----------------------------------------------------------------------------------