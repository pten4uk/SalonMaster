from django.contrib import admin

from .models import *


class NumberAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class MaterialAdmin(admin.ModelAdmin):
    search_fields = ('number',)


admin.site.register(Material, MaterialAdmin)
admin.site.register(Number, NumberAdmin)
admin.site.register(Category)
