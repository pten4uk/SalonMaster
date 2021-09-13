import json
import os

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .filters import MaterialFilter
from .forms import *
from .models import Material
from .utils import is_admin


class MaterialList(ListView):
    model = Material
    context_object_name = 'materials'
    template_name = 'WareHouse/material_list.html'
    paginate_by = 30
    ordering = ['number__name']

    def get_filter(self):
        return MaterialFilter(self.request.GET, queryset=super().get_queryset().select_related('category', 'number'))

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filter'] = self.get_filter()
        if self.request.GET:
            for key, value in self.request.GET.items():
                context[key] = value
        return context


class MaterialCreate(CreateView):
    template_name = 'WareHouse/material_create.html'
    form_class = MaterialForm
    success_url = '/warehouse/'


# --------------------------------------definitions-------------------------------------------
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

        return redirect(f'/warehouse/?number={material.number.name.split()[0]}')
    return render(request, 'WareHouse/material_expense.html', context=context)


# ---------------------------------------------incoming-expense-----------------------------------------------
def incoming(request, pk):
    material = Material.objects.get(pk=pk)
    form = UpdateForm()
    context = {
        'form': form,
        'material': material,
    }
    if request.method == 'POST':
        packages = 0
        quantity = 0
        if request.POST['quantity']:
            quantity = int(request.POST['quantity'])
        if request.POST['packages']:
            packages = int(request.POST['packages'])
        material.add_material(packages, quantity)

        return redirect(f'/warehouse/?number={material.number.name.split()[0]}')
    return render(request, 'WareHouse/material_incoming.html', context=context)


@is_admin
def delete(request, pk):
    material = Material.objects.select_related('category').get(pk=pk)
    context = {
        'material': material
    }
    return render(request, 'WareHouse/material_delete.html', context=context)

# ---------------------------------------------incoming-expense-----------------------------------------------
# -----------------------------------------confirmations----------------------------------------------


@is_admin
def delete_confirm(request, pk):
    Material.objects.get(pk=pk).delete()
    return redirect('/warehouse/')

# -----------------------------------------confirmations----------------------------------------------
# ---------------------------------------------------replenishment----------------------------------------------


@is_admin
def get_replenishment(request):
    materials = []
    get_mats = Material.objects.select_related('number', 'category').all()
    for mat in get_mats:
        if mat.tracked:
            if mat.quantity / mat.volume < 2:
                materials.append(mat)
    return render(request, 'WareHouse/replenishment_list.html', {'materials': materials})


@is_admin
def get_favorites(request):
    if os.path.exists('WareHouse/temporary/favorites.json'):
        with open('WareHouse/temporary/favorites.json') as f:
            pks = json.load(f)
    get_mats = Material.objects.select_related('number', 'category').filter(pk__in=pks)
    return render(request, 'WareHouse/replenishment_list.html', {'materials': get_mats})


@is_admin
def add_to_favorites(request, pk):

    if not os.path.exists('WareHouse/temporary/favorites.json'):
        pks = []
        pks.append(int(pk))
        with open('WareHouse/temporary/favorites.json', 'w') as f:
            json.dump(pks, f, indent=4)
    else:
        with open('WareHouse/temporary/favorites.json') as f:
            pks = json.load(f)
        if int(pk) not in pks:
            pks.append(int(pk))
        with open('WareHouse/temporary/favorites.json', 'w') as f:
            json.dump(pks, f, indent=4)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@is_admin
def del_from_favorites(request, pk):
    if not os.path.exists('WareHouse/temporary/favorites.json'):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    with open('WareHouse/temporary/favorites.json') as f:
        pks = json.load(f)
    for i, primary in enumerate(pks):
        if primary == int(pk):
            pks.pop(i)
    with open('WareHouse/temporary/favorites.json', 'w') as f:
        json.dump(pks, f, indent=4)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# ---------------------------------------------------replenishment----------------------------------------------