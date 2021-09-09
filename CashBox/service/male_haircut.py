from django.db import models

from .price_list import HAIRCUTS
from ..models import Client


class MaleClient(Client):
    service = models.ManyToManyField('Service', through='MaleClientService')


class MaleHaircut(models.Model):
    type = models.PositiveSmallIntegerField('Тип', choices=HAIRCUTS)


class MaleClientService(models.Model):
    male_client = models.ForeignKey('MaleClient', on_delete=models.CASCADE)
    male_service = models.ForeignKey('Service', on_delete=models.CASCADE)