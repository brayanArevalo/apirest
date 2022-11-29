from django.db import models

from .choices import sexos

class Grupo (models.Model):
    grupo = models.CharField(max_length=50)

    def nombre_curso(self):
        return "{},{},{}".format(self.id,self.grupo,self.can_estudiantes)

    def __srt__(self):
        return self.nombre_curso()


class Estudiante(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    Grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    sexo = models.CharField(max_length=1,choices=sexos,default='M')




class Profesor (models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    cedula = models.CharField(max_length=10)
    telefono = models.CharField(max_length=10)
    sexo = models.CharField(max_length=1,choices=sexos,default='M')


class Asignatura(models.Model):
    asignatura = models.CharField(max_length=50)
    creditos = models.PositiveIntegerField()
    Profesor = models.ForeignKey(Profesor,related_name="profesor_asignatura",on_delete=models.CASCADE)


class Logro(models.Model):
    logro = models.TextField()
    Asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)


class Boletin(models.Model):
    Asignatura = models.ForeignKey(Asignatura,related_name="asignaturas",on_delete=models.CASCADE)
    Logro = models.ForeignKey(Logro,related_name="logros",on_delete=models.CASCADE)
    Estudiante = models.ForeignKey(Estudiante, related_name="estudiantes",on_delete=models.CASCADE)
    periodo = models.CharField(max_length=50)
    nota = models.FloatField()
    
