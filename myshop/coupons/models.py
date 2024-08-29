from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Coupon(models.Model):
    code = models.CharField(
        verbose_name='Промокод',
        max_length=50,
        unique=True
    )
    valid_from = models.DateTimeField(verbose_name='Действителен с')
    valid_to = models.DateTimeField(verbose_name='действителен до')
    discount = models.IntegerField(
        verbose_name='Размер скидки',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Процент скидки (0 - 100)'
    )
    active = models.BooleanField(verbose_name='Активен')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'
