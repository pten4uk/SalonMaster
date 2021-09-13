from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import *

urlpatterns = [
    path('', MaterialList.as_view(), name='home'),

    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('create/', MaterialCreate.as_view(), name='create'),
    path('<int:pk>/delete/', delete, name='delete'),
    path('<int:pk>/delete/confirm', delete, name='delete_confirm'),

    path('<int:pk>/expense/', expense, name='expense'),
    path('<int:pk>/incoming/', incoming, name='incoming'),

    path('needs_replenishment/', get_replenishment, name='replenishment'),
    path('favorites/', get_favorites, name='favorites'),
    path('<int:pk>/add_to_favorites', add_to_favorites, name='add_to_favorites'),
    path('<int:pk>/del_from_favorites', del_from_favorites, name='del_from_favorites'),

]
