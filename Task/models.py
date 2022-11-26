from django.db import models
from django.db.models.signals import pre_save

from .validators import UnicodeUsernameValidator
from django.contrib.auth.hashers import make_password, check_password


class TaskUserManager(models.Manager):

    def create_task_user(self, username, password, email=None, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username, password=password, email=email, **extra_fields)
        user.save()
        return user


# Create your models here.
class TaskUSer(models.Model):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    password = models.CharField(max_length=128)
    email = models.EmailField(blank=True)

    REQUIRED_FIELDS = ('password',)
    USERNAME_FIELD = 'username'

    objects = TaskUserManager()

    def __str__(self):
        return str(self.username)

    def validiate_password(self, raw_password):
        password = check_password(raw_password, self.password)
        return password

    @property
    def is_authenticated(self):
        return True


def pre_hash_password(sender, instance, *args, **kwargs):
    instance.password = make_password(instance.password)


pre_save.connect(pre_hash_password, sender=TaskUSer)
