from django.urls import reverse
from django.conf import settings
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


CHOICES = [
    ('False', 'No'),
    ('True', 'Yes'),
]


class Ticket(Model):
    user = ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='User', on_delete=PROTECT)

    title = CharField(max_length=150, verbose_name='Title')
    closed = CharField(max_length=100, choices=CHOICES, verbose_name='Closed', default='False')
    bought = FloatField(default=0, verbose_name='Bought')
    sold = FloatField(blank=True, null=True, verbose_name='Sold')
    profit = FloatField(blank=True, null=True, verbose_name='Profit')
    category = ForeignKey('Category', on_delete=PROTECT, verbose_name='Category', blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True, verbose_name='Date of creation')
    closed_at = DateTimeField(auto_now=True, blank=True, null=True, verbose_name='Closing date')
    deleted = CharField(max_length=100, choices=CHOICES, verbose_name='Deleted', default='False')

    def get_update_url(self):
        return reverse('update_ticket', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('delete_ticket', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = ['-created_at']


class Category(Model):
    title = CharField(max_length=150, db_index=True, verbose_name='Categories')

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['title']


