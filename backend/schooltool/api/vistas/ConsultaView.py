from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from api.models import Asignatura
from django.db import connection
import json


class ConsultaView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request,id=0):
        with connection.cursor() as cursor:
            query = 'SELECT api_logro.id,api_logro.logro,api_logro.Asignatura_id,api_asignatura.asignatura FROM api_logro,api_asignatura WHERE api_logro.Asignatura_id=api_asignatura.id AND api_logro.Asignatura_id= %s GROUP BY (api_logro.logro)',[id]
            consulta = list(cursor.execute('SELECT api_logro.id,api_logro.logro,api_logro.Asignatura_id,api_asignatura.asignatura FROM api_logro,api_asignatura WHERE api_logro.Asignatura_id=api_asignatura.id AND api_logro.Asignatura_id= %s GROUP BY (api_logro.logro)',[id]))
            
            lista = []
            for c in consulta:
                    secuencia=("id","logro","Asignatura_id","asignatura")
                    resultado = list(zip(secuencia, c))
                    resultado = dict(resultado)
                    lista = lista+[resultado]  
            cursor.close()
            print(lista)
            print(query)
            datos={'consulta':lista}
            
        return JsonResponse (datos) 

        # # CONSULTA SQL    
        # with connection.cursor() as cursor:            
        #     consulta = list(cursor.execute('SELECT api_estudiante.id,nombre,apellido,sexo,Grupo_id,grupo FROM api_estudiante,api_grupo WHERE api_estudiante.Grupo_id = %s GROUP BY(api_estudiante.nombre)',[id]))
        #     print(consulta)
        #     datos = {'consulta':consulta}
        #     return JsonResponse (datos) 
        # #FIN CONSULTA SQL

