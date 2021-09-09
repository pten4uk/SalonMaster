from .models import Material


class MaterialDataMixin:
    model = Material
    context_object_name = 'materials'
    template_name = 'WareHouse/material_list.html'
    paginate_by = 30

