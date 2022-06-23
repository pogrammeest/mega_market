# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-krivg-gflbp8btf5k0=c5b$z!ez^uuck))@@eplss)*$*te!gh'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'yndx_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }
}
