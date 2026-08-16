# Diario técnico — Actualización de Clinic mediante FastAPI

**Proyecto:** Medical CMS Platform  
**Fecha:** 2026-08-15  
**Bloque:** 4 — UPDATE de `Clinic`  
**Rama:** `develop`

---

# 1. Objetivo del bloque

Construir la primera operación de actualización de una entidad mediante FastAPI.

El objetivo fue comprender la diferencia entre crear un objeto nuevo y modificar un objeto que ya existe en PostgreSQL.

La operación implementada fue:

```text
PUT /clinics/{clinic_id}

El recorrido esperado fue:

Cliente
   ↓
PUT /clinics/{clinic_id}
   ↓
FastAPI
   ↓
ClinicUpdate
   ↓
Session
   ↓
update_clinic()
   ↓
buscar Clinic existente
   ↓
modificar atributo
   ↓
commit()
   ↓
PostgreSQL
   ↓
ClinicResponse
   ↓
JSON
2. Situación inicial

Al comenzar este bloque ya estaban funcionando:

PostgreSQL 17 mediante Docker Compose.
SQLAlchemy 2.0.
Psycopg 3.
engine.
Base.
SessionLocal.
get_db().
Modelo Clinic.
Tabla clinics.
create_clinic().
get_clinics().
get_clinic().
ClinicCreate.
ClinicResponse.
POST /clinics/.
GET /clinics/.
GET /clinics/{clinic_id}.

Estado de CRUD antes de este bloque:

CREATE
POST /clinics/              ✅


READ
GET /clinics/               ✅
GET /clinics/{clinic_id}    ✅


UPDATE
PUT /clinics/{clinic_id}    ⏳


DELETE
DELETE /clinics/{clinic_id} ⏳
3. Concepto de UPDATE

Se aprendió que actualizar un registro existente no significa crear otro objeto.

En CREATE:

Objeto nuevo
   ↓
add()
   ↓
commit()
   ↓
INSERT

En UPDATE:

Buscar objeto existente
   ↓
Modificar atributo
   ↓
commit()
   ↓
UPDATE

La idea fundamental:

Para modificar una entidad que SQLAlchemy ya está gestionando, no necesitamos crear un segundo objeto ni hacer add() nuevamente.

4. Diferencia entre CREATE y UPDATE
CREATE
clinic = Clinic(
    name=name
)


db.add(clinic)
db.commit()
db.refresh(clinic)

Conceptualmente:

Clinic no existe
↓
crear objeto
↓
INSERT
UPDATE
clinic = obtener_clinic(...)


clinic.name = name


db.commit()
db.refresh(clinic)

Conceptualmente:

Clinic ya existe
↓
buscar objeto
↓
modificar atributo
↓
UPDATE

Esta diferencia fue uno de los principales conceptos del bloque.

5. Intento inicial realizado por el desarrollador

Antes de recibir la solución completa se intentó construir update_clinic() de forma independiente.

Primer intento:

def update_clinic(db: Session, name: str) -> Clinic:
    clinic = Clinic(
        name=name
    )


    try:
        db.commit()


        return clinic


    except Exception:
        db.rollback()
        raise

Se detectó que este enfoque estaba creando un nuevo objeto Clinic, lo cual corresponde a CREATE y no a UPDATE.

6. Segundo intento

Se realizó un segundo intento utilizando conceptos ya aprendidos:

def update_clinic(db: Session, clinic_id: int, name: str) -> Clinic | None:
    statement = select(Clinic).where(Clinic.id == clinic_id)
    result = db.execute(statement)
    clinic = result.scalar_one_or_none()


    if clinic == name:
        clinic.name = name


    try:
        db.commit()
        db.refresh()


        return clinic


    except Exception:
        db.rollback()
        raise

Se identificaron y corrigieron dos problemas principales:

Comparación incorrecta
if clinic == name:

comparaba:

objeto Clinic
vs.
texto

Lo correcto era comprobar si el registro existía:

if clinic is None:
refresh() sin objeto

Se utilizó:

db.refresh()

pero refresh() necesita recibir el objeto que debe actualizar:

db.refresh(clinic)
7. Implementación definitiva de update_clinic()

La implementación corregida fue:

def update_clinic(
    db: Session,
    clinic_id: int,
    name: str,
) -> Clinic | None:
    statement = select(Clinic).where(Clinic.id == clinic_id)


    result = db.execute(statement)


    clinic = result.scalar_one_or_none()


    if clinic is None:
        return None


    clinic.name = name


    try:
        db.commit()
        db.refresh(clinic)


        return clinic


    except Exception:
        db.rollback()
        raise
8. Explicación del flujo de update_clinic()
Buscar la clínica
statement = select(Clinic).where(Clinic.id == clinic_id)

Se busca una clínica concreta mediante su identificador.

Ejemplo:

clinic_id = 3

equivale conceptualmente a:

SELECT ...
FROM clinics
WHERE id = 3;
Ejecutar la consulta
result = db.execute(statement)

La consulta se ejecuta mediante la Session.

Obtener un único resultado o None
clinic = result.scalar_one_or_none()

Se obtienen dos posibles escenarios:

Clínica encontrada
↓
Clinic

o:

Clínica inexistente
↓
None
9. Verificación de existencia

Se utiliza:

if clinic is None:
    return None

Esto mantiene la responsabilidad del service separada de la respuesta HTTP.

El service responde conceptualmente:

Existe
↓
Clinic


No existe
↓
None

El endpoint posteriormente interpreta None como:

404 Not Found
10. Modificación del objeto existente

La operación fundamental del bloque es:

clinic.name = name

Esto significa:

Modificar el atributo name del objeto Clinic que acabamos de recuperar desde la base de datos.

No hacemos:

clinic = Clinic(...)

porque eso crearía otro objeto.

El flujo correcto es:

PostgreSQL
   ↓
Clinic existente
   ↓
objeto Python
   ↓
clinic.name = nuevo_nombre
11. commit() en UPDATE

Después:

db.commit()

SQLAlchemy confirma la modificación.

Conceptualmente:

objeto existente
   ↓
atributo modificado
   ↓
commit()
   ↓
UPDATE
   ↓
PostgreSQL
12. refresh() en UPDATE

Después del commit():

db.refresh(clinic)

permite volver a cargar desde PostgreSQL el estado actual del objeto.

El flujo completo queda:

buscar
↓
modificar
↓
commit()
↓
refresh()
↓
return
13. Manejo de errores

El patrón utilizado es:

try:
    db.commit()
    db.refresh(clinic)


    return clinic


except Exception:
    db.rollback()
    raise

El rollback() se utiliza si la operación de persistencia falla.

No se utiliza para errores de validación HTTP como 422.

14. Nuevo schema — ClinicUpdate

Se agregó en:

backend/app/schemas/clinic.py
class ClinicUpdate(BaseModel):
    name: str

Responsabilidad:

ClinicCreate
↓
datos para crear




ClinicUpdate
↓
datos para actualizar




ClinicResponse
↓
datos que devuelve la API
15. Endpoint PUT /clinics/{clinic_id}

Se agregó en:

backend/app/routes/clinic.py
@router.put(
    "/{clinic_id}",
    response_model=ClinicResponse,
    responses={
        404: {
            "description": "No se encontró la clínica solicitada",
        }
    },
)
def update_clinic_endpoint(
    clinic_id: int,
    clinic_data: ClinicUpdate,
    db: Session = Depends(get_db),
):
    clinic = update_clinic(
        db=db,
        clinic_id=clinic_id,
        name=clinic_data.name,
    )


    if clinic is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró la clínica solicitada",
        )


    return clinic
16. Lectura del endpoint

El endpoint recibe:

clinic_id

Desde la URL:

PUT /clinics/3

FastAPI interpreta:

clinic_id = 3
clinic_data

Desde el body:

{
  "name": "Clínica del Norte Premium"
}

FastAPI utiliza:

ClinicUpdate

para validar la entrada.

17. Flujo completo de UPDATE
Cliente
   ↓
PUT /clinics/3
   ↓
clinic_id = 3
   ↓
ClinicUpdate
   ↓
{
     "name": "Clínica del Norte Premium"
}
   ↓
update_clinic()
   ↓
buscar Clinic 3
   ↓
¿Existe?
   ├── No → None → 404
   │
   └── Sí
        ↓
   clinic.name = nuevo nombre
        ↓
      commit()
        ↓
      refresh()
        ↓
    PostgreSQL
        ↓
  ClinicResponse
        ↓
       JSON
18. Prueba real de actualización

La clínica seleccionada fue:

id = 3

Estado anterior:

3 → Clínica del Norte Central

Se realizó un:

PUT /clinics/3

para modificarla.

Estado posterior:

3 → Clínica del Norte Premium

La API confirmó correctamente la actualización.

19. Verificación directa en PostgreSQL

Se realizó una consulta directa:

SELECT * FROM clinics
WHERE id = 3;

Resultado:

(3, 'Clínica del Norte Premium')

Esto confirmó que la modificación no se quedó solamente en el objeto Python.

El cambio fue realmente persistido en PostgreSQL.

20. Prueba de clínica inexistente

También se probó:

PUT /clinics/999

Como la clínica no existe:

get_clinic(...)

devuelve:

None

El endpoint detecta el caso:

if clinic is None:

y devuelve:

404 Not Found

Respuesta conceptual:

{
  "detail": "No se encontró la clínica solicitada"
}
21. OpenAPI

La documentación de FastAPI fue comprobada.

El endpoint:

PUT /clinics/{clinic_id}

documenta:

clinic_id
↓
path
↓
integer
↓
required

Request body:

ClinicUpdate

Responses:

200 → Successful Response
404 → No se encontró la clínica solicitada
422 → Validation Error
22. Problema de codificación

Durante el bloque apareció una representación incorrecta de caracteres:

No se encontrÃ³ la clÃnica solicitada

Se comprobó que el comportamiento de la API era correcto, pero el archivo contenía una representación incorrecta del texto.

Para evitar alterar la lógica del sistema se corrigió la representación del texto y se verificó mediante OpenAPI que FastAPI mostrara correctamente:

No se encontró la clínica solicitada

El resultado final quedó correctamente interpretado tanto para GET como para PUT.

23. Diferencia entre UPDATE y CREATE

Concepto fundamental consolidado:

CREATE
Clinic(...)
↓
objeto nuevo
↓
add()
↓
commit()
↓
INSERT
UPDATE
buscar Clinic
↓
objeto existente
↓
modificar atributo
↓
commit()
↓
UPDATE

No se utiliza add() nuevamente para el objeto existente.

24. Código permanente incorporado

Se modificó:

backend/app/schemas/clinic.py

para incorporar:

class ClinicUpdate(BaseModel):
    name: str

Se modificó:

backend/app/services/clinic_service.py

para incorporar:

def update_clinic(...)

Se modificó:

backend/app/routes/clinic.py

para incorporar:

PUT /clinics/{clinic_id}

No se modificó:

modelo Clinic;
database.py;
get_db();
PostgreSQL;
Docker.
25. Pruebas realizadas

Se verificó:

✅ ClinicUpdate
✅ update_clinic()
✅ búsqueda por clinic_id
✅ modificación de atributo
✅ commit()
✅ refresh()
✅ PUT /clinics/{clinic_id}
✅ HTTP 200
✅ HTTP 404
✅ Swagger
✅ OpenAPI
✅ persistencia real en PostgreSQL
✅ manejo de clínica inexistente
26. Estado del CRUD de Clinic

Al finalizar este bloque:

CREATE
POST /clinics/              ✅


READ
GET /clinics/               ✅
GET /clinics/{clinic_id}    ✅


UPDATE
PUT /clinics/{clinic_id}    ✅


DELETE
DELETE /clinics/{clinic_id} ⏳

Esto representa tres de las cuatro operaciones básicas del CRUD.

27. Estado del bloque

Estado: COMPLETADO

Completado
Concepto de UPDATE.
Diferencia entre CREATE y UPDATE.
ClinicUpdate.
update_clinic().
Búsqueda por identificador.
Modificación de un objeto existente.
commit().
refresh().
PUT /clinics/{clinic_id}.
HTTP 200.
HTTP 404.
OpenAPI.
Swagger.
Verificación directa en PostgreSQL.
Manejo del recurso inexistente.
Corrección del texto mostrado por la API.
Pendiente
DELETE de Clinic.
Validaciones de negocio.
Manejo más específico de errores de base de datos.
Evolución futura hacia CRUD de otras entidades.

No se incorporan todavía para mantener el desarrollo progresivo.

28. Próximo bloque

El siguiente bloque será:

DELETE /clinics/{clinic_id}

Antes de implementarlo se estudiará:

qué significa eliminar un recurso;
diferencia entre eliminar el objeto y confirmar la eliminación;
cómo utilizar db.delete();
cuándo utilizar commit();
cómo manejar una clínica inexistente;
qué respuesta HTTP debe devolver el endpoint.

El objetivo será completar el CRUD básico de Clinic.

29. Git y GitHub

Antes del cierre definitivo del bloque se debe revisar:

git status
git --no-pager diff --check
git add
git --no-pager diff --cached --check
git --no-pager diff --cached

Después:

commit
↓
push origin develop

La documentación de este bloque se mantiene en un archivo independiente para conservar un historial cronológico y evitar modificar documentos de bloques anteriores ya cerrados.

Archivo:

docs/technical-journal/2026-08-15-clinic-update-endpoint.md
30. Estado general del proyecto
Medical CMS Platform


Stack
✅ Python
✅ FastAPI
✅ SQLAlchemy 2.0
✅ Psycopg 3
✅ PostgreSQL 17
✅ Docker
✅ Docker Compose


Base
✅ Engine
✅ Base
✅ SessionLocal
✅ get_db()
✅ Clinic


API
✅ POST /clinics/
✅ GET /clinics/
✅ GET /clinics/{clinic_id}
✅ PUT /clinics/{clinic_id}


Schemas
✅ ClinicCreate
✅ ClinicResponse
✅ ClinicUpdate


CRUD
✅ Create
✅ Read — lista
✅ Read — por id
✅ Update
⏳ Delete


Documentación
✅ Bloque 1
✅ Bloque 2
✅ Bloque 3
✅ Bloque 4


Git/GitHub
⏳ Cierre del Bloque 4


Próximo
⏳ DELETE de Clinic
31. Metodología mantenida

Este bloque siguió exactamente la metodología acordada:

Concepto
    ↓
Explicación sencilla
    ↓
Ejemplo
    ↓
Intento propio
    ↓
Corrección
    ↓
Aplicación al proyecto
    ↓
Prueba
    ↓
Verificación
    ↓
Código definitivo
    ↓
Documentación
    ↓
Git/GitHub
    ↓
Siguiente bloque