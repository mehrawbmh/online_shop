from django.core.exceptions import ValidationError
from .utils import phone_normalize


def is_11_characters(phone):
    """
    Notice that before this validator, a normalizer has implemented on all  phone numbers
    :param phone:
    :return: True if it has 11 digits else False
    """
    phone = phone_normalize(phone)
    if not len(phone) == 11:
        raise ValidationError("phone number length is not valid!")
    return True


def is_all_digit(phone: str):
    phone = phone_normalize(phone)
    if not phone.isdigit():
        raise ValidationError("Phone number must be all digit!")
    return True


def startswith_09(phone):
    phone = phone_normalize(phone)
    if not phone.startswith('09'):
        raise (ValidationError("Phone number is invalid!"))
    return True


def check_all_phone_validations(phone: str):
    return startswith_09(phone) and is_all_digit(phone) and is_11_characters(phone)
