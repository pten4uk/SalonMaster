import json

from django.core.management import BaseCommand
from WareHouse.models import *

alp = 'qwertyuiopasdfghjklzxcvbnm'


def start():
    with open('WareHouse/management/commands/parse_coloration.json') as f:
        info = json.load(f)
    counter = 0
    for key, values in info.items():
        for value in values:
            brand = 'Matrix'
            category = None
            number = None
            volume = None
            quantity = 0
            if key == 'Шампуни, кондиционеры и пр.':
                category = Category.objects.get(name=key)
                for i, raw in enumerate(value):
                    elems = []
                    if raw == ',':
                        try:
                            number = Number.objects.get(name=value[:i])
                            volume = value[i+1:]
                        except Exception:
                            continue
                    elif ',' not in value:
                        number = Number.objects.get(name=value)
                    else:
                        continue
                    for elem in volume:
                        if elem.isdigit():
                            elems.append(elem)
                    volume = int(''.join(elems))
            else:
                for i, raw in enumerate(key):
                    elems = []
                    if raw == ',':
                        category = Category.objects.get(name=key[:i])
                        volume = key[i+1:]
                    else:
                        continue
                    for elem in volume:
                        if elem.isdigit():
                            elems.append(elem)
                    volume = int(''.join(elems))
                number = Number.objects.get(name=value)
            mat = Material(brand=brand, category=category, number=number, volume=volume)
            objects = Material.objects.all()
            exists = False
            for obj in objects:
                if obj.number.name == number.name and mat.volume == obj.volume:
                    exists = True
                    print('Совпадение!')
                    break
            if not exists:
                mat.save()
                print(f'Добавлен материал {mat}')


class Command(BaseCommand):
    def handle(self, *args, **options):
        start()