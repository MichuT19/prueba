
from rest_framework.serializers import ModelSerializer,CharField,SerializerMethodField,ImageField
from home.administrador import models
from home.cliente import models
from home.trabajador import models

class ProfesionesSerializer(ModelSerializer):
    class Meta:
        model = models.Profesiones
        fields = ['id_profesiones','descripcion','estado']

class EstadoTrabajadorSerializer(ModelSerializer):
    class Meta:
        model = models.EstadoTrabajador
        fields = ['id_estado','descripcion']

class ProfesionesxTrabajadorSerializer(ModelSerializer):
    class Meta:
        model = models.ProfesionesxTrabajador
        fields = ['id_profesionesxtrabajador','id_profesiones','id_trabajador','numero_titulo','estado']

class ClienteSerializer(ModelSerializer):
    sexodescrip=SerializerMethodField()
    paisdescrip=SerializerMethodField()
    provinciadescrip=SerializerMethodField()
    ciudaddescrip=SerializerMethodField()
    sangredescrip=SerializerMethodField()

    class Meta:
        model = models.Cliente 
        fields = ["id_cliente","cedula","nombre",
                 "apellido","fecha_nacimiento","sexo",'sexodescrip',
                 "telefono","pais",'paisdescrip',"provincia",'provinciadescrip',"ciudad",'ciudaddescrip',
                 "referencia_de_domicilio","tipo_sangre",'sangredescrip',"foto"]
    def get_sexodescrip(self,obj):
        return obj.sexo.descripcion
    def get_paisdescrip(self,obj):
        return obj.pais.nombre
    def get_provinciadescrip(self,obj):
        return obj.provincia.nombre
    def get_ciudaddescrip(self,obj):
        return obj.ciudad.nombre   
    def get_sangredescrip(self,obj):
        return obj.tipo_sangre.descripcion   

    
    
    

class ServicioSerializer(ModelSerializer):
    class Meta:
        model = models.Servicio
        fields = ["id_servicio","id_profesiones","descripcion","estado"]


# class TrabajadorSerializer(ModelSerializer):
#     class Meta:
#         model = models.Trabajador
#         fields = ['id_trabajador','id_cliente','id_tipo_trabajador','pdf_cedula','coordenadas_x','coordenadas_y','estado']       
class TrabajadorSerializer(ModelSerializer):
    cliente = SerializerMethodField()
    trabajador = CharField(read_only=True, source = 'id_tipo_trabajador.descripcion')
    estadoid = CharField(read_only=True, source = 'estado.descripcion')
    foto=ImageField(read_only=True,source='id_cliente.foto')
    profesiones = SerializerMethodField()

    def get_profesiones(self, trabajador):
        profesionesxtrabajador = models.ProfesionesxTrabajador.objects.filter(id_trabajador=trabajador.id_trabajador)
        id_profesiones_list = profesionesxtrabajador.values_list('id_profesiones', flat=True)
        nombres_profesiones = []
        for id_profesion in id_profesiones_list:
            try:
                profesion = models.Profesiones.objects.get(id_profesiones=id_profesion)
                nombres_profesiones.append(profesion.descripcion)
            except models.Profesiones.DoesNotExist:
                pass
        return nombres_profesiones 
    
    def get_cliente(self,obj):
        return f"{obj.id_cliente.nombre} {obj.id_cliente.apellido}"
    
    class Meta:
        model = models.Trabajador
        fields = ['id_trabajador','cliente','id_cliente','profesiones','id_tipo_trabajador','trabajador','pdf_cedula','pdf_curriculum','latitud', 'longitud','estado','estadoid','foto']

class CitaSerializer(ModelSerializer):
    estadoid = CharField(read_only=True, source = 'estado.descripcion')
    class Meta:
        model = models.Cita
        fields = ['id_cita','id_trabajador','id_cliente','descripcion_motivo',
                  'fecha_creacion','fecha_inicioatencion','fecha_finatencion','latitud',
                  'longitud','estado','estadoid'
                  ]        

class DetalleCitaSerializer(ModelSerializer):
    class Meta:
        model = models.DetalleCita
        fields = '__all__'

class EnfermedadesSerializar(ModelSerializer):
    clasificaciondeenfermedad=SerializerMethodField()
    class Meta:
        model = models.Enfermedades 
        fields = ['id_enfermedad','descripcion','id_clasificacionenfermedad','clasificaciondeenfermedad','estado'] 
    def get_clasificaciondeenfermedad(self,obj):
        return obj.id_clasificacionenfermedad.descripcion
             
            

class EnfermedadesXP(ModelSerializer):
    enfermedad = SerializerMethodField()
    idclasienfermedad= CharField(read_only=True, source = 'id_enfermedad.id_clasificacionenfermedad.idclasificacion')
    class Meta:
        model = models.EnfermedadesxPaciente   
        fields = ['id_enfermedadesxpaciente','id_enfermedad','enfermedad','idclasienfermedad','id_cliente','descripcion','estado']
    def get_enfermedad(self,obj):
        return obj.id_enfermedad.descripcion

class LoginSerializer(ModelSerializer):
    clienteL = SerializerMethodField()
    class Meta:
        model = models.Login
        fields = ['id_login','clienteL','id_cliente','usuario','contrasenia','tipo_login', 'estado']
    def get_clienteL(self,obj):
        return f"{obj.id_cliente.nombre} {obj.id_cliente.apellido}"

class ChatSerializer(ModelSerializer):
    cliente = SerializerMethodField()
    trabajador = SerializerMethodField()
    class Meta:
        model = models.Chat   
        fields = ['id_chat','id_cliente','cliente','id_trabajador','trabajador','fecha_creacion','estado']
    def get_cliente(self,obj):
        return f"{obj.id_cliente.nombre} {obj.id_cliente.apellido}"
    def get_trabajador(self,obj):
        return f"{obj.id_trabajador.id_cliente.nombre} {obj.id_trabajador.id_cliente.apellido}"
    

class ChatDetalleSerializar(ModelSerializer):
    class Meta:
        model = models.ChatDetalle  
        fields = ['id_chatdetalle','id_chat','id_cliente']

class MensajeSerializar(ModelSerializer):
    class Meta:
        model = models.Mensaje  
        fields = ['id_mensaje','id_chat','id_cliente','fecha_envio','Mensaje','tipo_mensaje','estado_tipo']
        
class TipoSangreSerializer(ModelSerializer):
    class Meta:
        model = models.TipoSangre 
        fields = ['id_tiposangre','descripcion'] 

class PaisSerializer(ModelSerializer):   
    class Meta:
        model = models.Pais
        fields = ['id_pais','nombre']

class ProvinciaSerializer(ModelSerializer):   
    class Meta:
        model = models.Provincia
        fields = ['id_provincia','nombre','id_pais']

class CiudadSerializer(ModelSerializer):   
    class Meta:
        model = models.Ciudad
        fields = ['id_ciudad','nombre','provincia']                

class SexoSerializar(ModelSerializer):
    class Meta:
        model = models.Sexo
        fields = ['id_sexo','descripcion']