#import openpyxl
from django.contrib import admin
from task.trabajador.models import *
from task.cliente.models import *
from task.administrador.models import *
from django.utils.html import format_html
#crsf
from django.contrib.admin import AdminSite
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
#fecha nacimiento
from django import forms
from django.forms import DateInput
#reportes
from task.reportes.reportes_excel.admin import *
from task.reportes.reportes_pdf.admin import *

from django.utils.safestring import mark_safe

class CustomAdminSite(AdminSite):
    @method_decorator(csrf_exempt)
    def each_context(self, request):
        context = super().each_context(request)
        # Eliminar la clave del token CSRF del contexto
        del context['csrf_token']
        return context
admin_site = CustomAdminSite()

@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    def pdf_cedula_link(self, instance):
        if instance.pdf_cedula:
            return mark_safe('<a href="{0}" target="_blank">{1}</a>'.format(instance.pdf_cedula.url, instance.pdf_cedula.name))
        return None
    pdf_cedula_link.allow_tags = True
    pdf_cedula_link.short_description = 'Pdf Cédula'
    
    def pdf_curriculum_link(self, instance):
        if instance.pdf_curriculum:
            return mark_safe('<a href="{0}" target="_blank">{1}</a>'.format(instance.pdf_curriculum.url, instance.pdf_curriculum.name))
        return None
    pdf_curriculum_link.allow_tags = True
    pdf_curriculum_link.short_description = 'Pdf Curriculum'


    ordering =('id_trabajador',)
    list_display = ('id_trabajador',
                    'id_cliente',
                    'id_tipo_trabajador',
                    'pdf_cedula_link',
                    'pdf_curriculum_link',
                    'estado',
                    'presentacion',
                    #'ubicacion',
                    'latitud', 'longitud',
                    )
    
    #search_fields=('estado',)
    readonly_fields=('longitud','latitud')   
    default_lon = -78.52495 
    default_lat = -1.22985  
    default_zoom = 3  
    def reportepdf_trabajador(self, request, queryset):
        # Obtén los datos de los trabajadores seleccionados en queryset
        datos = list(queryset)
        filename = "reporteTrabajador.pdf"
        return generar_pdf_matriztrabajador(datos, filename)
    reportepdf_trabajador.short_description = "Reporte en PDF"

    actions=[reportexcel_trabajador,reportepdf_trabajador]  
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    

class ClienteForm(forms.ModelForm):
    class Meta:
        model=Cliente
        fields='__all__'
        widgets = {
            'fecha_nacimiento': DateInput(attrs={'type': 'date', 'year': True}),
        }
# Register your models here.
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    form=ClienteForm

    def foto_link(self, instance):
        if instance.foto:
            return mark_safe('<a href="{0}" target="_blank">{1}</a>'.format(instance.foto.url, instance.foto.name))
        return None
    foto_link.allow_tags = True
    foto_link.short_description = 'Foto de Perfil'

    list_display = ('id_cliente',
                    'cedula',
                    'nombre',
                    'apellido',
                    'fecha_nacimiento',
                    'telefono',
                    'sexo',
                    'pais',
                    'provincia',
                    'ciudad',
                    'referencia_de_domicilio',
                    'tipo_sangre',
                    'foto_link',
                    )
    ordering=('id_cliente',)
    search_fields=('id_cliente','nombre','apellido','cedula')

    def reportepdf_cliente2(self, request, queryset):
        # Obtén los datos de los trabajadores seleccionados en queryset
        datos = list(queryset)
        filename = "reporteCliente.pdf"
        return generar_pdf_matrizcliente(datos, filename)
    reportepdf_cliente2.short_description = "Reporte en PDF"

    actions=[reportexcel_cliente,reportepdf_cliente2]
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions    
    
    def foto2(self, obj):
        return format_html('<img src={} width="130" height="100"/>',obj.foto.url)
        #return "<img src="+obj.foto.url+"/>"
    
    


@admin.register(Profesiones)
class ProfesionesAdmin(admin.ModelAdmin):
    list_display = ('id_profesiones',
                    'descripcion',
                    'estado')
    search_fields=('descripcion','estado')

    def reportepdf_profesiones(self, request, queryset):
        # Obtén los datos de los trabajadores seleccionados en queryset
        datos = list(queryset)
        filename = "reporteClasifiEnfermedades.pdf"
        return generar_pdf_matrizprofesiones(datos, filename)
    reportepdf_profesiones.short_description = "Reporte en PDF" 

    actions=[reportexcel_profesiones,reportepdf_profesiones]
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions 

