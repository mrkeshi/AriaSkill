import re


def check_string_type(value):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    username_pattern = r'^[a-zA-Z0-9_.-]+$'

    if re.fullmatch(email_pattern, value):
        return 'Email'
    elif re.fullmatch(username_pattern, value):
        return 'Username'
    else:
        return 'None'

