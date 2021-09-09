from django.urls import path

from .views import *

urlpatterns = [
    path('', MaterialList.as_view(), name='home'),
    path('filter/category/<int:pk>', MaterialCategory.as_view(), name='filter_category'),
    path('create/', MaterialCreate.as_view(), name='create'),
    path('<int:pk>/expense/', expense, name='expense'),
    path('<int:pk>/incoming/', incoming, name='incoming'),

]
