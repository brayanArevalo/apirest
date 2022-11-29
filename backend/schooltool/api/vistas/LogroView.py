from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from api.models import Logro
from django.http.response import JsonResponse
from django.db import connection
import json


class LogroView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if (id > 0):
            logros = list(Logro.objects.filter(id=id).values())
            if len(logros) > 0:
                logro = logros[0]
                datos = {'mensaje': "OK", 'logro': logro}
            else:
                datos = {'Mensaje': "Logro no encontrado"}
            return JsonResponse(datos)
        else:
            # CONSULTA SQL
            with connection.cursor() as cursor:
                consulta = list(cursor.execute("SELECT * FROM lista_logros"))
                lista = []
                for c in consulta:
                    secuencia = ("id", "logro", "Asignatura_id","asignatura")
                    resultado = list(zip(secuencia, c))
                    resultado = dict(resultado)
                    lista = lista+[resultado]
                cursor.close()
                print(lista)
            # FIN CONSULTA SQL
            logros = list(Logro.objects.values())
            if len(logros) > 0:
                datos = {'Mensaje': "OK",
                         'logros': lista}
            else:
                datos = {'Mensaje': "Logros no encontrados"}
            return JsonResponse(datos)

    def post(self, request):
        jsondata = json.loads(request.body)
        Logro.objects.create(
            logro=jsondata['logro'], Asignatura_id=jsondata['Asignatura_id'])
        datos = {'Mensaje': "creado con exito"}
        return JsonResponse(datos)

    def put(self, request, id):
        jsondata = json.loads(request.body)
        logros = list(Logro.objects.filter(id=id).values())

        if len(logros) > 0:
            logro = Logro.objects.get(id=id)
            logro.logro = jsondata['logro']
            logro.Asignatura_id = jsondata['Asignatura_id']
            logro.save()
            datos = {'Mensaje': "actualización realizada"}
        else:
            datos = {'Mensaje': "Logro no encontrados"}
        return JsonResponse(datos)

    def delete(self, request, id):
        logros = list(Logro.objects.filter(id=id).values())
        if len(logros) > 0:
            logro = Logro.objects.filter(id=id).delete()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE sqlite_sequence SET seq=0 WHERE name='api_logro'")
                cursor.close()
            datos = {'Mensaje': "eliminación realizada"}
        else:
            datos = {'Mensaje': "Logro no encontrados"}
        return JsonResponse(datos)
