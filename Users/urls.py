from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('logout/', views.logout_view, name='logout'),
]