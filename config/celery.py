import os
from celery import Celery
from platformshconfig import Config
import logging

logger = logging.getLogger(__name__)

config = Config()

if (
    not os.getenv('CI')
    and not config.variable('BUILD')
    and os.getenv('PLATFORM_APPLICATION_NAME')
):
    creds = config.credentials('queue_sms')
    user = creds['username']
    host = creds['host']
    port = str(creds['port'])
    password = creds['password']
    url = f'amqp://{user}:{password}@{host}:{port}/'

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    queue_sms = Celery('tasks', broker=url)

    # Using a string here means the worker doesn't have to serialize
    # the configuration object to child processes.
    # - namespace='CELERY' means all celery-related configuration keys
    #   should have a `CELERY_` prefix.

    # TODO: Test if we are using this. Came from boilerplate
    queue_sms.config_from_object('django.conf:settings', namespace='CELERY')

    # Load task modules from all registered Django queue_smss.
    queue_sms.autodiscover_tasks()

else:
    queue_sms = Celery('tasks')
    queue_sms.autodiscover_tasks()

    print(
        'Celery is not configured to run in this environment. Tasks will not'
        ' exist and you may see errors such as \'NoneType\' object has no'
        ' attribute \'delay\' when you attempt to run tasks.')

__all__ = ['queue_sms']
