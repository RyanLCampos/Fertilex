from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class ConfiguracaoPrevisao(models.Model):
    id_config = models.AutoField(primary_key=True)
    num_linhas = models.IntegerField(default=0)
    colunas_selecionadas = models.JSONField(default=list)
    standard_scaler = models.BooleanField(default=False)
    smote = models.BooleanField(default=False)
    

# Create your models here.
class Previsao(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100, default="1")
    data_criacao = models.DateTimeField(default=timezone.now)
    dados_tabela = models.JSONField(default=list)
    resultados = models.JSONField(default=list)
    configuracao = models.OneToOneField(ConfiguracaoPrevisao, on_delete=models.CASCADE, null=True)
    # selecao_colunas = models.JSONField(default=list)

