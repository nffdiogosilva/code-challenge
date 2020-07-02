import datetime

from django.db import models

from django_pandas.managers import DataFrameManager


class Company(models.Model):
    SECTOR_TYPES_CHOICES = (
        ('it', 'IT'),
        ('finance', 'Finance'),
        # TOOD: add other sectors
    )
    ticker = models.CharField('Ticker', max_length=10, primary_key=True)
    short_name = models.CharField('short Name', max_length=50)
    sector = models.CharField(max_length=20, choices=SECTOR_TYPES_CHOICES)
    address = models.CharField('address', max_length=50)

    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    def __str__(self):
        return f'{self.pk}'


class DailyPrice(models.Model):
    created_at = models.DateField('created_at')
    open_value = models.FloatField('open')
    high_value = models.FloatField('high')
    low_value = models.FloatField('low')
    close_value = models.FloatField('close')
    volume = models.IntegerField('volume') # FIXME: should this be a BigIntegerField?
    company = models.ForeignKey('Company', related_name='daily_prices', on_delete=models.CASCADE)

    objects = DataFrameManager()

    class Meta:
        verbose_name = 'daily price'
        verbose_name_plural = 'daily prices'
        unique_together = ('created_at', 'company')

    def __str__(self):
        return f'DP ({self.pk}): {self.created_at}'


class Recommendation(models.Model):
    created_at = models.DateTimeField(default=datetime.datetime.now)
    to_grade = models.CharField('to grade', max_length=20)
    scalar = models.FloatField('scalar')
    daily_price = models.ForeignKey('DailyPrice', related_name='recommendations', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'recommendation'
        verbose_name_plural = 'recommendations'

    def __str__(self):
        return f'R ({self.pk}): {self.to_grade} - {self.scalar}'
