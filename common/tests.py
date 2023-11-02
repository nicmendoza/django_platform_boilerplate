import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from common.constants import (
    ChoicesEnum
)


User = get_user_model()


@pytest.mark.django_db
class TestCommon:
    def test_something(self):
        User.objects.create_user(
            email="normal@user.com", password="foo"
        )


class TestConstants:
    def test_choices_enum(self):
        class Choices(ChoicesEnum):
            ONE = 'one'
            TWO = 'two'

        assert Choices.values() == [
            'one', 'two'
        ]

        assert Choices.keys() == [
            'ONE', 'TWO'
        ]

        # TODO: not sure _value_ is ever set
        assert str(Choices) == "<class 'common.tests.TestConstants.test_choices_enum.<locals>.Choices'>"  # noqa


class TestManagers:
    def test_superuser_validation(self):
        with pytest.raises(ValueError):

            User.objects.create_superuser(
                is_staff=False,
                email='whatever', password='whatever'
            )

        with pytest.raises(ValueError):

            User.objects.create_superuser(
                is_superuser=False,
                email='whatever', password='whatever'
            )


@pytest.mark.django_db
class TestModels:
    def test_timestamped_model(self):

        test_object = User.objects.create_user(
                is_superuser=False,
                email='whatever', password='whatever'
            )

        assert test_object.first_name == 'Name 1'

        test_object.update(name='Name 2')
        assert test_object.first_name == 'Name 2'

        test_object.update({'name': 'Name 3'})
        assert test_object.first_name == 'Name 3'

    def test_user_custom_methods(self):

        user = User.objects.create()
        assert user.full_name == ''
        assert user.display_name == '+161712354567'

        user.update(email='person@site.com')
        assert user.full_name == ''
        assert user.display_name == 'person@site.com'

        user.update(first_name='First')
        assert user.full_name == 'First'
        assert user.display_name == 'First'

        user.update(last_name='Last')
        assert user.full_name == 'First Last'
        assert user.display_name == 'First Last'

        assert str(user) == 'First Last'

        user.update(first_name='')
        assert user.full_name == 'Last'
        assert user.display_name == 'Last'
