from django.db import models

class Table(models.Model):
    STATUS_CHOICES = [
        ('busy', 'Занят'),
        ('free', 'Свободен'),
    ]

    number_of_seats = models.IntegerField(verbose_name='Количество мест')
    is_free = models.CharField(verbose_name='Занятость стола', max_length=10, choices=STATUS_CHOICES, default='free')

    class Meta:
        ordering = ('id',)

    def __str__(self) -> str:
        return f'{self.id}'