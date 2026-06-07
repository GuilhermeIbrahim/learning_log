from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, verbose_name='Biografia')
    campus = models.CharField(max_length=100, blank=True, verbose_name='Campus')
    matricula = models.CharField(max_length=14, blank=True, verbose_name='Matrícula')
    tipo_vinculo = models.CharField(max_length=50, blank=True, verbose_name='Tipo de Vínculo')
    foto_url = models.URLField(blank=True, verbose_name='Foto')
    
    def __str__(self):
        return f'{self.user.username}'