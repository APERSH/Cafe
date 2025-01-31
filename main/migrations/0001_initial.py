# Generated by Django 5.1.5 on 2025-01-15 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_seats', models.IntegerField(verbose_name='Количество мест')),
                ('is_free', models.CharField(choices=[('busy', 'Занят'), ('free', 'Свободен')], default='free', max_length=10, verbose_name='Занятость стола')),
            ],
        ),
    ]
