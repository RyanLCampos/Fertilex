from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    # Se deletar o usuario, será deletado o perfil
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    imagem = models.ImageField(default='default.png', upload_to='perfil_img')

    def __str__(self):
        return f'{self.user.username} Perfil'
    
