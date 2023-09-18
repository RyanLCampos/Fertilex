from django.urls import path
from . import views

app_name = 'app_fertilex'

urlpatterns = [
    path('resultados/', views.resultados, name='resultados'),
    path('prever/', views.prever_nova, name='prever_nova'),
    path('prever/<int:previsao_id>/', views.prever_atualizar, name='prever_atualizar'),
    path('excluir-previsao/<int:previsao_id>/', views.excluir_previsao, name='excluir_previsao'),
    path('limpar_dados/<int:previsao_id>/', views.limpar_dados, name='limpar_dados'),
]