from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from api.models import Boletin
from django.http.response import JsonResponse
from django.db import connection
import json


class BoletinView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if (id > 0):
            boletines = list(Boletin.objects.filter(id=id).values())
            if len(boletines) > 0:
                boletin = boletines[0]
                datos = {'mensaje': "OK", 'boletin': boletin}
            else:
                datos = {'Mensaje': "Boletin no encontrado"}
            return JsonResponse(datos)
        else:

            #CONSULTA SQL
            with connection.cursor() as cursor:
                consulta = list(cursor.execute("SELECT * FROM lista_boletines"))
                #print(consulta)                
                lista = []
                for c in consulta:
                    secuencia = ("id", "periodo", "nota","Estudiante_id", "nombre", "apellido","Logro_id","logro","Asignatura_id","asignatura","creditos")
                    resultado = list(zip(secuencia, c))
                    resultado = dict(resultado)
                    lista = lista+[resultado]
                cursor.close()
                #print(lista)
            # FIN CONSULTA SQL
            boletines = list(Boletin.objects.values())
            if len(boletines) > 0:
                datos = {'Mensaje': "OK",
                         'boletines': boletines,'consulta':lista}
            else:
                datos = {'Mensaje': "Boletines no encontrados"}
            return JsonResponse(datos)

    def post(self, request):
        jsondata = json.loads(request.body)
        Boletin.objects.create(
            periodo=jsondata['periodo'], nota=jsondata['nota'], Asignatura_id=jsondata['Asignatura_id'],
            Estudiante_id=jsondata['Estudiante_id'], Logro_id=jsondata['Logro_id'])
        datos = {'Mensaje': "creado con exito"}
        return JsonResponse(datos)

    def put(self, request, id):
        jsondata = json.loads(request.body)
        boletines = list(Boletin.objects.filter(id=id).values())

        if len(boletines) > 0:
            boletin = Boletin.objects.get(id=id)
            boletin.periodo = jsondata['periodo']
            boletin.nota = jsondata['nota']
            boletin.Asignatura_id = jsondata['Asignatura_id']
            boletin.Estudiante_id = jsondata['Estudiante_id']
            boletin.Logro_id = jsondata['Logro_id']
            #boletin.boletin = jsondata['boletin']
            boletin.Asignatura_id = jsondata['Asignatura_id']
            boletin.save()
            datos = {'Mensaje': "actualización realizada"}
        else:
            datos = {'Mensaje': "Boletin no encontrados"}
        return JsonResponse(datos)

    def delete(self, request, id):
        boletines = list(Boletin.objects.filter(id=id).values())
        if len(boletines) > 0:
            boletin = Boletin.objects.filter(id=id).delete()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE sqlite_sequence SET seq=0 WHERE name='api_boletin'")
                cursor.close()
            datos = {'Mensaje': "eliminación realizada"}
        else:
            datos = {'Mensaje': "Boletin no encontrados"}
        return JsonResponse(datos)
