from django.db import models
from django.contrib.auth.models import User

CURRENCY = (
    ('USD', '$'),
    ('EUR', '€'),
    ('RUB', '₽'),
    ('UAH', '₴'),
    ('MDL', 'L'),
)

# class UserAdditional():
#     user = ForeignKey(User)
#     currency =