#Generated from Chef, do not modify
from bdpindex.settings_changeme import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bdphpc',
        'USER': 'postgres',
        'PASSWORD': 'randompasswordkadsgjadsgj', # unused with ident auth
        'HOST': '',
        'PORT': '',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'timestamped': {
            'format': '%(asctime)s-%(filename)s-%(lineno)s-%(levelname)s: %(message)s'
        },
    },

    'handlers': {
        'file': {
            'level':'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/bdp/bdpindex.log',
            'formatter': 'timestamped'
        },
    },

    'loggers': {
        'bdpindex.searchengine': {
            'handlers': ['file'],
            'level': 'INFO',
            },
        },
}

