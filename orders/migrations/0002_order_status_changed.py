# Generated by Django 5.1.5 on 2025-01-20 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status_changed',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата изменения статуса'),
        ),
    ]
