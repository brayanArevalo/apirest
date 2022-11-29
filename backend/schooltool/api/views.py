from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Grupo
from django.http.response import JsonResponse
from django.db import connection
import json


class GrupoView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if (id > 0):
            grupos = list(Grupo.objects.filter(id=id).values())
            if len(grupos) > 0:
                grupo = grupos[0]
                datos = {'mensaje': "OK", 'grupo': grupo}
            else:
                datos = {'Mensaje': "Grupo no encontrado"}
            return JsonResponse(datos)
        else:
            grupos = list(Grupo.objects.values())
            #print(grupos)
            lista=[]
            with connection.cursor() as cursor:
                consulta = list(cursor.execute("SELECT api_grupo.id,api_grupo.grupo,COUNT(api_estudiante.Grupo_id) As 'Cantidad de estudiantes' FROM api_grupo LEFT JOIN api_estudiante ON api_grupo.id=api_estudiante.Grupo_id GROUP BY(api_grupo.grupo)"))      
                for c in consulta:
                    secuencia = ("id","grupo","cantidad")
                    resultado = list(zip(secuencia, c)) #une los campos de secuencia con c ('id',1) ,('grupo',2)
                    resultado = dict(resultado) #convertir en diccionario {'id':1,'grupo':2}
                    lista=lista+[resultado] #acumulador del diccionario
                cursor.close()
                #print(lista)
            if len(grupos) > 0:
                datos = {'consulta': lista}
            else:
                datos = {'Mensaje': "Grupos no encontrados"}
            return JsonResponse(datos)


    def post(self, request):
        jsondata = json.loads(request.body)
        Grupo.objects.create(
            grupo=jsondata['grupo'])
        datos = {'Mensaje': "creado con exito"}
        return JsonResponse(datos)

    def put(self, request, id):
        jsondata = json.loads(request.body)
        grupos = list(Grupo.objects.filter(id=id).values())

        if len(grupos) > 0:
            grupo = Grupo.objects.get(id=id)
            grupo.grupo = jsondata['grupo']
            grupo.save()
            datos = {'Mensaje': "actualización realizada"}
        else:
            datos = {'Mensaje': "Grupo no encontrados"}
        return JsonResponse(datos)

    def delete(self, request, id):
        grupos = list(Grupo.objects.filter(id=id).values())
        if len(grupos) > 0:
            grupo = Grupo.objects.filter(id=id).delete()

            # query=Grupo.objects.raw("UPDATE sqlite_sequence SET seq=1 WHERE name='api_grupo'")
            # print(query)
            # connection.cursor("UPDATE sqlite_sequence SET seq=1 WHERE name='api_grupo'")
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE sqlite_sequence SET seq=0 WHERE name='api_grupo'")
                cursor.close()
            datos = {'Mensaje': "eliminación realizada"}
        else:
            datos = {'Mensaje': "Grupo no encontrados"}
        return JsonResponse(datos)


