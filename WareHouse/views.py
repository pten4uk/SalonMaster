import json
import os

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView

from .forms import *
from .models import Material
from .utils import is_admin, DataListMixin


class MaterialList(DataListMixin, ListView):
    paginate_by = 30

    def get_queryset(self):
        get_mats = self.get_filter().qs
        materials = [] + list(get_mats)
        return materials


class ReplenishmentList(DataListMixin, ListView):
    paginate_by = 15

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='admins').exists():
            return redirect('/warehouse/login/')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        materials = []
        get_mats = self.get_filter().qs
        for mat in get_mats:
            if mat.needs_replenishment():
                materials.append(mat)
        return materials


class FavoriteList(ReplenishmentList):
    def get_queryset(self):
        pks = []
        if os.path.exists('WareHouse/temporary/favorites.json'):
            with open('WareHouse/temporary/favorites.json') as f:
                pks = json.load(f)
        get_mats = Material.objects.select_related('number', 'category').filter(pk__in=pks, tracked=True)
        materials = [] + list(get_mats)
        return materials

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['materials_exists'] = True if self.object_list else False
        return context


class NonTrackedList(FavoriteList):
    def get_queryset(self):
        get_mats = Material.objects.select_related('number', 'category').filter(tracked=False)
        materials = [] + list(get_mats)
        return materials

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['materials_exists'] = False
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


@is_admin
def clean_favorites(request):
    os.remove('WareHouse/temporary/favorites.json')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@is_admin
def set_nontracked(request, pk):
    mat = Material.objects.get(pk=pk)
    mat.tracked = False
    mat.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@is_admin
def set_tracked(request, pk):
    mat = Material.objects.get(pk=pk)
    mat.tracked = True
    mat.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# -----------------------------------------confirmations----------------------------------------------
# ---------------------------------------------------replenishment----------------------------------------------


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
