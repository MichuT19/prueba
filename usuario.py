import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home.settings")  # Reemplaza "tuprojecto" con el nombre de tu proyecto Django
django.setup()

from django.contrib.auth.models import User

def main():
    # Crea un usuario
    user = User.objects.create_superuser('admin', 'correo@ejemplo.com', 'contraseña')
    print('Usuario creado exitosamente:', user.username)

if __name__ == '__main__':
    main()