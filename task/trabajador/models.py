from datetime import timezone
import re
from django.db import models
from django.forms import ValidationError
from datetime import date
from datetime import datetime
from django.utils import timezone
import pytz
from django.core.exceptions import ValidationError
from home.cliente.models import *
from home.administrador.models import *
from home.trabajador.models import *
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.dispatch import receiver
from django.db.models.signals import pre_save

from home.trabajador.models import *

class Cita(models.Model):
    id_cita = models.AutoField(primary_key=True)
    id_trabajador = models.ForeignKey('Trabajador', models.DO_NOTHING, db_column='id_trabajador',verbose_name = 'Trabajador')
    id_cliente = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='id_cliente',verbose_name = 'Cliente')
    descripcion_motivo = models.CharField(max_length=200,verbose_name = 'Motivo de cita')
    
    fecha_creacion = models.DateTimeField(verbose_name = 'Fecha de Creacion')
    fecha_inicioatencion = models.DateTimeField(null=True,verbose_name = 'Fecha Inicio de Atención')
    fecha_finatencion = models.DateTimeField(verbose_name = 'Fecha Fin de Atención')


    latitud = models.DecimalField(max_digits=15, decimal_places=9)
    longitud = models.DecimalField(max_digits=15, decimal_places=9) 
    ubicacion = models.PointField(null=True,blank=True)
    estado = models.ForeignKey('EstadoCita', models.DO_NOTHING, db_column='id_estado',verbose_name = 'Estado')
    def save(self,*args,**kwagrs):
        self.fecha_creacion = self.convertir_fecha(self.fecha_creacion)
        self.fecha_inicioatencion = self.convertir_fecha(self.fecha_inicioatencion)
        self.fecha_finatencion = self.convertir_fecha(self.fecha_finatencion)
        
        if not self.latitud:
            self.latitud=self.ubicacion.y
        if not self.longitud:
            self.longitud=self.ubicacion.x
        super(Cita,self).save(*args,**kwagrs)
        
    def convertir_fecha(self, fecha_str):
        if fecha_str:
            fecha_obj = datetime.fromisoformat(fecha_str.isoformat()[:-6])
            return fecha_obj.strftime('%Y-%m-%d %H:%M:%S')
        return None
    
    class Meta:
        app_label = "home"
        managed = True
        db_table = 'Cita'


class DetalleCita(models.Model):
    id_detalle_cita = models.AutoField(primary_key=True)
    id_cita = models.ForeignKey(Cita, models.DO_NOTHING, db_column='id_cita')
    id_servicio = models.ForeignKey('Servicio', models.DO_NOTHING, db_column='id_servicio')
    descripcion_motivo = models.CharField(max_length=200)

    class Meta:
        managed = True
        db_table = 'Detalle_cita'

class Chat(models.Model):
    id_chat = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='id_cliente')
    id_trabajador = models.ForeignKey('Trabajador', models.DO_NOTHING, db_column='id_trabajador')
    fecha_creacion=models.DateField()
    estado = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'Chat'
    def __str__(self):
        return f" {self.id_chat}"

class ChatDetalle(models.Model):
    id_chatdetalle = models.AutoField(primary_key=True)
    id_chat = models.ForeignKey('Chat', models.DO_NOTHING, db_column='id_chat')
    id_cliente = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='id_cliente')

    class Meta:
        managed = True
        db_table = 'ChatDetalle'


class Mensaje(models.Model):
    id_mensaje = models.AutoField(primary_key=True)
    id_chat = models.ForeignKey('Chat', models.DO_NOTHING, db_column='id_chat')
    id_cliente = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='id_cliente')
    fecha_envio = models.DateField()
    Mensaje = models.CharField(max_length=200)
    tipo_mensaje=models.CharField(max_length=50)
    estado_tipo=models.CharField(max_length=50)
    class Meta:
        managed = True
        db_table = 'Mensaje'



class TipoTrabajador(models.Model):
    id_tipotrabajador = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=70,verbose_name = 'Descripción')
    def clean(self):
        super().clean()
        if not re.match(r'^[Normal|Premiun]+$', self.descripcion):
            raise ValidationError('Solo tipo Normal o Premiun.')
    estado = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'Tipo_trabajador'
        verbose_name = 'Tipo de Trabajador'
        verbose_name_plural = 'Tipo de Trabajador'

    def __str__(self):
        return self.descripcion
    
