DEFAULT_IMAGE = 'user_image/(default).png'

from django.db.models import ImageField, EmailField
from django.contrib.auth.models import AbstractUser

def get_image_path(model, filename):
    temp = filename.split('.')[-1]
    return f'user_image/{model.pk}.{temp}'


class User(AbstractUser):
    avatar = ImageField(
        'Аватар',
        upload_to=get_image_path,
        default=DEFAULT_IMAGE)
    email = EmailField("E-mail", unique=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
