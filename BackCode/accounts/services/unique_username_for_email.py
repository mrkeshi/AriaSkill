from django.contrib.auth import get_user_model

def unique_username_from_email(email):
    base = email.split('@')[0].replace('.', '_') or 'user'
    username = base
    counter = 1

    while User.objects.filter(username=username).exists():
        username = f'{base}_{counter}'
        counter += 1

    return username