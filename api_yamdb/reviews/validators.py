from datetime import date

from django.core.exceptions import ValidationError


def validate_year(year):
    """Проверяет, что указанный год не в будущем
             и не до большого взрыва"""

    current_year = date.today().year
    if year > current_year:
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
