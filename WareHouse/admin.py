from django.contrib import admin

from .models import *


class NumberAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name', 'pk')
    list_select_related = True


class MaterialAdmin(admin.ModelAdmin):
    search_fields = ('number__name',)
    list_select_related = True


admin.site.register(Material, MaterialAdmin)
admin.site.register(Number, NumberAdmin)
admin.site.register(Category)
