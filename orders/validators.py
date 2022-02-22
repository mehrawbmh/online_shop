from rest_framework.exceptions import ValidationError


def check_positive_not_zero(number):
    if number <= 0:
        raise ValidationError("This field should be greater than zero!")
    return True
