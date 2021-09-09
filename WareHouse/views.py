from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView

from .forms import *
from .models import Material
from .utils import MaterialDataMixin


class MaterialList(MaterialDataMixin, ListView):
    def get_queryset(self):
        return Material.objects.order_by('pk').select_related('category', 'number')


class MaterialCategory(MaterialDataMixin, ListView):
    def get_queryset(self):
        return Material.objects.order_by('pk').filter(
            category__pk=self.kwargs['pk']).select_related('category', 'number')

    def dispatch(self, request, *args, **kwargs):
        if 'category' in self.request.GET:
            cat_pk = self.request.GET['category']
            return redirect(f'/warehouse/filter/category/{cat_pk}')
        return super().dispatch(request, *args, **kwargs)


class MaterialCreate(CreateView):
    template_name = 'WareHouse/material_create.html'
    form_class = MaterialForm
    success_url = '/warehouse/'


def expense(request, pk):
    material = Material.objects.get(pk=pk)
    form = UpdateForm()
    context = {
        'form': form,
        'material': material,
    }
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])

        if quantity <= 0:
            return render(request, 'WareHouse/material_expense.html', context=context)

        if material.quantity >= quantity:
            material.expense(quantity)
        else:
            form.error = f'Нельзя израсходовать больше материала, чем имеется ({material.quantity}).'
            return render(request, 'WareHouse/material_expense.html', context=context)

        return redirect('/warehouse/')
    return render(request, 'WareHouse/material_expense.html', context=context)


def incoming(request, pk):
    material = Material.objects.get(pk=pk)
    form = UpdateForm()
    context = {
        'form': form,
        'material': material,
    }
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        material.add_material(quantity)
        return redirect('/warehouse/')
    return render(request, 'WareHouse/material_incoming.html', context=context)