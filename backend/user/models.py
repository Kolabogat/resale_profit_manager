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
    CASCADE,
)


class CommandPagination(Model):
    paginate_by = IntegerField(verbose_name='Paginate By')

    def __str__(self):
        return str(self.paginate_by)

    @classmethod
    def get_default_pk(cls):
        paginate_by, created = cls.objects.get_or_create(
            pk=2,
            defaults=dict(pk=2, paginate_by=10),
        )
        return paginate_by.pk


class CommandCurrency(Model):
    currency = CharField(max_length=10, verbose_name='Currency')

    def __str__(self):
        return str(self.currency)

    @classmethod
    def get_default_pk(cls):
        currency, created = cls.objects.get_or_create(
            pk=1,
            defaults=dict(pk=1, currency='$'),
        )
        return currency.pk


class UserSettings(Model):
    class Meta:
        verbose_name = 'User Settings'
        verbose_name_plural = 'User Settings'
        ordering = ['user']

    user = ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='User', on_delete=PROTECT, related_name='user_settings')

    paginate_by = ForeignKey(to='CommandPagination', verbose_name='Pagination', max_length=50, on_delete=CASCADE, default=CommandPagination.get_default_pk, related_name='command_pagination')
    currency = ForeignKey(to='CommandCurrency', verbose_name='Currency', on_delete=CASCADE, default=CommandCurrency.get_default_pk)
    display_symbol = BooleanField(verbose_name='Display symbol', default=False)
    delete_confirmation = BooleanField(verbose_name='Delete confirmation', default=True)

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

    def __str__(self):
        return str(self.user)


