from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator

username_validators = [UnicodeUsernameValidator(), MinLengthValidator(limit_value=6)]


def validate_audio_ext(value):
    """Thanks to the https://stackoverflow.com/a/27081099/22892730"""
    import os
    from django.core.exceptions import ValidationError

    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.wav', '.mpeg', '.mp3']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Unsupported file extension.')
