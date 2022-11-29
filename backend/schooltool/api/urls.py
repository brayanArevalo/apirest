from django.urls import path
from .views import GrupoView
from .vistas.EstudianteView import EstudianteView
from .vistas.AsignaturaView import AsignaturaView
from .vistas.ProfesorView import ProfesorView
from .vistas.LogroView import LogroView
from .vistas.BoletinView import BoletinView
from .vistas.ConsultaView import ConsultaView

urlpatterns = [
    path('',GrupoView.as_view(),name="inicio"),
    path('grupos/', GrupoView.as_view(), name='lista_grupos'),
    path('grupos/<int:id>', GrupoView.as_view(), name='proceso'),
    path('estudiantes/',EstudianteView.as_view(),name="lista_estudiante"),
    path('estudiantes/<int:id>',EstudianteView.as_view(),name="procesar_estudiante"),
    path('asignaturas/',AsignaturaView.as_view(),name="lista_asignatura"),
    path('asignaturas/<int:id>',AsignaturaView.as_view(),name="procesar_asignatura"),
    path('profesores/',ProfesorView.as_view(),name="lista_profesor"),
    path('profesores/<int:id>',ProfesorView.as_view(),name="procesar_profesor"),
    path('logros/',LogroView.as_view(),name="lista_logro"),
    path('logros/<int:id>',LogroView.as_view(),name="procesar_logro"),
    path('boletin/',BoletinView.as_view(),name="lista_boletin"),
    path('boletin/<int:id>',BoletinView.as_view(),name="procesar_boletin"),
    path('consulta/',ConsultaView.as_view(),name="consulta"),
    path('consulta/<int:id>',ConsultaView.as_view(),name="proceso")

]