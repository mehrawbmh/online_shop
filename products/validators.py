from django.core.exceptions import ValidationError


def is_positive(number):
    if number < 0:
        raise ValidationError("This field must be positive")
    return True


def check_percent_range(number):
    if number < 0 or number > 100:
        raise ValidationError("The percent is out of range!")
    return True
