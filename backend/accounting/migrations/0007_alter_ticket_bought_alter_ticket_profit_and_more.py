# Generated by Django 4.2.2 on 2023-07-01 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0006_alter_ticket_closed_alter_ticket_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='bought',
            field=models.FloatField(default=0, verbose_name='Bought'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='profit',
            field=models.FloatField(blank=True, null=True, verbose_name='Profit'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='sold',
            field=models.FloatField(blank=True, null=True, verbose_name='Sold'),
        ),
    ]
