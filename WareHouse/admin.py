from django.contrib import admin

from .models import *


class NumberAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name', 'pk')


class MaterialAdmin(admin.ModelAdmin):
    search_fields = ('number__name',)


admin.site.register(Material, MaterialAdmin)
admin.site.register(Number, NumberAdmin)
admin.site.register(Category)
