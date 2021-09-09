from django.db import models

from CashBox import service


class Service(models.Model):
    haircut = models.OneToOneField('MaleHaircut', blank=True, on_delete=models.CASCADE)
    coloration = models.OneToOneField('Coloration', blank=True, on_delete=models.CASCADE)
    manicure = 'M'
    cosmetology = 'COS'
    braiding = 'B'
    hairdo = 'HD'


class Client(models.Model):
    name = models.CharField('Имя', max_length=15, blank=True)
    datetime = models.TimeField('Дата посещения', auto_now_add=True)
    t_number = models.SmallIntegerField('Номер телефона', unique=True)


# class Coloration(models.Model):
#     hair_length = models.CharField(max_length=7, choices=service.price_list.HAIR_LENGTH)
#     type = None
