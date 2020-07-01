from django.conf import settings
from django.db import models


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


class Company(models.Model):
    SECTOR_TYPES_CHOICES = (
        ('',''),
    )
    sector = models.CharField(max_length=20, choices=SECTOR_TYPES_CHOICES)
    address = models.CharField('address', max_length=50)
    ticker = models.OneToOneField('Ticker', on_delete=models.CASCADE)
    short_name = models.CharField('short Name', max_length=20)

    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    def __str__(self):
        return f'{self.pk} - Company: {self.short_name}, Ticker: {self.ticker}'


class DailyPrice(models.Model):
    open_value = models.FloatField('open')
    high_value = models.FloatField('high')
    low_value = models.FloatField('low')
    close_value = models.FloatField('close')
    volume = models.IntegerField('volume') # FIXME: should this be a BigIntegerField?

    company = models.ForeignKey('Company', related_name='daily_prices', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'daily price'
        verbose_name_plural = 'daily prices'

    def __str__(self):
        return f'{self.pk} - Daily Price: {self.short_name}, Ticker: {self.ticker}'


class Recommendation(models.Model):
    # TODO: remove this redundancy. Make compreension list?
    GRADE_CHOICES = (
        ('buy', 'Buy'),
        ('neutral', 'Neutral'),
        ('strong_buy', 'Strong Buy'),
        ('sell', 'Sell'),
        ('strong_sell', 'Strong Sell'),
        ('positive', 'Positive'),
        ('everything_else', 'Everything Else')
    )
    to_grade = models.CharField('to grade', max_length=20, choices=GRADE_CHOICES, default='everything_else')
    scalar = models.FloatField('scalar', editable=False)
    daily_price = models.ForeignKey('DailyPrice', related_name='recommendations', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'recommendation'
        verbose_name_plural = 'recommendations'

    def __str__(self):
        return f'{self.pk} - Recommendation: {self.to_grade}, Scalar Value: {self.scalar_value}'

    def save(self, *args, **kwargs):
        # Everytime the object is saved, the scalar value is updated
        # based on the any change it might happen on to_grade value.
        self.scalar = self.get_scalar_value()
        super().save(*args, **kwargs)

    def get_scalar_value(self):
        """
        Method responsible of mapping the "to_grade" field into a scalar value.
        If key not found return 0 as the default value, that represents "Everything Else".
        """
        scalar_value = 0

        if self.to_grade in SCALAR_VALUES:
            scalar_value = SCALAR_VALUES[self.to_grade]

        return scalar_value


class Ticker(models.Model):
    name = models.CharField('name', max_length=50)

    class Meta:
        verbose_name = 'ticker'
        verbose_name_plural = 'tickers'

    def __str__(self):
        return f'{self.pk} - Ticker: {self.name}'

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)
