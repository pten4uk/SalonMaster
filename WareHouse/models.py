from django.db import models


class Material(models.Model):
    BRANDS = [
        ('Matrix', 'Матрикс'),
        ('Estel', 'Эстель'),
    ]
    brand = models.CharField('Бренд', max_length=32, choices=BRANDS, default='Matrix')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    number = models.ForeignKey('Number', max_length=256, on_delete=models.CASCADE)
    volume = models.PositiveSmallIntegerField('Объем', default=0)
    quantity = models.PositiveSmallIntegerField('Количество', default=0)
    tracked = models.BooleanField('Отслеживаемость', default=False)

    def add_material(self, quantity):
        self.quantity += quantity * self.volume
        self.tracked = True
        self.save()

    def expense(self, quantity):
        if self.quantity >= quantity:
            self.quantity -= quantity
            if self.quantity == quantity:
                self.tracked = False
            self.save()
        return self.quantity

    def __str__(self):
        return f'{self.number}'


class Category(models.Model):
    name = models.CharField('Категория', max_length=256)

    def __str__(self):
        return f'{self.name}'


class Number(models.Model):
    name = models.CharField('Идентификатор', max_length=256)

    def __str__(self):
        return f'{self.name}'