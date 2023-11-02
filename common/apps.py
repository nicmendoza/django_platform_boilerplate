import os
import sys
from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import analytics

from platformshconfig import Config
config = Config()


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'

    def ready(self):

        is_build_env = config.variable('BUILD')
        is_ci_env = os.getenv('CI')
        is_test_run = "pytest" in sys.modules  # hardly bulletproof

        if (
            not is_build_env
            and not is_ci_env
        ):

            if not is_test_run:
                # only configure signals if we are NOT in a test run
                from . import signals  # noqa

            if not settings.SEGMENT_WRITE_KEY:
                raise ImproperlyConfigured('Segment write key not configured!')

            analytics.write_key = settings.SEGMENT_WRITE_KEY
