from django.urls import path
from . import views

app_name = 'app_fertilex'

urlpatterns = [
    path('', views.resultados, name='resultados'),
    path('prever/', views.prever, name='prever_nova'),
    path('prever/<int:previsao_id>/', views.prever, name='prever_atualizar'),
    path('excluir-previsao/<int:previsao_id>/', views.excluir_previsao, name='excluir_previsao'),
]