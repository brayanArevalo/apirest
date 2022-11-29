from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from api.models import Estudiante
from django.http.response import JsonResponse
from django.db import connection
import json


class EstudianteView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if (id > 0):
            estudiantes = list(Estudiante.objects.filter(id=id).values())
            if len(estudiantes) > 0:
                estudiante = estudiantes[0]
                datos = {'mensaje': "OK", 'estudiante': estudiante}
            else:
                datos = {'Mensaje': "Estudiante no encontrado"}
            return JsonResponse(datos)
        else:

            # CONSULTA SQL
            with connection.cursor() as cursor:
                consulta = list(cursor.execute(
                    "SELECT api_estudiante.id,nombre,apellido,sexo,Grupo_id,grupo FROM api_estudiante,api_grupo WHERE api_estudiante.Grupo_id = api_grupo.id"))
                lista = []
                for c in consulta:
                    secuencia = ("id", "nombre", "apellido", "sexo","Grupo_id","grupo")
                    resultado = list(zip(secuencia, c))
                    resultado = dict(resultado)
                    lista = lista+[resultado]  
                cursor.close()
                print(lista)
            # FIN CONSULTA SQL
            estudiantes = list(Estudiante.objects.values())
            if len(estudiantes) > 0:
                datos = {'Mensaje': "OK",
                         'estudiantes': estudiantes,'consulta':lista}
            else:
                datos = {'Mensaje': "Estudiantes no encontrados"}
            return JsonResponse(datos)

    def post(self, request):
        jsondata = json.loads(request.body)
        Estudiante.objects.create(
            nombre=jsondata['nombre'], apellido=jsondata['apellido'], sexo=jsondata['sexo'], Grupo_id=jsondata['Grupo_id'])
        datos = {'Mensaje': "creado con exito"}
        return JsonResponse(datos)

    def put(self, request, id):
        jsondata = json.loads(request.body)
        estudiantes = list(Estudiante.objects.filter(id=id).values())

        if len(estudiantes) > 0:
            estudiante = Estudiante.objects.get(id=id)
            estudiante.nombre = jsondata['nombre']
            estudiante.apellido = jsondata['apellido']
            estudiante.sexo = jsondata['sexo']
            estudiante.Grupo_id = jsondata['Grupo_id']
            estudiante.save()
            datos = {'Mensaje': "actualización realizada"}
        else:
            datos = {'Mensaje': "Estudiante no encontrados"}
        return JsonResponse(datos)

    def delete(self, request, id):
        estudiantes = list(Estudiante.objects.filter(id=id).values())
        if len(estudiantes) > 0:
            estudiante = Estudiante.objects.filter(id=id).delete()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE sqlite_sequence SET seq=0 WHERE name='api_estudiante'")
                cursor.close()
            datos = {'Mensaje': "eliminación realizada"}
        else:
            datos = {'Mensaje': "Estudiante no encontrados"}
        return JsonResponse(datos)
