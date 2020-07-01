from django.db import models


class Company(models.Model):
    SECTOR_TYPES_CHOICES = (
        ('',''),
    )
    short_name = models.CharField('short Name', max_length=50)
    ticker = models.CharField('Ticker', max_length=20)
    sector = models.CharField(max_length=20, choices=SECTOR_TYPES_CHOICES)
    address = models.CharField('address', max_length=50)

    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    def __str__(self):
        return f'{self.pk} - Company: {self.short_name}, Ticker: {self.ticker}'


class DailyPrice(models.Model):
    created_at = models.DateField('created_at')
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
    to_grade = models.CharField('to grade', max_length=20)
    scalar = models.FloatField('scalar')
    daily_price = models.ForeignKey('DailyPrice', related_name='recommendations', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'recommendation'
        verbose_name_plural = 'recommendations'

    def __str__(self):
        return f'{self.pk} - Recommendation: {self.to_grade}, Scalar Value: {self.scalar_value}'
