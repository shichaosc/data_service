from data_service.base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(funcName)s %(lineno)d:%(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'info_file': {
            'class': 'base.log_handler.HxTimedRotatingFileHandler',
            'filename': '/data/logs/data_service/info.log',
            'when': 'midnight',
            # 时间间隔
            'interval': 1,
            'formatter': 'verbose',
        },
        'error_file': {
            'class': 'base.log_handler.HxTimedRotatingFileHandler',
            'filename': '/data/logs/data_service/error.log',
            'when': 'midnight',
            # 时间间隔
            'interval': 1,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'info': {
            'handlers': ['info_file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'error': {
            'handlers': ['error_file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
    },
}

DATABASES = {
    'default': {
        'STORAGE_ENGINE': 'MyISAM / INNODB / ETC',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'data_service',
        'USER': 'datawarehouse',
        'PASSWORD': '9QRrwR2C*ur&1[}2h-[Z',
        'HOST': 'localhost',
        'PORT': '3306',
    },
    'lingoacedw': {
        'STORAGE_ENGINE': 'MyISAM / INNODB / ETC',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lingoacedw',
        'USER': 'datawarehouse',
        'PASSWORD': '9QRrwR2C*ur&1[}2h-[Z',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
