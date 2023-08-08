from django.urls import path
from .views import lista
from django.conf import settings
from django.conf.urls.static import static
from home.api.views import ObtenerToken

from rest_framework import routers
from home.api import views

# urlpatterns = [
#     path('',lista)
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


router_posts = routers.DefaultRouter()

router_posts.register(prefix='EstadoTrabajador', basename="Estado_trabajador", viewset=views.EstadoTrabajadorApi)
router_posts.register(prefix='TipoDeProfesiones', basename="Profesiones", viewset=views.ProfesionesApi)
router_posts.register(prefix='ProfesionesxTrabajador', basename="ProfesionesxTrabajador", viewset=views.ProfesionesxTrabajadorApi)
router_posts.register(prefix='Servicio', basename="Servicio", viewset=views.ServiciosApi)
router_posts.register(prefix='Cliente', basename="Cliente", viewset=views.ClienteApi)
router_posts.register(prefix='Trabajador', basename="Trabajador", viewset=views.TrabajadorApi)
router_posts.register(prefix='Cita', basename="Cita", viewset=views.CitaApi)
router_posts.register(prefix='DetalleCita', basename="DetalleCita", viewset=views.DetalleCitaApi)
router_posts.register(prefix='Enfermedades', basename="Enfermedades", viewset=views.EnfermedadesApi)
router_posts.register(prefix='EnfermedadesxPaciente', basename="EnfermedadesxPaciente", viewset=views.EmfermedadesxPacienteApi)



router_posts.register(prefix='Login', basename="Login", viewset=views.LoginApi)
router_posts.register(prefix='Chat', basename="Chat", viewset=views.ChatApi)
router_posts.register(prefix='ChatDetalle', basename="ChatDetalle", viewset=views.ChatDetalle)
router_posts.register(prefix='Mensaje', basename="Mensaje", viewset=views.MensajeApi)
router_posts.register(prefix='TipoSangre',basename='TipoSangre',viewset=views.TipoSangreApi)
#router_posts.register(prefix='',basename='',viewset=)
router_posts.register(prefix='Pais',basename='Pais',viewset=views.PaisApi)
router_posts.register(prefix='Ciudad',basename='Ciudad',viewset=views.CiudadApi)
router_posts.register(prefix='Provincia',basename='Provincia',viewset=views.ProvinciaApi)
router_posts.register(prefix='Sexo',basename='Sexo',viewset=views.SexoApi)

urlpatterns = router_posts.urls 
urlpatterns += [
    path('token/', ObtenerToken.as_view(), name='token'),
]