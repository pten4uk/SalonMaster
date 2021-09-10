from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import *

urlpatterns = [
    path('', MaterialList.as_view(), name='home'),
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', MaterialCreate.as_view(), name='create'),
    path('<int:pk>/expense/', expense, name='expense'),
    path('<int:pk>/incoming/', incoming, name='incoming'),

]
