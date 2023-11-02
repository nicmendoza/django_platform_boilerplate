import pytest
import analytics


@pytest.fixture(autouse=True)
def no_analytics(monkeypatch):
    """
        Remove analytics.track and analytics.identify for all tests.

        TODO: See if we can upgrade this to use mock.patch so we can check the
        contents of the calls and test our analytics cases
    """

    def mock_identify(*args, **kwargs):
        return None

    def mock_track(*args, **kwargs):
        return None

    monkeypatch.setattr(analytics, "identify", mock_identify)
    monkeypatch.setattr(analytics, "track", mock_track)


def pytest_configure(config):
    from django.conf import settings
    settings._called_from_test = True

    # OVERRIDE config.settings values for tests here
    settings.ADMIN_EMAIL = 'test@test.com'
    settings.ADMIN_PASSWORD = 'testpass12345'
    settings.TWILIO_ACCOUNT_SID = 'Fake'
    settings.TWILIO_AUTH_TOKEN = 'Fake'
    # TODO: Get celery test runner working so we can test tasks, presumably not
    # have to monkeypatch them
    # settings.TEST_RUNNER = (
    # 'djcelery.contrib.test_runner.CeleryTestSuiteRunner')  noqa
    # settings.CELERY_ALWAYS_EAGER = True


def pytest_unconfigure(config):
    from django.conf import settings  # This was missing from the manual
    del settings._called_from_test
