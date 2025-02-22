from backend.settings import *

SECRET_KEY = 'sadfuheqwekrm'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}