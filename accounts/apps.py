from django.contrib.auth.apps import AuthConfig as AuthConfigOld


class AccountsConfig(AuthConfigOld):
    name = 'accounts'
    verbose_name = 'Пользователи'
