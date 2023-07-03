from django.db import models
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
    ('USD', '$'),
    ('EUR', '€'),
    ('RUB', '₽'),
    ('UAH', '₴'),
    ('MDL', 'L'),
)

PAGINATION = (
    ('10', '10'),
    ('15', '15'),
    ('25', '25'),
    ('50', '50'),
    ('100', '100'),
)


class UserAdditional(Model):
    class Meta:
        verbose_name = 'Additional User Settings'
        verbose_name_plural = 'Additional User Settings'
        # ordering = ['user']

    # user = ForeignKey(User)
    # currency = CharField(choices=CURRENCY)
    paginate_by = CharField(verbose_name='Pagination', max_length=50, choices=PAGINATION, default='10')
