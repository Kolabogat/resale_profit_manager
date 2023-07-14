from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import (
    Model,
    CharField,
    DateTimeField,
    IntegerField,
    ForeignKey,
    PROTECT,
    BooleanField,
    FloatField,
)


CURRENCY = (
    ('$', '$'),
    ('€', '€'),
    ('₽', '₽'),
    ('₴', '₴'),
    ('L', 'L'),
)

PAGINATION = (
    ('5', '5'),
    ('10', '10'),
    ('15', '15'),
    ('25', '25'),
    ('50', '50'),
    ('100', '100'),
    ('200', '200'),
)


class UserSettings(Model):
    class Meta:
        verbose_name = 'User Settings'
        verbose_name_plural = 'User Settings'
        ordering = ['user']

    user = ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='User', on_delete=PROTECT, related_name='user_settings')

    paginate_by = CharField(verbose_name='Pagination', max_length=50, choices=PAGINATION, default='10')
    currency = CharField(verbose_name='Currency', max_length=50, choices=CURRENCY, default='$')
    display_symbol = BooleanField(verbose_name='Display symbol', default=False)
    delete_confirmation = BooleanField(verbose_name='Delete confirmation', default=True)

    def get_absolute_url(self):
        return reverse('account_profile', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.user)


class UserProfile(Model):
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profile'
        ordering = ['user']

    user = ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='User', on_delete=PROTECT, related_name='user_profile')

    all_time_profit = FloatField(verbose_name='Profit', default=0)
    tickets_quantity = IntegerField(verbose_name='Quantity', default=0)
    highest_profit = FloatField(verbose_name='Highest profit', default=0)
    highest_loss = FloatField(verbose_name='Highest loss', default=0)

    def get_absolute_url(self):
        return reverse('account_profile', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.user)
