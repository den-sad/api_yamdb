from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(year):
    """Проверяет, что указанный год не в будущем
             и не до большого взрыва"""

    date = timezone.localtime(timezone.now()).strftime('%Y')
    if year > int(date):
        raise ValidationError(
            (f'Указанный год ({year}) ещё не наступил'),
            params={'value': year},
        )
    if year < -14000000000:
        raise ValidationError(
            (f'В указанный год ({year}) наша вселенная вероятно '
             f'ещё не существовала'),
            params={'value': year},
        )
