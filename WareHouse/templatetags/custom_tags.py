import json
import os

from django.template import Library

from WareHouse.models import Material

register = Library()


@register.inclusion_tag('WareHouse/template_particles/material_template.html')
def get_materials():
    materials = Material.objects.all()
    return {'materials': materials}


@register.inclusion_tag('WareHouse/replenishment_list.html')
def get_context(request):
    context = {
        'is_admin': request.user.groups.filter(name='admins').exists(),
    }
    return context


@register.simple_tag(name='favorites')
def get_favorites():
    if os.path.exists('WareHouse/temporary/favorites.json'):
        with open('WareHouse/temporary/favorites.json') as f:
            pks = json.load(f)
        return pks


@register.simple_tag(name='is_admin')
def is_admin(request):
    is_admin = request.user.groups.filter(name='admins').exists()
    return is_admin

