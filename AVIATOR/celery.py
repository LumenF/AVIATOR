import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AVIATOR.settings')

app = Celery('AVIATOR')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.control.purge()
app.autodiscover_tasks()
