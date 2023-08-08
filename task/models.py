from django.db import models
from django.contrib.auth.models import User

# Crea un nuevo usuario
user = User.objects.create_user(username='nombre_de_usuario', password='contraseña')


class task(models.Model):
    title = models.CharField(max_length=100)
