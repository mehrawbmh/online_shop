def phone_normalize(phone: str):
    """
    normalizes all kind of phone numbers (for Iran)
    :param phone: with format of  starting with +98 or 0098 or 9 or 09
    :return: a phone number with format of 09*********
    """
    final_phone = phone
    if phone.startswith('9'):
        final_phone = '0' + phone
    elif phone.startswith('+989'):
        final_phone = '0' + phone[3:]
    elif phone.startswith('+980'):
        final_phone = phone[3:]
    elif phone.startswith('0098'):
        final_phone = '0' + phone[4:]
    persian_digits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']
    english_digits = [str(x) for x in range(0,10)]
    for pers, en in list(zip(persian_digits, english_digits)):
        final_phone.replace(pers, en)
    return final_phone



