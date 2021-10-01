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

    path('needs_replenishment/', ReplenishmentList.as_view(), name='replenishment'),
    path('favorites/', FavoriteList.as_view(), name='favorites'),
    path('favorites/clean', clean_favorites, name='clean_favorites'),
    path('<int:pk>/add_to_favorites', add_to_favorites, name='add_to_favorites'),
    path('<int:pk>/del_from_favorites', del_from_favorites, name='del_from_favorites'),

    path('nontracked/', NonTrackedList.as_view(), name='nontracked'),
    path('<int:pk>/set_nontracked', set_nontracked, name='set_nontracked'),
    path('<int:pk>/set_tracked', set_tracked, name='set_tracked'),

]
