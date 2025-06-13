from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator

username_validators = [UnicodeUsernameValidator(), MinLengthValidator(limit_value=6)]
