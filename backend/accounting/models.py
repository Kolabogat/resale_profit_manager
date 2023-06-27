from django.urls import reverse

from django.db.models import (
    Model,
    CharField,
    DateTimeField,
    IntegerField,
    ForeignKey,
    PROTECT,
    BooleanField,
)


CHOICES = [
    ('False', 'No'),
    ('True', 'Yes'),
]


class Ticket(Model):
    title = CharField(max_length=150, verbose_name='Title')
    closed = CharField(max_length=100, choices=CHOICES, verbose_name='Closed', default='False')
    bought = IntegerField(default=0, verbose_name='Bought', help_text='The price is the value divided by 100 (848 = 8,48 $)')
    sold = IntegerField(blank=True, null=True, verbose_name='Sold', help_text='902 = 9,02 $')
    profit = IntegerField(blank=True, null=True, verbose_name='Profit', help_text='54 = 0,54 $')
    category = ForeignKey('Category', on_delete=PROTECT, verbose_name='Category')
    created_at = DateTimeField(auto_now_add=True, verbose_name='Date of creation')
    closed_at = DateTimeField(blank=True, null=True, verbose_name='Closing date')

    def get_absolute_url(self):
        return reverse('view_operations', kwargs={'pk': self.pk})

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

