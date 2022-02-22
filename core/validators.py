from django.core.exceptions import ValidationError


def is_11_characters(phone):
    """
    Notice that before this validator, a normalizer has implemented on all  phone numbers
    :param phone:
    :return: True if it has 11 digits else False
    """
    if not len(phone) == 11:
        raise ValidationError("phone number length is not valid!")


def is_all_digit(phone: str):
    if not phone.isdigit():
        raise ValidationError("Phone number must be all digit!")


def startswith_09(phone):
    if not phone.startwith('09'):
        raise(ValidationError("Phone number is invalid!"))
