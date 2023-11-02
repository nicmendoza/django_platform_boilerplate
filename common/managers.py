import logging
from django.contrib.auth.base_user import BaseUserManager

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        logger.info(f'creating superuser with email: {email}')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Super Admin must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Super Admin must have is_superuser=True.')

        user = self._create_user(email, password, **extra_fields)

        return user
