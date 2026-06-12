from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def normalize_url(value):
    value = (value or '').strip()
    if not value:
        return ''

    if not value.startswith(('http://', 'https://')):
        value = f'https://{value}'

    try:
        URLValidator()(value)
    except ValidationError:
        raise serializers.ValidationError('Enter a valid URL.')

    return value