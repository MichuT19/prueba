from datetime import timezone
import re
from django.db import models
from django.forms import ValidationError
from datetime import date
from django.core.exceptions import ValidationError

class Cliente(models.Model): 
    id_cliente = models.AutoField(primary_key=True)  
    cedula = models.CharField(max_length=10,unique=True, verbose_name = 'Cédula')
    def clean(self):
        super().clean()
        if not re.match(r'^[0-9]+$', self.cedula):
            raise ValidationError('Cédula solo debe contener números.')
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    def validate_date_range(value):
        min_fecha_nacimiento = date(1923, 1, 1)
        max_fecha_nacimiento = date(2005, 12, 31)
        if value < min_fecha_nacimiento or value > max_fecha_nacimiento:
            raise ValidationError("La fecha debe estar entre {} y {}".format('1/1/1923', '31/12/2005'))
    fecha_nacimiento = models.DateField(validators=[validate_date_range])
    telefono = models.CharField(max_length=10,verbose_name="Teléfono")
    sexo = models.ForeignKey('Sexo', models.DO_NOTHING, db_column='id_sexo',verbose_name = 'Sexo')
    pais = models.ForeignKey('Pais', on_delete=models.CASCADE,verbose_name="País")
    provincia = models.ForeignKey('Provincia', on_delete=models.CASCADE)
    ciudad = models.ForeignKey('Ciudad', on_delete=models.CASCADE)
    referencia_de_domicilio = models.CharField(max_length=30)
    tipo_sangre = models.ForeignKey('TipoSangre', models.DO_NOTHING, db_column='id_tiposangre',verbose_name = 'Tipo de Sangre')
    foto = models.ImageField(upload_to='images/',null=True,blank=True)
    
    class Meta:
        managed = True
        db_table = 'Cliente'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    
class ClasificacionDeEnfermerdades(models.Model):
    idclasificacion = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50,verbose_name = 'Descripción')
    def clean(self):
        super().clean()
        if not re.match(r'^[Alergías|Enfermedades crónicas|Enfermedades congénitas]+$', self.descripcion):
            raise ValidationError('Solo Alergías, Enfermedades crónicas y Enfermedades congénitas.')
    estado = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'Clasificacion_de_enfermerdades'
        verbose_name = 'Clasif. de Enfermedades'
        verbose_name_plural = 'Clasif. de Enfermedades'

    def __str__(self):
        return self.descripcion
    

class Servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True)    
    id_profesiones = models.ForeignKey('Profesiones', models.DO_NOTHING, db_column='id_profesiones')
    descripcion = models.CharField(max_length=200,verbose_name = 'Descripción')
    estado = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'Servicio'

    def __str__(self):
        return self.descripcion  
    

class Enfermedades(models.Model):
    id_enfermedad = models.AutoField(primary_key=True)
    id_clasificacionenfermedad = models.ForeignKey(ClasificacionDeEnfermerdades, models.DO_NOTHING, db_column='id_clasificacionenfermedad',verbose_name = 'Id Clasf. Enfermedad')
    descripcion = models.CharField(max_length=50,verbose_name = 'Descripción')
    estado = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'Enfermedades'
        verbose_name = 'Enfermedades'
        verbose_name_plural = 'Enfermedades'

    def __str__(self):
        return f"{self.id_clasificacionenfermedad}  {self.descripcion}"    

class EnfermedadesxPaciente(models.Model):
    id_enfermedadesxpaciente=models.AutoField(primary_key=True)
    id_enfermedad = models.ForeignKey(Enfermedades, models.DO_NOTHING, db_column='id_enfermedad',verbose_name = 'Enfermedad')
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente',verbose_name='Cliente')
    descripcion = models.CharField(max_length=50,verbose_name = 'Descripción')
    estado = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'EnfermedadesxPaciente'
        verbose_name = 'Enfermedades x Paciente'
        verbose_name_plural = 'Enfermedades x Paciente'

    def __str__(self):
        return self.descripcion    

class Calificacion(models.Model):
    id_paciente = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='id_cliente',verbose_name='Cliente')
    id_trabajador = models.ForeignKey('Trabajador', models.DO_NOTHING, db_column='id_trabajador',verbose_name='Trabajador')
    puntuacion = models.IntegerField()
    comentario = models.CharField(max_length=200)

    class Meta:
        managed = True
        db_table = 'Calificacion'
        verbose_name_plural = 'Calificación de Atención'

class Sexo(models.Model):
    id_sexo = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50,verbose_name = 'Sexo')
    class Meta:
        managed = True
        db_table = 'Sexo'
        verbose_name = 'Sexo'
        verbose_name_plural = 'Sexo'
    def __str__(self):
        return self.descripcion

class TipoSangre(models.Model):
    id_tiposangre = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50,verbose_name = 'Tipo de Sangre')
    class Meta:
        managed = True
        db_table = 'TipoSangre'
        verbose_name = 'TipoSangre'
        verbose_name_plural = 'TipoSangre'
    def __str__(self):
        return self.descripcion

