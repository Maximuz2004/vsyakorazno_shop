import os

from celery import Celery

from django.conf import settings

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'myshop.settings'
)
app = Celery('myshop', broker='pyamqp://guest@localhost//')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
