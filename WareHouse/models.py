from django.db import models


class Material(models.Model):
    BRANDS = [
        ('Matrix', 'Матрикс'),
        ('Estel', 'Эстель'),
    ]
    brand = models.CharField('Бренд', max_length=32, choices=BRANDS, default='Matrix')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    number = models.ForeignKey('Number', max_length=256, on_delete=models.CASCADE, verbose_name='Номер')
    volume = models.PositiveSmallIntegerField('Объем', default=0)
    quantity = models.PositiveSmallIntegerField('Количество', default=0)
    tracked = models.BooleanField('Отслеживаемость', default=False)

    def add_material(self, packages, quantity):
        self.quantity += packages * self.volume + quantity
        self.tracked = True
        self.save()

    def expense(self, quantity):
        if self.quantity >= quantity:
            if self.quantity == quantity:
                self.tracked = False
            self.quantity -= quantity
            self.save()
        return self.quantity

    def needs_replenishment(self):
        return self.tracked and (self.quantity / self.volume < 2)

    def __str__(self):
        return f'{self.number}'


class Category(models.Model):
    name = models.CharField('Категория', max_length=256)

    def __str__(self):
        return f'{self.name}'


class Number(models.Model):
    name = models.CharField('Идентификатор', max_length=256, unique=True)

    def __str__(self):
        return f'{self.name}'