# Diario técnico — Eliminación de Clinic mediante FastAPI

**Proyecto:** Medical CMS Platform  
**Fecha:** 2026-08-15  
**Bloque:** 5 — DELETE de `Clinic`  
**Rama:** `develop`

---

# 1. Objetivo del bloque

Construir la operación de eliminación de una clínica mediante FastAPI.

El objetivo fue comprender cómo SQLAlchemy elimina un objeto existente y cómo FastAPI comunica al cliente el resultado de la operación.

La operación implementada fue:

```text
DELETE /clinics/{clinic_id}

El recorrido esperado fue:

Cliente
   ↓
DELETE /clinics/{clinic_id}
   ↓
FastAPI
   ↓
clinic_id
   ↓
Session
   ↓
delete_clinic()
   ↓
buscar Clinic existente
   ↓
db.delete()
   ↓
db.commit()
   ↓
PostgreSQL
   ↓
204 No Content

También se incorporó el manejo de una clínica inexistente:

DELETE /clinics/999
        ↓
404 Not Found
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
update_clinic().
ClinicCreate.
ClinicUpdate.
ClinicResponse.
POST /clinics/.
GET /clinics/.
GET /clinics/{clinic_id}.
PUT /clinics/{clinic_id}.

Estado del CRUD antes de este bloque:

CREATE
POST /clinics/              ✅


READ
GET /clinics/               ✅
GET /clinics/{clinic_id}    ✅


UPDATE
PUT /clinics/{clinic_id}    ✅


DELETE
DELETE /clinics/{clinic_id} ⏳
3. Concepto de DELETE

Se aprendió que DELETE se utiliza para solicitar la eliminación de un recurso.

Ejemplo:

DELETE /clinics/7

se interpreta como:

Eliminar la clínica cuyo id es 7.

La idea mental utilizada fue:

POST
↓
crear


GET
↓
consultar


PUT
↓
modificar


DELETE
↓
eliminar
4. Diferencia entre CREATE, UPDATE y DELETE

Durante el bloque se consolidó la diferencia entre las tres operaciones.

CREATE
Clinic(...)
↓
db.add()
↓
db.commit()
↓
INSERT

La clínica todavía no existía.

UPDATE
buscar Clinic existente
↓
modificar atributo
↓
db.commit()
↓
UPDATE

La clínica ya existía y se modifica uno de sus atributos.

DELETE
buscar Clinic existente
↓
db.delete()
↓
db.commit()
↓
DELETE

La clínica ya existe y se solicita su eliminación.

5. Intento inicial

Se realizó un primer intento de crear un schema:

class ClinicDelete(BaseModel):
    name: str

y una función:

def delete_clinic(
    db: Session,
    clinic_id: int,
    name: str,
) -> Clinic:

También se utilizó:

db.refresh(clinic)

Se identificaron varios problemas conceptuales.

6. No se necesita ClinicDelete

Se comprobó que el DELETE actual solamente necesita identificar qué clínica debe eliminar.

La URL:

DELETE /clinics/7

ya contiene toda la información necesaria mediante:

clinic_id = 7

Por lo tanto no se necesita:

class ClinicDelete(BaseModel):
    name: str

No se agregó ningún schema específico para DELETE.

La diferencia quedó:

POST
↓
ClinicCreate




PUT
↓
ClinicUpdate




GET
↓
sin request body




DELETE
↓
sin request body
7. No se necesita name para DELETE

La función de eliminación no necesita recibir:

name: str

porque el nombre no participa en la identificación del registro.

La función necesita solamente:

db: Session
clinic_id: int

Por lo tanto:

def delete_clinic(
    db: Session,
    clinic_id: int,
) -> bool:
8. No se utiliza refresh() después de DELETE

Se observó que inicialmente se intentó utilizar:

db.refresh(clinic)

Después de eliminar un objeto, esto no corresponde.

La razón es que:

db.delete(clinic)
↓
commit()
↓
registro eliminado

Después del commit() el registro ya no debería existir en PostgreSQL.

Por lo tanto no tiene sentido pedirle a SQLAlchemy que vuelva a cargar un objeto que acabamos de eliminar.

Comparación:

CREATE
↓
commit()
↓
refresh()
UPDATE
↓
commit()
↓
refresh()
DELETE
↓
commit()
↓
fin
9. Implementación definitiva de delete_clinic()

La función quedó conceptualmente:

def delete_clinic(
    db: Session,
    clinic_id: int,
) -> bool:
    statement = select(Clinic).where(Clinic.id == clinic_id)


    result = db.execute(statement)


    clinic = result.scalar_one_or_none()


    if clinic is None:
        return False


    try:
        db.delete(clinic)
        db.commit()


        return True


    except Exception:
        db.rollback()
        raise
10. Búsqueda de la clínica

Antes de eliminar debemos localizar el objeto.

Se utiliza:

statement = select(Clinic).where(Clinic.id == clinic_id)

y:

result = db.execute(statement)

Después:

clinic = result.scalar_one_or_none()

El resultado puede ser:

Clinic

o:

None
11. Si la clínica no existe

Se utiliza:

if clinic is None:
    return False

El service comunica:

True
↓
eliminación realizada




False
↓
la clínica no existía

Esto permite mantener la separación entre:

Service
↓
resultado de la operación




Endpoint
↓
respuesta HTTP
12. db.delete()

La nueva pieza principal aprendida fue:

db.delete(clinic)

Esto indica a SQLAlchemy que el objeto debe eliminarse de la base de datos cuando se confirme la transacción.

Conceptualmente:

Clinic existente
      ↓
db.delete()
      ↓
objeto marcado para eliminación

Todavía no se ha confirmado la operación.

13. commit() en DELETE

Después:

db.commit()

confirma la transacción.

El flujo completo es:

Clinic existente
      ↓
db.delete(clinic)
      ↓
db.commit()
      ↓
DELETE
      ↓
PostgreSQL
14. rollback()

La operación conserva el patrón utilizado en las operaciones de escritura:

try:
    db.delete(clinic)
    db.commit()


    return True


except Exception:
    db.rollback()
    raise

Si PostgreSQL o SQLAlchemy encuentran un error durante la transacción, se ejecuta:

db.rollback()

para cancelar los cambios pendientes.

15. Endpoint DELETE

Se incorporó en:

backend/app/routes/clinic.py

la ruta:

@router.delete(
    "/{clinic_id}",
    status_code=204,
    responses={
        404: {
            "description": "No se encontró la clínica solicitada",
        }
    },
)
def delete_clinic_endpoint(
    clinic_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_clinic(
        db=db,
        clinic_id=clinic_id,
    )


    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="No se encontró la clínica solicitada",
        )
16. Parámetro de ruta

La URL:

DELETE /clinics/7

hace que FastAPI interprete:

clinic_id = 7

La función recibe:

clinic_id: int

Por lo tanto:

URL
↓
clinic_id
↓
delete_clinic()
17. 204 No Content

Se utilizó:

status_code=204

Esto significa:

La operación fue exitosa pero la respuesta no contiene contenido.

Por lo tanto el DELETE no devuelve:

{
  "id": 7,
  "name": "..."
}

sino:

204 No Content

La diferencia conceptual es:

200
↓
éxito + contenido




204
↓
éxito + sin contenido
18. Manejo de 404

Si el clinic_id no existe:

delete_clinic(...)

devuelve:

False

El endpoint interpreta ese resultado:

if not deleted:

y genera:

raise HTTPException(
    status_code=404,
    detail="No se encontró la clínica solicitada",
)

Por lo tanto:

DELETE /clinics/999
↓
buscar
↓
None
↓
False
↓
404
19. OpenAPI

Se comprobó que FastAPI documenta el endpoint:

DELETE /clinics/{clinic_id}

con:

clinic_id
↓
path
↓
integer
↓
required

Y las respuestas:

204 → Successful Response
404 → No se encontró la clínica solicitada
422 → Validation Error

Esto confirmó que el endpoint está correctamente integrado en la documentación automática.

20. Prueba controlada

Para probar DELETE se utilizó una clínica destinada a la prueba.

El objetivo fue evitar eliminar accidentalmente cualquiera de las clínicas que queríamos conservar como datos base.

El flujo de prueba fue:

Crear clínica de prueba
↓
obtener su id
↓
DELETE /clinics/{id}
↓
204
↓
verificar PostgreSQL
21. Verificación de PostgreSQL

Después de ejecutar el DELETE se consultó directamente:

SELECT * FROM clinics ORDER BY id;

Resultado final:

1 → Clínica Central
2 → Clínica del Oeste
3 → Clínica del Norte Premium
5 → Clínica del Sur
7 → Clinica especial del Oeste

La clínica utilizada para la prueba de DELETE ya no aparecía.

Esto confirmó que:

db.delete()
↓
commit()
↓
PostgreSQL
↓
registro eliminado

La eliminación no fue solamente una modificación del objeto Python; quedó persistida realmente en la base de datos.

22. Prueba de recurso inexistente

También se probó:

DELETE /clinics/999

Resultado:

404 Not Found

Esto confirmó que la API maneja correctamente el caso en el que la clínica no existe.

23. Pruebas realizadas

Se verificó:

✅ delete_clinic()
✅ db.delete()
✅ commit()
✅ rollback()
✅ DELETE /clinics/{clinic_id}
✅ status_code=204
✅ HTTP 204
✅ HTTP 404
✅ OpenAPI
✅ Swagger
✅ eliminación real en PostgreSQL
✅ manejo de clínica inexistente
24. CRUD básico completo de Clinic

Con este bloque se completaron las cuatro operaciones principales:

CREATE
POST /clinics/              ✅


READ
GET /clinics/               ✅
GET /clinics/{clinic_id}    ✅


UPDATE
PUT /clinics/{clinic_id}    ✅


DELETE
DELETE /clinics/{clinic_id} ✅

Por primera vez tenemos un CRUD completo funcional dentro del proyecto.

25. Arquitectura actual de Clinic

El flujo actual para las operaciones de Clinic queda:

CLIENTE
   ↓
FASTAPI
   ↓
ROUTER
   ↓
SCHEMA
   ↓
SERVICE
   ↓
SQLALCHEMY SESSION
   ↓
POSTGRESQL
   ↓
RESPONSE SCHEMA
   ↓
JSON

Para DELETE:

CLIENTE
   ↓
DELETE /clinics/{clinic_id}
   ↓
ROUTER
   ↓
clinic_id
   ↓
delete_clinic()
   ↓
select()
   ↓
scalar_one_or_none()
   ↓
db.delete()
   ↓
commit()
   ↓
POSTGRESQL
   ↓
204
26. Conceptos consolidados durante los bloques CRUD

Con el CRUD completo de Clinic se consolidaron:

select()
where()
execute()
scalars()
all()
scalar_one_or_none()


db.add()
db.delete()
db.commit()
db.refresh()
db.rollback()


POST
GET
PUT
DELETE


200
204
404
422


APIRouter
Depends()
response_model
HTTPException
OpenAPI
Swagger
27. Comparación de las operaciones CRUD
CREATE
POST /clinics/
↓
ClinicCreate
↓
Clinic()
↓
add()
↓
commit()
↓
refresh()
↓
ClinicResponse
↓
200
READ ALL
GET /clinics/
↓
select()
↓
execute()
↓
scalars().all()
↓
list[ClinicResponse]
↓
200
READ ONE
GET /clinics/{clinic_id}
↓
select()
↓
where()
↓
scalar_one_or_none()
↓
Clinic / None
↓
200 / 404
UPDATE
PUT /clinics/{clinic_id}
↓
ClinicUpdate
↓
buscar
↓
modificar atributo
↓
commit()
↓
refresh()
↓
ClinicResponse
↓
200 / 404
DELETE
DELETE /clinics/{clinic_id}
↓
buscar
↓
db.delete()
↓
commit()
↓
True / False
↓
204 / 404
28. Lección importante del CRUD

Durante estos bloques se aprendió que no todas las operaciones tienen exactamente el mismo comportamiento.

CREATE
↓
crear objeto




READ
↓
consultar objeto




UPDATE
↓
modificar objeto existente




DELETE
↓
eliminar objeto existente

Y cada operación utiliza diferentes métodos SQLAlchemy:

CREATE
→ add()


UPDATE
→ modificar atributo


DELETE
→ delete()

En las operaciones de escritura:

CREATE
→ commit()


UPDATE
→ commit()


DELETE
→ commit()
29. Problemas y correcciones

Durante el desarrollo de DELETE aparecieron varios intentos incorrectos.

ClinicDelete innecesario

Se intentó crear:

class ClinicDelete(BaseModel):
    name: str

Se descartó porque DELETE solamente necesita el identificador del recurso.

name innecesario

Se intentó utilizar:

name: str

en delete_clinic().

Se eliminó porque el nombre no interviene en la eliminación.

refresh() innecesario

Se intentó:

db.refresh(clinic)

después de eliminar.

Se descartó porque el objeto ya fue eliminado mediante la transacción.

None vs bool

Inicialmente se utilizó:

return None

a pesar de declarar:

-> bool

Se corrigió a:

return False

para mantener la coherencia del tipo de retorno.

30. Código incorporado

Se modificó:

backend/app/routes/clinic.py

para incorporar:

DELETE /clinics/{clinic_id}

Se modificó:

backend/app/services/clinic_service.py

para incorporar:

delete_clinic()

No fue necesario modificar:

database.py

ni:

models/clinic.py
31. Estado del CRUD de Clinic

Al finalizar el bloque:

CREATE
✅ POST /clinics/


READ
✅ GET /clinics/
✅ GET /clinics/{clinic_id}


UPDATE
✅ PUT /clinics/{clinic_id}


DELETE
✅ DELETE /clinics/{clinic_id}

El CRUD básico de Clinic está completo.

32. Estado del bloque

Estado: COMPLETADO

Completado
Concepto de DELETE.
Diferencia entre CREATE, UPDATE y DELETE.
db.delete().
commit().
rollback().
Eliminación de un objeto existente.
True / False desde el service.
DELETE /clinics/{clinic_id}.
204 No Content.
404 Not Found.
OpenAPI.
Swagger.
Verificación directa en PostgreSQL.
Eliminación real del registro.
Manejo de recurso inexistente.
CRUD básico completo de Clinic.
Pendiente
Validaciones de negocio.
Manejo más específico de errores de base de datos.
CRUD de otras entidades.
Relaciones entre entidades.
Autenticación y autorización.
Multi-tenancy.
Auditoría.
Funcionalidades específicas del sistema médico.

Estas funcionalidades se desarrollarán progresivamente.

33. Próximo paso

El siguiente paso ya no será agregar otra operación al CRUD de Clinic.

Ahora que tenemos:

CREATE ✅
READ   ✅
UPDATE ✅
DELETE ✅

podemos utilizar Clinic como nuestro primer patrón CRUD completo.

El siguiente recurso dependerá de la planificación del sistema, pero entre las entidades principales estarán:

Patient
Professional
Appointment
MedicalRecord
Prescription
Inventory
Provider
Financial records
Users

Antes de multiplicar los CRUDs, será importante revisar si necesitamos mejorar el patrón que acabamos de construir para evitar repetir código innecesariamente.

34. Git y GitHub

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

La documentación de este bloque debe mantenerse en un archivo independiente:

docs/technical-journal/2026-08-15-clinic-delete-endpoint.md

Esto permite mantener un historial separado para cada bloque y evita modificar documentación de bloques anteriores ya cerrados.

35. Estado general del proyecto
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
✅ DELETE /clinics/{clinic_id}


Schemas
✅ ClinicCreate
✅ ClinicResponse
✅ ClinicUpdate


CRUD de Clinic
✅ Create
✅ Read — lista
✅ Read — por id
✅ Update
✅ Delete


Documentación
✅ Bloque 1
✅ Bloque 2
✅ Bloque 3
✅ Bloque 4
✅ Bloque 5


Próximo
⏳ Selección del siguiente recurso y evolución del patrón CRUD
36. Metodología mantenida

Este bloque siguió la metodología acordada:

Concepto
    ↓
Explicación sencilla
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

Un punto especialmente importante fue que la implementación de delete_clinic() fue inicialmente intentada de forma independiente y posteriormente corregida a partir del razonamiento sobre las diferencias entre CREATE, UPDATE y DELETE.