"""
Django settings for cafe_manager project.
Updated for Static files and custom Template paths.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f-#+sn8=ovbwmg^to#83hb6r-b-n^a@6lovd7w&)1%kqh5k8wn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps
    'core',
    # Third-party
    'jalali_date',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cafe_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # اصلاح مسیر تمپلیت‌ها با توجه به ساختار پوشه‌بندی شما
        'DIRS': [os.path.join(BASE_DIR, 'core', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cafe_manager.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation - غیرفعال شده برای راحتی در محیط توسعه
AUTH_PASSWORD_VALIDATORS = []


# Internationalization
LANGUAGE_CODE = 'fa-ir' # تغییر به فارسی برای اعداد و تقویم بهتر

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# اضافه کردن مسیر پوشه استاتیک در ریشه اصلی پروژه
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# مسیر ذخیره فایل‌های استاتیک در هنگام استقرار (اختیاری برای الان)
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Media files (Images for Menu Items)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Auth Redirects
LOGIN_REDIRECT_URL = '/dashboard/'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'