from django.shortcuts import render

# Create your views here.
def lista(request):
    return render(request,'lista.html')


from django.http import FileResponse, Http404
from django.conf import settings
import os

def serve_media_file(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')  # Ajusta el content_type según el tipo de archivo que deseas servir
    else:
        raise Http404("El archivo no existe")
    

from rest_framework.permissions import IsAuthenticated
from task.trabajador.models import CustomToken

class CustomIsAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        auth = request.META.get('HTTP_AUTHORIZATION')
        if auth and auth.startswith('Token '):
            token = auth[6:].strip()
            try:
                custom_token = CustomToken.objects.get(key=token)
            except CustomToken.DoesNotExist:
                return False
            return True
        return False