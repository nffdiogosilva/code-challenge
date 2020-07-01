from django.conf import settings


DEFAULT_SCALAR_VALUES = {
    'buy': 1,
    'neutral': 0,
    'strong_buy': 1.5,
    'sell': -1,
    'strong_sell': -1.5,
    'positive': 1,
    'negative': -1,
}

SCALAR_VALUES = getattr(settings, 'SCALAR_VALUES', DEFAULT_SCALAR_VALUES)


def clean_to_grade(to_grade):
    """
    If given to_grade not found in SCALAR VALUES keys 
    then set a default value "Everything Else".
    """
    return to_grade if to_grade.lower() in SCALAR_VALUES.keys() else 'Everything Else'


def get_scalar_value(to_grade):
    """
    Function responsible of mapping the "to_grade" field into a scalar value.
    If key not found return 0 as the default value, that represents "Everything Else".
    """
    return SCALAR_VALUES.get(to_grade.lower(), 0)
