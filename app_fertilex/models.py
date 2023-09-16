from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# Create your models here.
class Previsao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100, default="1")
    data_criacao = models.DateTimeField(default=timezone.now)
    dados_tabela = models.JSONField(default=list)
    resultados = models.JSONField(default=list)
