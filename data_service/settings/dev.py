from data_service.base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'info': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'formatter': 'verbose',
        },
        'error': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'formatter': 'verbose',
        },
        'django.db.backends': {
             'handlers': ['console'],
             'propagate': True,
             'level': 'DEBUG',
         },
    },
}

DATABASES = {
    # 'default': {
    #     'STORAGE_ENGINE': 'MyISAM / INNODB / ETC',
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'data_service',
    #     'USER': 'datawarehouse',
    #     'PASSWORD': '9QRrwR2C*ur&1[}2h-[Z',
    #     'HOST': '192.168.3.237',
    #     'PORT': '3306',
    # },
    # 'lingoacedw': {
    #     'STORAGE_ENGINE': 'MyISAM / INNODB / ETC',
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'lingoacedw',
    #     'USER': 'datawarehouse',
    #     'PASSWORD': '9QRrwR2C*ur&1[}2h-[Z',
    #     'HOST': '192.168.3.237',
    #     'PORT': '3306',
    # },
    'default': {
        'STORAGE_ENGINE': 'MyISAM / INNODB / ETC',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ng_webapp',
        'USER': 'lingoace',
        'PASSWORD': 'DB4lingo.com',
        'HOST': 'localhost',
        'PORT': '3306',
        # 'ATOMIC_REQUESTS': True,
        # 'CONN_MAX_AGE': 600,
    },
    'lingoacedw': {
        'STORAGE_ENGINE': 'MyISAM / INNODB / ETC',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lingoacedb',
        'USER': 'lingoace',
        'PASSWORD': 'DB4lingo.com',
        'HOST': 'localhost',
        'PORT': '3306',
        # 'CONN_MAX_AGE': 3600,
    },
}