class Trabajador(models.Model):
    id_trabajador = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente',verbose_name = 'Trabajador')#,unique=True
    id_tipo_trabajador = models.ForeignKey(TipoTrabajador, models.DO_NOTHING, db_column='id_tipo_trabajador',verbose_name = 'Tipo de Trabajador')
    pdf_cedula = models.FileField(null=True,upload_to='pdfs/',verbose_name = 'Pdf Cédula')
    pdf_curriculum = models.FileField(null=True,upload_to='pdfs/',verbose_name = 'Pdf Curriculum')
    latitud = models.DecimalField(max_digits=15, decimal_places=9)
    longitud = models.DecimalField(max_digits=15, decimal_places=9) 
    ubicacion = models.PointField(null=True,blank=True)
    estado = models.ForeignKey('EstadoTrabajador', models.DO_NOTHING, db_column='id_estado',verbose_name = 'Estado_Trabajador')
    presentacion = models.CharField(max_length=200,null=True)
    def save(self,*args,**kwagrs):
        if not self.latitud:
            self.latitud=self.ubicacion.y
        if not self.longitud:
            self.longitud=self.ubicacion.x
        super(Trabajador,self).save(*args,**kwagrs)

    class Meta:
        managed = True
        db_table = 'Trabajador'
        verbose_name = 'Trabajador'
        verbose_name_plural = 'Trabajador'

    def __str__(self):
        return f"{self.id_cliente.nombre} {self.id_cliente.apellido}"    
    

class GaleriaTrabajador(models.Model):
    id_galeria = models.AutoField(primary_key=True)
    id_trabajador = models.ForeignKey('Trabajador', models.DO_NOTHING, db_column='id_trabajador')
    foto = models.ImageField(upload_to='images/',null=True,blank=True)
    class Meta:
        managed = True
        db_table = 'GaleriaTrabajador'        
    

class Sucursal(models.Model):
    id_sucursal = models.AutoField(primary_key=True)
    id_trabajador = models.ForeignKey('Trabajador', models.DO_NOTHING, db_column='id_trabajador')
    coordenadas_x = models.DecimalField(max_digits=6,decimal_places=6)
    coordenadas_y = models.DecimalField(max_digits=7,decimal_places=7)
    telefono = models.CharField(max_length=20)
    referencia = models.CharField(max_length=200)
    estado = models.CharField(max_length=50)
    pdf_certificadoruc =models.FileField()
    foto=models.ImageField()
    

    class Meta:
        managed = True
        db_table = 'Sucursal'

class DetalleSucursal(models.Model):
    id_trabajador = models.ForeignKey('Trabajador', models.DO_NOTHING, db_column='id_trabajador')
    id_sucursal = models.ForeignKey('Sucursal', models.DO_NOTHING, db_column='id_sucursal')
    estado = models.BooleanField()


    class Meta:
        managed = True
        db_table = 'DetalleSucursal'        


class Ubicaciones(models.Model):
    id_ubicaciones = models.AutoField(primary_key=True)
    id_trabajador = models.ForeignKey('Trabajador', models.DO_NOTHING, db_column='id_trabajador')
    latitud = models.DecimalField(max_digits=15, decimal_places=9)
    longitud = models.DecimalField(max_digits=15, decimal_places=9) 
    ubicacion = models.PointField()

    def save(self,*args,**kwagrs):
        if not self.latitud:
            self.latitud=self.ubicacion.y
        if not self.longitud:
            self.longitud=self.ubicacion.x
        super(Ubicaciones,self).save(*args,**kwagrs)
    estado = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'Ubicaciones'

#Para trabajar con estado de trabajador
class EstadoTrabajador(models.Model):
    id_estado = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50,verbose_name = 'Descripcion')
    class Meta:
        managed = True
        db_table = 'Estado_trabajador'
        verbose_name = 'Estado_trabajador'
        verbose_name_plural = 'Estado_trabajador'
    def __str__(self):
        return self.descripcion
#Para trabajadar con estado de cita
class EstadoCita(models.Model):
    id_estado = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50,verbose_name = 'Descripcion')
    class Meta:
        managed = True
        db_table = 'Estado_cita'
        verbose_name = 'Estado_cita'
        verbose_name_plural = 'Estado_cita'
    def __str__(self):
        return self.descripcion

class Pais(models.Model):
    id_pais=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre
class Meta:
        managed = True
        db_table = 'Pais'
        verbose_name = 'Pais'
        verbose_name_plural = 'Pais'

class Provincia(models.Model):
    id_provincia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    id_pais = models.ForeignKey(Pais, models.DO_NOTHING, db_column='id_pais')

    def __str__(self):
        return self.nombre
class Meta:
        managed = True
        db_table = 'Provincia'
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincia'

class Ciudad(models.Model):
    id_ciudad=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    #país = models.ForeignKey(Pais, on_delete=models.CASCADE)
    provincia=models.ForeignKey(Provincia, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre
class Meta:
        managed = True
        db_table = 'Ciudad'
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudad'

class CustomToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    login = models.OneToOneField(Login, related_name='token', on_delete=models.CASCADE)

    def _str_(self):
        return self.key   

class Meta:
        managed = True
        db_table = 'token'
        verbose_name = 'token'
        verbose_name_plural = 'token'         