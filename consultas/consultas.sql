
/* CONSULTA QUE PERMITE VER LA CANTIDAD DE ESTUDIANTES REGISTRADOS EN UN GRUPO*/
SELECT api_grupo.id,api_grupo.grupo,COUNT(api_estudiante.Grupo_id) As 'Cantidad de estudiantes'
FROM api_grupo 
LEFT JOIN api_estudiante 
ON api_grupo.id=api_estudiante.Grupo_id GROUP BY(api_grupo.grupo)
/*FIN CONSULTA*/

/* CONSULTA PARA VER LAS ASIGNATURAS Y QUE PROFESOR ES EL ENCARGADO */
SELECT api_asignatura.id,api_asignatura.asignatura,api_asignatura.creditos,api_asignatura.Profesor_id,api_profesor.nombre,api_profesor.apellido
FROM api_asignatura
INNER JOIN api_profesor
ON api_asignatura.Profesor_id = api_profesor.id
/* FIN CONSULTA */

/* CREAR VISTA PARA LISTAR ASIGNATURAS */
CREATE VIEW lista_asignaturas 
AS
SELECT api_asignatura.id,api_asignatura.asignatura,api_asignatura.creditos,api_asignatura.Profesor_id,api_profesor.nombre,api_profesor.apellido
FROM api_asignatura
INNER JOIN api_profesor
ON api_asignatura.Profesor_id = api_profesor.id
/* FIN VISTA */

/*CONSULTANDO LA VISTA*/
SELECT * FROM lista_asignaturas
/*FIN*/

/*CONSULTA PARA VER LOS LOGROS DE LAS ASIGNATURAS*/
SELECT api_logro.id,api_logro.logro,api_logro.Asignatura_id,api_asignatura.asignatura
FROM api_logro,api_asignatura
WHERE api_logro.Asignatura_id=api_asignatura.id
/*FIN*/

/*CREAR VISTA*/
CREATE VIEW lista_logros AS
SELECT api_logro.id,api_logro.logro,api_logro.Asignatura_id,api_asignatura.asignatura
FROM api_logro,api_asignatura
WHERE api_logro.Asignatura_id=api_asignatura.id
/*FIN*/

SELECT api_boletin.id,api_boletin.periodo,api_boletin.nota,api_estudiante.nombre,api_asignatura.asignatura
FROM api_boletin,api_estudiante,api_asignatura
WHERE api_boletin.Asignatura_id = api_asignatura.id
GROUP BY(api_boletin.id)


SELECT *
FROM api_logro,api_asignatura
WHERE api_logro.Asignatura_id = 2 AND api_logro.Asignatura_id = api_asignatura.id
GROUP BY(api_logro.logro)

/*CONSULTA PARA BOLETINES*/
SELECT api_boletin.id,api_boletin.periodo,api_boletin.nota,api_boletin.Estudiante_id,api_estudiante.nombre,api_estudiante.apellido,api_boletin.Logro_id,api_logro.logro,api_boletin.Asignatura_id,api_asignatura.asignatura,api_asignatura.creditos
FROM api_boletin,api_estudiante,api_logro,api_asignatura
WHERE api_boletin.Asignatura_id = api_asignatura.id AND api_boletin.Logro_id = api_logro.id AND api_boletin.Estudiante_id = api_estudiante.id
GROUP BY(api_boletin.id)