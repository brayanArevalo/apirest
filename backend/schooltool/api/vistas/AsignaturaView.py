from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from api.models import Asignatura
from django.http.response import JsonResponse
from django.db import connection
import json


class AsignaturaView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if (id > 0):
            asignaturas = list(Asignatura.objects.filter(id=id).values())
            if len(asignaturas) > 0:
                asignatura = asignaturas[0]
                datos = {'mensaje': "OK", 'asignatura': asignatura}
            else:
                datos = {'Mensaje': "Asignatura no encontrado"}
            return JsonResponse(datos)
        else:
            with connection.cursor() as cursor:
                consulta = list(cursor.execute("SELECT * FROM lista_asignaturas"))
                lista = []
                for c in consulta:
                    secuencia = ("id", "asignatura", "creditos","Profesor_id", "nombre", "apellido")
                    resultado = list(zip(secuencia, c))
                    resultado = dict(resultado)
                    lista = lista+[resultado]
                cursor.close()
                print(lista)
            # FIN CONSULTA SQL
            asignaturas = list(Asignatura.objects.values())
            if len(asignaturas) > 0:
                datos = {'Mensaje': "OK",
                         'asignaturas': asignaturas, 'consulta': lista}
            else:
                datos = {'Mensaje': "Asignaturas no encontradas"}
            return JsonResponse(datos)

    def post(self, request):
        jsondata = json.loads(request.body)
        Asignatura.objects.create(
            creditos=jsondata['creditos'], asignatura=jsondata['asignatura'],Profesor_id=jsondata['Profesor_id'])
        datos = {'Mensaje': "creado con exito"}
        return JsonResponse(datos)

    def put(self, request, id):
        jsondata = json.loads(request.body)
        asignaturas = list(Asignatura.objects.filter(id=id).values())

        if len(asignaturas) > 0:
            asignatura = Asignatura.objects.get(id=id)
            asignatura.creditos = jsondata['creditos']
            asignatura.asignatura = jsondata['asignatura']
            asignatura.Profesor_id = jsondata['Profesor_id']
            asignatura.save()
            datos = {'Mensaje': "actualización realizada"}
        else:
            datos = {'Mensaje': "Asignatura no encontrados"}
        return JsonResponse(datos)

    def delete(self, request, id):
        asignaturas = list(Asignatura.objects.filter(id=id).values())
        if len(asignaturas) > 0:
            asignatura = Asignatura.objects.filter(id=id).delete()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE sqlite_sequence SET seq=0 WHERE name='api_asignatura'")
                cursor.close()
            datos = {'Mensaje': "eliminación realizada"}
        else:
            datos = {'Mensaje': "Asignatura no encontrados"}
        return JsonResponse(datos)