@admin.register(EnfermedadesxPaciente)
class EnfermedadesxPacienteAdmin(admin.ModelAdmin):
    list_display = (
                    'id_enfermedadesxpaciente',
                    'id_enfermedad',
                    'id_cliente',
                    'descripcion',
                    'estado')
    search_fields=('descripcion','estado')

    def reportepdf_enferxpaci(self, request, queryset):
        # Obtén los datos de los trabajadores seleccionados en queryset
        datos = list(queryset)
        filename = "reporteClasifiEnfermedades.pdf"
        return generar_pdf_matrizenferxpaciente(datos, filename)
    reportepdf_enferxpaci.short_description = "Reporte en PDF" 


    actions=[reportexcel_enfermedades_paciente,reportepdf_enferxpaci]
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions 

@admin.register(ClasificacionDeEnfermerdades)
class ClasificacionDeEnfermerdadesAdmin(admin.ModelAdmin):
    list_display = ('idclasificacion',
                    'descripcion',
                    'estado')
    ordering=('idclasificacion',)

    def reportepdf_clasifenfer(self, request, queryset):
        # Obtén los datos de los trabajadores seleccionados en queryset
        datos = list(queryset)
        filename = "reporteClasifiEnfermedades.pdf"
        return generar_pdf_matrizpuntuacion(datos, filename)
    reportepdf_clasifenfer.short_description = "Reporte en PDF" 

    actions=[reportexcel_clasificaciones,reportepdf_clasifenfer]
    search_fields=('descripcion','estado')
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions    

@admin.register(Enfermedades)
class EnfermedadesAdmin(admin.ModelAdmin):
    list_display = ('id_enfermedad',
                    'id_clasificacionenfermedad',
                    'descripcion',
                    'estado')
    
    def reportepdf_enfermedades(self, request, queryset):
        # Obtén los datos de los trabajadores seleccionados en queryset
        datos = list(queryset)
        filename = "reporteEnfermedades.pdf"
        return generar_pdf_matrizenfer(datos, filename)
    reportepdf_enfermedades.short_description = "Reporte en PDF"

    actions=[reportexcel_enfermedades,reportepdf_enfermedades]
    search_fields=('descripcion','estado')
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions    

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('id_servicio',
                    'id_profesiones',
                    'descripcion',
                    'estado')
    search_fields=('descripcion','estado')

    def reportepdf_servicios(self, request, queryset):
        # Obtén los datos de los trabajadores seleccionados en queryset
        datos = list(queryset)
        filename = "reporteServicio.pdf"
        return generar_pdf_matrizservicios(datos, filename)
    reportepdf_servicios.short_description = "Reporte en PDF" 


    actions=[reportexcel_servicio,reportepdf_servicios]
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions 

@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('id_paciente',
                    'id_trabajador',
                    'puntuacion',
                    'comentario')
    search_fields=('puntuacion','comentario')

    def reportepdf_calificacion(self, request, queryset):
        # Obtén los datos de los trabajadores seleccionados en queryset
        datos = list(queryset)
        filename = "reporteCalificacion.pdf"
        return generar_pdf_matrizpuntuacion(datos, filename)
    reportepdf_calificacion.short_description = "Reporte en PDF"

    actions=[reportexcel_calificacion,reportepdf_calificacion]
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

class CitaForm(forms.ModelForm):
    class Meta:
        model=Cita
        fields='__all__'
        widgets = {
            'fecha_creacion': DateInput(attrs={'type': 'datetime-local'}),
            'fecha_inicioatencion': DateInput(attrs={'type': 'datetime-local'}),
            'fecha_finatencion': DateInput(attrs={'type': 'datetime-local'}),
            
        }
@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    form=CitaForm
    list_display = ('id_cita',
                    'id_cliente',
                    'id_trabajador',
                    'descripcion_motivo',
                    'fecha_creacion',
                    'fecha_inicioatencion',
                    'fecha_finatencion',
                    #'ubicacion',
                    'longitud',
                    'latitud',
                    'estado',
                    )
    readonly_fields=('longitud','latitud') 

    def reportepdf_cita(self, request, queryset):
        # Obtén los datos de los trabajadores seleccionados en queryset
        datos = list(queryset)
        filename = "reporteCalificacion.pdf"
        return generar_pdf_matrizcita(datos, filename)
    reportepdf_cita.short_description = "Reporte en PDF"

    actions=[reportexcel_cita,reportepdf_cita]
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id_chat','id_cliente', 'id_trabajador','fecha_creacion','estado')
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

@admin.register(ChatDetalle)
class ChatDetalleAdmin(admin.ModelAdmin):
    list_display = ('id_chatdetalle','id_chat','id_cliente')
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ('id_mensaje','id_chat','id_cliente','fecha_envio','Mensaje','tipo_mensaje','estado_tipo')
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    ordering=('id_mensaje',)
    #search_fields=('descripcion','estado')

# @admin.register(GaleriaTrabajador)
# class GaleriaAdmin(admin.ModelAdmin):
#     list_display = ('id_galeria',
#                     'id_trabajador',
#                     'foto')
    
@admin.register(CustomToken)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'login')