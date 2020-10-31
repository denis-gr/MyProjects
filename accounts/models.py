from django.db.models import EmailField
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = EmailField("E-mail", unique=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
