from django.contrib.auth import logout
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView

from .filters import MaterialFilter
from .forms import *
from .models import Material


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
        context['is_admin'] = self.request.user.groups.filter(name='admins').exists()
        if self.request.GET:
            for key, value in self.request.GET.items():
                context[key] = value
        return context


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

        return redirect(f'/warehouse/?number={material.number.name.split()[0]}')
    return render(request, 'WareHouse/material_expense.html', context=context)


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


def delete(request, pk):
    if not request.user.groups.filter(name='admins').exists():
        raise Http404()
    print(pk)
    material = Material.objects.select_related('category').get(pk=pk)
    context = {
        'material': material
    }
    return render(request, 'WareHouse/material_delete.html', context=context)


def delete_confirm(request, pk):
    if not request.user.groups.filter(name='admins').exists():
        raise Http404()
    Material.objects.get(pk=pk).delete()
    return redirect('/warehouse/')
