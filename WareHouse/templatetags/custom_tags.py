from django.template import Library

from WareHouse.forms import ChoiceCategoryForm
from WareHouse.models import Material

register = Library()


@register.inclusion_tag('WareHouse/choice_category.html')
def show_categories(request):
    if '/warehouse/filter/category/' in request.path:
        form = ChoiceCategoryForm({'category': request.path.split('/')[-1]})
    else:
        form = ChoiceCategoryForm()
    return {'form': form}


@register.simple_tag(name='counted_objects')
def get_counted_objects(request):
    if '/filter/category/' in request.path:
        return Material.objects.filter(category__pk=request.path.split('/')[-1]).count()
    return Material.objects.count()
