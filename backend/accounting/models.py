from django.urls import reverse

from django.db.models import (
    Model,
    CharField,
    DateTimeField,
    IntegerField,
    ForeignKey,
    PROTECT,
)


class Operation(Model):
    title = CharField(max_length=150, verbose_name='Title')
    bought = IntegerField(default=0)
    sold = IntegerField(blank=True)
    profit = IntegerField(blank=True)
    category = ForeignKey('Category', on_delete=PROTECT, verbose_name='Category')
    created_at = DateTimeField(auto_now=True, verbose_name='Date of creation')
    closed_at = DateTimeField(verbose_name='Closing date')

    class Meta:
        verbose_name = 'Operation'
        verbose_name_plural = 'Operations'
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('view_operations', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


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

