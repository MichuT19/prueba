from datetime import timezone
import re
from django.db import models
from django.forms import ValidationError
from datetime import date
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import pre_save


class ProfesionesxTrabajador(models.Model):
    id_profesionesxtrabajador = models.AutoField(primary_key=True)
    id_profesiones = models.ForeignKey('Profesiones', models.DO_NOTHING, db_column='id_profesiones')
    id_trabajador = models.ForeignKey('Trabajador', models.DO_NOTHING, db_column='id_trabajador')
    numero_titulo = models.CharField(max_length=50)
    estado = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'ProfesionesxTrabajador'

    def __str__(self):
        return self.numero_titulo  
    

class Profesiones(models.Model):
    id_profesiones = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=70,verbose_name = 'Descripción')
    # def clean(self):
    #     super().clean()
    #     if not re.match(r'^[Enfermero]+$', self.descripcion):
    #         raise ValidationError('Solo profesión de Enfermero.')
    estado = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'Profesiones'
        verbose_name = 'Profesiones'
        verbose_name_plural = 'Profesiones'

    def __str__(self):
        return self.descripcion    
    
class Login(models.Model):
    id_login = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='id_cliente')
    usuario = models.CharField(max_length=50,unique=True)
    contrasenia = models.CharField(max_length=50)
    tipo_login = models.CharField(max_length=50)
    estado = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'Login'

    def __str__(self):
        return self.usuario      

# @receiver(pre_save, sender=Login)
# def actualizar_campo2(sender, instance, **kwargs):
#     # if instance.estado=='FALSE':
#     #     instance.tipo_login = 'Cliente'
#     # else:
#     #     instance.tipo_login = 'Trabajador'
#     if instance.estado=='FALSE':
#         instance.tipo_login = 'Trabajador'
#     else:
#         instance.tipo_login = 'Cliente'