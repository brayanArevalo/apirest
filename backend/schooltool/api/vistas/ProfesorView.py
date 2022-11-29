from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from api.models import Profesor
from django.http.response import JsonResponse
from django.db import connection
import json

class ProfesorView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get(self, request, id=0):
        if (id > 0):
            profesores = list(Profesor.objects.filter(id=id).values())
            if len(profesores) > 0:
                profesor = profesores[0]
                datos = {'mensaje': "OK", 'profesor': profesor}
            else:
                datos = {'Mensaje': "Profesor no encontrado"}
            return JsonResponse(datos)
        else:
            profesores = list(Profesor.objects.values())
            if len(profesores) > 0:
                datos = {'Mensaje': "OK",
                         'profesores': profesores}
            else:
                datos = {'Mensaje': "Profesores no encontrados"}
            return JsonResponse(datos)

    def post(self, request):
        jsondata = json.loads(request.body)
        Profesor.objects.create(
            nombre=jsondata['nombre'],apellido=jsondata['apellido'],telefono=jsondata['telefono'],
            cedula=jsondata['cedula'],sexo=jsondata['sexo'])
        datos = {'Mensaje': "creado con exito"}
        return JsonResponse(datos)

    def put(self, request, id):
        jsondata = json.loads(request.body)
        profesores = list(Profesor.objects.filter(id=id).values())

        if len(profesores) > 0:
            profesor = Profesor.objects.get(id=id)
            profesor.nombre = jsondata['nombre']
            profesor.apellido = jsondata['apellido']
            profesor.telefono = jsondata['telefono']
            profesor.cedula = jsondata['cedula']
            profesor.sexo = jsondata['sexo']
            profesor.save()
            datos = {'Mensaje': "actualización realizada"}
        else:
            datos = {'Mensaje': "Profesor no encontrado"}
        return JsonResponse(datos)

    def delete(self, request, id):
        profesores = list(Profesor.objects.filter(id=id).values())
        if len(profesores) > 0:
            profesor = Profesor.objects.filter(id=id).delete()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE sqlite_sequence SET seq=0 WHERE name='api_profesor'")
                cursor.close()
            datos = {'Mensaje': "eliminación realizada"}
        else:
            datos = {'Mensaje': "Profesor no encontrado"}
        return JsonResponse(datos)