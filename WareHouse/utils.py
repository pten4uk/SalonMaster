from django.http import Http404
from functools import wraps

from django.shortcuts import redirect

from .filters import MaterialFilter
from .models import Material


def is_admin(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.groups.filter(name='admins').exists():
            raise Http404()
        return view(request, *args, **kwargs)
    return wrapper


class DataListMixin:
    model = Material
    context_object_name = 'materials'
    template_name = 'WareHouse/material_list.html'
    ordering = ['number__name']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='admins').exists():
            return redirect('/warehouse/login/')
        return super().dispatch(request, *args, **kwargs)

    def get_filter(self):
        return MaterialFilter(self.request.GET,
                              queryset=super().get_queryset().select_related('category', 'number').filter(tracked=True))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filter'] = self.get_filter()
        context['queryset'] = self.object_list
        if self.request.GET:
            for key, value in self.request.GET.items():
                context[key] = value
        return context


