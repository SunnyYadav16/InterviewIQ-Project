import os

from celery import Celery

# set default Django settings module for celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "InterviewIQ.settings")

app = Celery("InterviewIQ")

# Load task modules from all registered Django app configs.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"

app.conf.beat_schedule = {}

app.conf.task_routes = {}
app.conf.task_annotations = {}

app.autodiscover_tasks()
