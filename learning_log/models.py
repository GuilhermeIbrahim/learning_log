from django.db import models

class Topic(models.Model):
    """Assunto sobre o qual o usuário está aprendendo."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """Devolve uma representacão em string do modelo."""
        return self.text