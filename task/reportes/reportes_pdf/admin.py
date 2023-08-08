import io
from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate,Paragraph, Table, TableStyle
from reportlab.pdfgen import canvas


from home.trabajador.models import *
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter




def draw_encabezadogeneral(c):
    # Agrega la foto al encabezado
    imagen_path = "./media/logo.jpeg"  # Reemplaza con la ruta de tu imagen
    imagen_x = 20  # Coordenada X para la imagen
    imagen_y = 470  # Coordenada Y para la imagen
    c.drawImage(imagen_path, imagen_x, imagen_y, width=200, height=100)  # Ajusta el ancho y alto según tus necesidades

    # Fecha Actual
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    fecha_x = 550  # Coordenada X para la fecha
    fecha_y = 417  # Coordenada Y para la fecha

    font_name="Helvetica-Bold"

    c.setFont(font_name,14)

    c.drawString(fecha_x, fecha_y, f"Fecha de Reporte: {fecha_actual}")

def generar_pdf_matrizpais(datos, filename):
    # Crea un objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Crea el documento PDF en orientación horizontal
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))

    # Dibuja el encabezado en la página horizontal
    draw_encabezadogeneral(c)

    # Agrega el encabezado al PDF
    styles = getSampleStyleSheet()
    encabezado = Paragraph("Reporte de Paises Registrados", styles['Heading1'])
    encabezado.wrapOn(c, 1000, 100)
    encabezado.drawOn(c, 100, 414)  # Ajusta la coordenada Y para colocar el encabezado debajo de la foto

    # Organiza los datos en una matriz
    data = [['Id pais', 'Nombre']]
    for dato in datos:
        row = [dato.id_pais, dato.nombre]
        data.append(row)

    # Crea la tabla
    table = Table(data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00B2FF')),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    # Ajusta el tamaño de la tabla
    table.wrapOn(c, 1000, 100)
    table.drawOn(c, 100, 20)  # Ajusta la coordenada Y para colocar la tabla debajo del encabezado

    # Cierra el documento PDF
    c.showPage()
    c.save()

    # Obtén el contenido del buffer y añádelo a la respuesta
    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()

    return response
generar_pdf_matrizpais.short_description = "Generar Reporte en PDF"


def generar_pdf_matrizpuntuacion(datos, filename):
    # Crea un objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Crea el documento PDF en orientación horizontal
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
        # Agrega el encabezado al PDF
    styles = getSampleStyleSheet()
    encabezado = Paragraph("Reporte de Puntuaciones Registradas", styles['Heading1'])
    encabezado.wrapOn(c, 700, 800)
    encabezado.drawOn(c, 20, 410)  # Ajusta la coordenada Y para colocar el encabezado debajo de la foto

    # Dibuja el encabezado en la página horizontal
    draw_encabezadogeneral(c)

    # Organiza los datos en una matriz
    data = [['Cliente', 'Trabajador', 'Puntuación', 'Comentario']]
    for dato in datos:
        row = [dato.id_paciente, dato.id_trabajador, dato.puntuacion, dato.comentario]
        data.append(row)
    # Crea la tabla
    table = Table(data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00B2FF')),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    # Ajusta el tamaño de la tabla
    table.wrapOn(c, 600, 100)
    table.drawOn(c, 20, 320)  # Ajusta la coordenada Y para colocar la tabla debajo del encabezado

    # Cierra el documento PDF
    c.showPage()
    c.save()

    # Obtén el contenido del buffer y añádelo a la respuesta
    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()

    return response
generar_pdf_matrizpuntuacion.short_description = "Generar Reporte en PDF"


def generar_pdf_matrizclasifenfer(datos, filename):
    # Crea un objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Crea el documento PDF en orientación horizontal
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
        # Agrega el encabezado al PDF
    styles = getSampleStyleSheet()
    encabezado = Paragraph("Reporte de Clasif. de Enfermedades Registradas", styles['Heading1'])
    encabezado.wrapOn(c, 700, 800)
    encabezado.drawOn(c, 20, 410)  # Ajusta la coordenada Y para colocar el encabezado debajo de la foto

    # Dibuja el encabezado en la página horizontal
    draw_encabezadogeneral(c)

    # Organiza los datos en una matriz
    data = [['IdClasificacion', 'Descripcion', 'Estado']]
    for dato in datos:
        row = [dato.idclasificacion, dato.descripcion, dato.estado]
        data.append(row)
    # Crea la tabla
    table = Table(data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00B2FF')),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    # Ajusta el tamaño de la tabla
    table.wrapOn(c, 600, 100)
    table.drawOn(c, 20, 320)  # Ajusta la coordenada Y para colocar la tabla debajo del encabezado

    # Cierra el documento PDF
    c.showPage()
    c.save()

    # Obtén el contenido del buffer y añádelo a la respuesta
    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()

    return response
generar_pdf_matrizclasifenfer.short_description = "Generar Reporte en PDF"


def generar_pdf_matrizenfer(datos, filename):
    # Crea un objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Crea el documento PDF en orientación horizontal
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
        # Agrega el encabezado al PDF
    styles = getSampleStyleSheet()
    encabezado = Paragraph("Reporte de Enfermedades Registradas", styles['Heading1'])
    encabezado.wrapOn(c, 700, 800)
    encabezado.drawOn(c, 20, 410)  # Ajusta la coordenada Y para colocar el encabezado debajo de la foto

    # Dibuja el encabezado en la página horizontal
    draw_encabezadogeneral(c)

    # Organiza los datos en una matriz
    data = [['Id Enfermedad', 'Id Clasf. Enfermedad','Descripción','Estado']]
    for dato in datos:
        row = [dato.id_enfermedad, dato.id_clasificacionenfermedad, dato.descripcion,dato.estado]
        data.append(row)
    # Crea la tabla
    table = Table(data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00B2FF')),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    # Ajusta el tamaño de la tabla
    table.wrapOn(c, 600, 100)
    table.drawOn(c, 20, 320)  # Ajusta la coordenada Y para colocar la tabla debajo del encabezado

    # Cierra el documento PDF
    c.showPage()
    c.save()

    # Obtén el contenido del buffer y añádelo a la respuesta
    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()

    return response
generar_pdf_matrizenfer.short_description = "Generar Reporte en PDF"


def generar_pdf_matrizcita(datos, filename):
    # Crea un objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Crea el documento PDF en orientación horizontal
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
        # Agrega el encabezado al PDF
    styles = getSampleStyleSheet()
    encabezado = Paragraph("Reporte de Enfermedades Registradas", styles['Heading1'])
    encabezado.wrapOn(c, 700, 800)
    encabezado.drawOn(c, 20, 410)  # Ajusta la coordenada Y para colocar el encabezado debajo de la foto

    # Dibuja el encabezado en la página horizontal
    draw_encabezadogeneral(c)

    # Organiza los datos en una matriz
    data = [['Id Cita', 'Cliente','Motivo','Fech. Crea', 'Fech.Ini','Fech.Fin',
             'Longitud','Latitud','Estado']]
    for dato in datos:
        row = [dato.id_cita, dato.id_trabajador, dato.descripcion_motivo,dato.fecha_creacion,
               dato.fecha_inicioatencion,dato.fecha_finatencion,dato.longitud,
               dato.latitud, dato.estado]
        data.append(row)
    # Crea la tabla
    table = Table(data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00B2FF')),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    # Ajusta el tamaño de la tabla
    table.wrapOn(c, 600, 100)
    table.drawOn(c, 20, 320)  # Ajusta la coordenada Y para colocar la tabla debajo del encabezado

    # Cierra el documento PDF
    c.showPage()
    c.save()

    # Obtén el contenido del buffer y añádelo a la respuesta
    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()

    return response
generar_pdf_matrizcita.short_description = "Generar Reporte en PDF"


def generar_pdf_matrizcliente(datos, filename):
    # Crea un objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Crea el documento PDF en orientación horizontal
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
        # Agrega el encabezado al PDF
    styles = getSampleStyleSheet()
    encabezado = Paragraph("Reporte de Clientes Registrados", styles['Heading1'])
    encabezado.wrapOn(c, 700, 800)
    encabezado.drawOn(c, 20, 410)  # Ajusta la coordenada Y para colocar el encabezado debajo de la foto

    # Dibuja el encabezado en la página horizontal
    draw_encabezadogeneral(c)

    # Organiza los datos en una matriz
    data = [['Id cliente', 'Cédula', 'Cliente', 'Fecha nacimiento', 'Teléfono',
             'Sexo','Pais','Provincia', 'Ciudad','Referencia de domicilio','Tipo de Sangre']]
    for dato in datos:
        row = [dato.id_cliente, dato.cedula, dato.nombre +" " +dato.apellido, 
               dato.fecha_nacimiento, dato.telefono,dato.sexo,dato.pais,dato.provincia,dato.ciudad,
               dato.referencia_de_domicilio,dato.tipo_sangre]
        data.append(row)

    # Crea la tabla
    table = Table(data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00B2FF')),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    # Ajusta el tamaño de la tabla
    table.wrapOn(c, 600, 100)
    table.drawOn(c, 7, 250)  # Ajusta la coordenada Y para colocar la tabla debajo del encabezado

    # Cierra el documento PDF
    c.showPage()
    c.save()

    # Obtén el contenido del buffer y añádelo a la respuesta
    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()

    return response
generar_pdf_matrizcliente.short_description = "Generar Reporte en PDF"


def generar_pdf_matrizenferxpaciente(datos, filename):
    # Crea un objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Crea el documento PDF en orientación horizontal
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
        # Agrega el encabezado al PDF
    styles = getSampleStyleSheet()
    encabezado = Paragraph("Reporte de Enfermedades por Paciente Registradas", styles['Heading1'])
    encabezado.wrapOn(c, 700, 800)
    encabezado.drawOn(c, 20, 410)  # Ajusta la coordenada Y para colocar el encabezado debajo de la foto

    # Dibuja el encabezado en la página horizontal
    draw_encabezadogeneral(c)

    # Organiza los datos en una matriz
    data = [['Enfermedad', 'Cliente', 'Descripción', 'Estado']]
    for dato in datos:
        row = [dato.id_enfermedad, dato.id_cliente, dato.descripcion, 
               dato.estado]
        data.append(row)

    # Crea la tabla
    table = Table(data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00B2FF')),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    # Ajusta el tamaño de la tabla
    table.wrapOn(c, 600, 100)
    table.drawOn(c, 12, 320)  # Ajusta la coordenada Y para colocar la tabla debajo del encabezado

    # Cierra el documento PDF
    c.showPage()
    c.save()

    # Obtén el contenido del buffer y añádelo a la respuesta
    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()

    return response
generar_pdf_matrizenferxpaciente.short_description = "Generar Reporte en PDF"


def generar_pdf_matrizprofesiones(datos, filename):
    # Crea un objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Crea el documento PDF en orientación horizontal
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
        # Agrega el encabezado al PDF
    styles = getSampleStyleSheet()
    encabezado = Paragraph("Reporte de Profesiones Registradas", styles['Heading1'])
    encabezado.wrapOn(c, 700, 800)
    encabezado.drawOn(c, 20, 410)  # Ajusta la coordenada Y para colocar el encabezado debajo de la foto

    # Dibuja el encabezado en la página horizontal
    draw_encabezadogeneral(c)

    # Organiza los datos en una matriz
    data = [['Id profesiones', 'Descripcion', 'Estado']]
    for dato in datos:
        row = [dato.id_profesiones, dato.descripcion, dato.estado]
        data.append(row)

    # Crea la tabla
    table = Table(data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00B2FF')),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    # Ajusta el tamaño de la tabla
    table.wrapOn(c, 600, 100)
    table.drawOn(c, 12, 320)  # Ajusta la coordenada Y para colocar la tabla debajo del encabezado

    # Cierra el documento PDF
    c.showPage()
    c.save()

    # Obtén el contenido del buffer y añádelo a la respuesta
    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()

    return response
generar_pdf_matrizprofesiones.short_description = "Generar Reporte en PDF"


def generar_pdf_matrizservicios(datos, filename):
    # Crea un objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Crea el documento PDF en orientación horizontal
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
        # Agrega el encabezado al PDF
    styles = getSampleStyleSheet()
    encabezado = Paragraph("Reporte de Profesiones Registradas", styles['Heading1'])
    encabezado.wrapOn(c, 700, 800)
    encabezado.drawOn(c, 20, 410)  # Ajusta la coordenada Y para colocar el encabezado debajo de la foto

    # Dibuja el encabezado en la página horizontal
    draw_encabezadogeneral(c)

    # Organiza los datos en una matriz
    data = [['Id Servicio', 'Id profesiones', 'Descipción','Estado']]
    for dato in datos:
        row = [dato.id_servicio, dato.id_profesiones, dato.descripcion,dato.estado]
        data.append(row)

    # Crea la tabla
    table = Table(data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00B2FF')),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    # Ajusta el tamaño de la tabla
    table.wrapOn(c, 600, 100)
    table.drawOn(c, 12, 320)  # Ajusta la coordenada Y para colocar la tabla debajo del encabezado

    # Cierra el documento PDF
    c.showPage()
    c.save()

    # Obtén el contenido del buffer y añádelo a la respuesta
    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()

    return response
generar_pdf_matrizservicios.short_description = "Generar Reporte en PDF"


def generar_pdf_matriztrabajador(datos, filename):
    # Crea un objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Crea el documento PDF en orientación horizontal
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
        # Agrega el encabezado al PDF
    styles = getSampleStyleSheet()
    encabezado = Paragraph("Reporte de Trabajadores Registrados", styles['Heading1'])
    encabezado.wrapOn(c, 700, 800)
    encabezado.drawOn(c, 20, 410)  # Ajusta la coordenada Y para colocar el encabezado debajo de la foto

    # Dibuja el encabezado en la página horizontal
    draw_encabezadogeneral(c)

    # Organiza los datos en una matriz
    data = [['Id trabajador', 'Trabajador', 'Tipo de Trabajador', 'Latitud', 'Longitud', 'Estado Trabajador']]
    for dato in datos:
        row = [dato.id_trabajador, dato.id_cliente, dato.id_tipo_trabajador, dato.latitud, dato.longitud, dato.estado]
        data.append(row)
    # Crea la tabla
    table = Table(data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00B2FF')),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    # Ajusta el tamaño de la tabla
    table.wrapOn(c, 600, 100)
    table.drawOn(c, 20, 250)  # Ajusta la coordenada Y para colocar la tabla debajo del encabezado

    # Cierra el documento PDF
    c.showPage()
    c.save()

    # Obtén el contenido del buffer y añádelo a la respuesta
    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()

    return response
generar_pdf_matriztrabajador.short_description = "Generar Reporte en PDF"