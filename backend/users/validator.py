from django.core.exceptions import ValidationError


def validate_no_me(value):
    if 'me' in value.lower():
        raise ValidationError('Логин "me" запрещён.')
