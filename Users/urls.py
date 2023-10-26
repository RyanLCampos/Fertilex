from django.urls import path
from . import views

app_name = 'Users'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
]