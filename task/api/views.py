from rest_framework.viewsets import ModelViewSet
from home.administrador import models
from home.cliente import models
from home.trabajador import models
from home.api import serializers

from rest_framework.views import APIView
from rest_framework.response import Response

class ProfesionesApi(ModelViewSet):
    queryset = models.Profesiones.objects.all()
    serializer_class = serializers.ProfesionesSerializer

class EstadoTrabajadorApi(ModelViewSet):
    queryset = models.EstadoTrabajador.objects.all()
    serializer_class = serializers.EstadoTrabajadorSerializer

class ServiciosApi(ModelViewSet):
    queryset = models.Servicio.objects.all()
    serializer_class = serializers.ServicioSerializer     

class ClienteApi(ModelViewSet):
    queryset = models.Cliente.objects.all()
    serializer_class = serializers.ClienteSerializer

class TrabajadorApi(ModelViewSet):
    queryset = models.Trabajador.objects.all()
    serializer_class = serializers.TrabajadorSerializer

class CitaApi(ModelViewSet):
    queryset = models.Cita.objects.all()
    serializer_class = serializers.CitaSerializer

class DetalleCitaApi(ModelViewSet):
    queryset = models.DetalleCita.objects.all()
    serializer_class = serializers.DetalleCitaSerializer


class ProfesionesxTrabajadorApi(ModelViewSet):
    queryset = models.ProfesionesxTrabajador.objects.all()
    serializer_class = serializers.ProfesionesxTrabajadorSerializer  

class EnfermedadesApi(ModelViewSet): 
    queryset = models.Enfermedades.objects.all()
    serializer_class = serializers.EnfermedadesSerializar

class EmfermedadesxPacienteApi(ModelViewSet):  
    queryset = models.EnfermedadesxPaciente.objects.all()
    serializer_class = serializers.EnfermedadesXP


class LoginApi(ModelViewSet):
    queryset = models.Login.objects.all()
    serializer_class = serializers.LoginSerializer 

class MensajeApi(ModelViewSet):
    queryset = models.Mensaje.objects.all()
    serializer_class = serializers.MensajeSerializar  

class ChatApi(ModelViewSet):
    queryset = models.Chat.objects.all()
    serializer_class = serializers.ChatSerializer

class ChatDetalle(ModelViewSet):
    queryset = models.ChatDetalle.objects.all()
    serializer_class = serializers.ChatDetalleSerializar  

class TipoSangreApi(ModelViewSet):
    queryset = models.TipoSangre.objects.all()
    serializer_class = serializers.TipoSangreSerializer

class PaisApi(ModelViewSet):
    queryset = models.Pais.objects.all()
    serializer_class = serializers.PaisSerializer

class ProvinciaApi(ModelViewSet):
    queryset = models.Provincia.objects.all()
    serializer_class = serializers.ProvinciaSerializer

class CiudadApi(ModelViewSet):
    queryset = models.Ciudad.objects.all()
    serializer_class = serializers.CiudadSerializer   

class SexoApi(ModelViewSet):
    queryset = models.Sexo.objects.all()
    serializer_class = serializers.SexoSerializar

import secrets

class ObtenerToken(APIView):
    def post(self, request, *args, **kwargs):
        usuario = request.data.get('usuario')
        contrasenia = request.data.get('contrasenia')

        try:
            cliente = models.Login.objects.get(usuario=usuario)
        except models.Login.DoesNotExist:
            return Response({"error": "Credenciales inválidas."}, status=400)

        if cliente.contrasenia == contrasenia:
            try:
                token = models.CustomToken.objects.get(login=cliente)
            except models.CustomToken.DoesNotExist:
                token = models.CustomToken(login=cliente, key=secrets.token_hex(16))
                token.save()
                
            return Response({'token': token.key})
        else:
            return Response({"error": "Contraseña inválidas."}, status=400)    