También se incorporó la consulta de una clínica específica mediante:

GET /clinics/{clinic_id}

y el manejo correcto del caso en el que la clínica no existe mediante:

HTTP 404 Not Found
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
Servicio create_clinic().
ClinicCreate.
ClinicResponse.
Router de Clinic.
Endpoint POST /clinics/.

La base de datos tenía registros de prueba conservados:

1 → Clínica Central
2 → Clínica del Oeste
3 → Clínica del Norte
5 → Clínica del Sur
7 → Clinica especial del Oeste
3. Concepto de GET

Se aprendió que GET se utiliza para consultar información.

Comparación con el endpoint anterior:

POST /clinics/
↓
crear una clínica




GET /clinics/
↓
consultar clínicas

La idea mental utilizada fue:

POST
↓
crear


GET
↓
consultar
4. Nuevo servicio: get_clinics()

Se amplió:

backend/app/services/clinic_service.py

con:

from sqlalchemy import select
from sqlalchemy.orm import Session


from app.models.clinic import Clinic




def create_clinic(db: Session, name: str) -> Clinic:
    clinic = Clinic(
        name=name
    )


    try:
        db.add(clinic)
        db.commit()
        db.refresh(clinic)


        return clinic


    except Exception:
        db.rollback()
        raise




def get_clinics(db: Session) -> list[Clinic]:
    statement = select(Clinic)


    result = db.execute(statement)


    clinics = result.scalars().all()


    return clinics

La función:

get_clinics(db: Session) -> list[Clinic]

recibe una Session y devuelve una lista de objetos Clinic.

5. Reutilización de select()

Se reutilizó el concepto aprendido anteriormente:

statement = select(Clinic)

Interpretación:

Consultar los registros representados por el modelo Clinic.

Conceptualmente:

select(Clinic)
   ↓
consultar clinics
6. Reutilización de execute()

Se utilizó:

result = db.execute(statement)

Interpretación:

Ejecutar la consulta mediante la Session.

El recorrido es:

statement
   ↓
db.execute()
   ↓
resultado de la consulta
7. Reutilización de scalars().all()

Se utilizó:

clinics = result.scalars().all()

Se reforzó la diferencia entre ambas partes:

scalars()
↓
obtener los objetos Clinic




all()
↓
obtener todos los resultados

Por lo tanto:

PostgreSQL
   ↓
SELECT
   ↓
SQLAlchemy
   ↓
Clinic
Clinic
Clinic

El resultado es una lista de objetos Clinic.

8. Nuevo endpoint GET /clinics/

Se incorporó al router:

backend/app/routes/clinic.py

el endpoint:

@router.get("/", response_model=list[ClinicResponse])
def get_clinics_endpoint(
    db: Session = Depends(get_db),
):
    clinics = get_clinics(db)


    return clinics

La separación de responsabilidades queda:

Router
↓
recibe la petición


Service
↓
realiza la consulta


SQLAlchemy
↓
trabaja con PostgreSQL


ClinicResponse
↓
define la respuesta de la API
9. response_model=list[ClinicResponse]

Se aprendió por qué el endpoint utiliza:

response_model=list[ClinicResponse]

En el endpoint de creación utilizábamos:

response_model=ClinicResponse

porque devolvíamos una sola clínica.

Ahora:

ClinicResponse
↓
una clínica


list[ClinicResponse]
↓
una lista de clínicas

Ejemplo de respuesta:

[
  {
    "id": 1,
    "name": "Clínica Central"
  },
  {
    "id": 2,
    "name": "Clínica del Oeste"
  }
]
10. Primera prueba de GET /clinics/

La ruta fue comprobada mediante OpenAPI.

La aplicación reconoció:

GET /clinics/
POST /clinics/

Se probó el endpoint real desde Swagger:

http://127.0.0.1:8000/docs

Resultado:

HTTP 200

Response body:

[
  {
    "id": 1,
    "name": "Clínica Central"
  },
  {
    "id": 2,
    "name": "Clínica del Oeste"
  },
  {
    "id": 3,
    "name": "Clínica del Norte"
  },
  {
    "id": 5,
    "name": "Clínica del Sur"
  },
  {
    "id": 7,
    "name": "Clinica especial del Oeste"
  }
]

Esto confirmó que:

GET /clinics/
   ↓
Session
   ↓
SELECT
   ↓
PostgreSQL
   ↓
lista de Clinic
   ↓
ClinicResponse
   ↓
JSON
11. Caso de lista vacía

Se analizó qué ocurriría si PostgreSQL no tuviera registros.

Con:

clinics = result.scalars().all()

el resultado sería:

[]

No sería:

None

ni un error.

La interpretación es:

Hay registros
↓
[Clinic, Clinic, ...]


No hay registros
↓
[]

Una lista vacía es una respuesta válida para:

GET /clinics/
12. Consulta por identificador

Se incorporó una segunda operación de lectura:

GET /clinics/{clinic_id}

Ejemplo:

GET /clinics/3

Se aprendió que:

{clinic_id}

representa un parámetro de ruta.

FastAPI recibe el valor directamente en la función:

def get_clinic_endpoint(
    clinic_id: int,
    db: Session = Depends(get_db),
):

Por ejemplo:

GET /clinics/3
↓
clinic_id = 3

El valor viene de la URL y int indica que esperamos un número entero.

13. Nuevo servicio: get_clinic()

Se agregó:

def get_clinic(db: Session, clinic_id: int) -> Clinic | None:
    statement = select(Clinic).where(Clinic.id == clinic_id)


    result = db.execute(statement)


    clinic = result.scalar_one_or_none()


    return clinic

Se reutilizó la consulta aprendida anteriormente:

select(Clinic).where(Clinic.id == 1)

pero ahora el valor es dinámico:

select(Clinic).where(Clinic.id == clinic_id)
14. Clinic | None

Se aprendió que:

Clinic | None

significa que la función puede devolver:

Clinic

o:

None

Esto es necesario porque una clínica puede existir o no existir.

Ejemplo:

GET /clinics/3
↓
Clinic

mientras:

GET /clinics/999
↓
None
15. scalar_one_or_none()

Se reforzó el concepto:

clinic = result.scalar_one_or_none()

Interpretación:

0 registros
↓
None


1 registro
↓
Clinic


más de 1 registro
↓
error

Es apropiado cuando buscamos como máximo un registro, especialmente por una clave primaria.

Comparación:

scalars().all()
↓
muchos / lista vacía




scalar_one_or_none()
↓
uno / None
16. Nuevo endpoint GET /clinics/{clinic_id}

Se incorporó:

@router.get(
    "/{clinic_id}",
    response_model=ClinicResponse,
    responses={
        404: {
            "description": "No se encontró la clínica solicitada",
        }
    },
)
def get_clinic_endpoint(
    clinic_id: int,
    db: Session = Depends(get_db),
):
    clinic = get_clinic(
        db=db,
        clinic_id=clinic_id,
    )


    if clinic is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró la clínica solicitada",
        )


    return clinic
17. Problema real descubierto: ResponseValidationError

Durante una prueba con una clínica inexistente:

GET /clinics/999

el service devolvió:

None

pero el endpoint tenía:

response_model=ClinicResponse

Por lo tanto FastAPI intentó convertir:

None
↓
ClinicResponse

y produjo:

ResponseValidationError

El error indicaba que la respuesta no era un objeto válido del cual extraer los atributos esperados.

Este problema fue útil para comprender que:

Service
↓
puede devolver None




Endpoint
↓
debe decidir cómo comunicar ese caso mediante HTTP
18. Solución: HTTPException

Se agregó:

from fastapi import APIRouter, Depends, HTTPException

y:

if clinic is None:
    raise HTTPException(
        status_code=404,
        detail="No se encontró la clínica solicitada",
    )

Esto transformó el comportamiento.

Clínica existente
GET /clinics/3
↓
200 OK

Respuesta:

{
  "id": 3,
  "name": "Clínica del Norte"
}
Clínica inexistente
GET /clinics/999
↓
404 Not Found

Respuesta:

{
  "detail": "No se encontró la clínica solicitada"
}
19. Diferencia entre validación y 404

Durante el bloque se reforzó la diferencia entre distintos errores HTTP.

422

Se utiliza cuando los datos recibidos no cumplen el schema.

Ejemplo:

{
  "name": 123
}

o:

{}

Flujo:

Request
↓
ClinicCreate
↓
validación
↓
422
404

Se utiliza cuando el recurso solicitado no existe.

Ejemplo:

GET /clinics/999

Flujo:

Request
↓
consulta
↓
None
↓
HTTPException
↓
404

Estas situaciones no representan una transacción de escritura fallida y no requieren rollback().

20. Documentación del 404 en OpenAPI

Inicialmente Swagger mostró:

404 Undocumented

aunque la API ya devolvía correctamente el 404.

Se entendió la diferencia entre:

funcionamiento
≠
documentación

Para documentar el resultado se utilizó:

responses={
    404: {
        "description": "No se encontró la clínica solicitada",
    }
}

Posteriormente OpenAPI mostró:

200 → Successful Response
404 → No se encontró la clínica solicitada
422 → Validation Error

La respuesta real continúa siendo:

raise HTTPException(
    status_code=404,
    detail="No se encontró la clínica solicitada",
)
21. Problema de inspección interna de FastAPI

Durante las comprobaciones se utilizó:

app.routes

y se intentó asumir que todos sus elementos tenían:

route.path
route.methods

FastAPI 0.141.1 también utiliza objetos internos como:

_IncludedRouter

que no exponen esos atributos directamente.

Se intentó posteriormente acceder a:

included.routes

pero tampoco es una API pública utilizable de esa forma.

Solución

Para comprobar las rutas efectivamente expuestas se utilizó OpenAPI:

app.openapi()["paths"]

Resultado:

['/clinics/', '/']

y posteriormente:

app.openapi()['paths']['/clinics/{clinic_id}']

confirmó la existencia del endpoint.

Se aprendió que es preferible utilizar mecanismos públicos de FastAPI como OpenAPI y pruebas HTTP en lugar de depender de estructuras internas.

22. OpenAPI verificó el parámetro de ruta

Se comprobó que FastAPI documenta:

clinic_id

como:

in: path
required: True
type: integer

Interpretación:

clinic_id
↓
nombre del parámetro


path
↓
viene de la URL


required
↓
es obligatorio


integer
↓
debe ser entero
23. Código permanente incorporado

Se modificó:

backend/app/routes/clinic.py

para incluir:

GET /clinics/
GET /clinics/{clinic_id}

Se modificó:

backend/app/services/clinic_service.py

para incluir:

get_clinics()
get_clinic()

El modelo Clinic, SessionLocal, get_db() y el resto de la infraestructura no fueron modificados.

24. Pruebas realizadas

Se verificó:

✅ GET /clinics/
✅ GET /clinics/3
✅ GET /clinics/999
✅ consulta de lista
✅ lista vacía como caso válido
✅ consulta por id
✅ parámetro de ruta
✅ validación de integer
✅ HTTP 200
✅ HTTP 404
✅ HTTP 422
✅ OpenAPI
✅ documentación del 404
✅ Swagger
✅ lectura desde PostgreSQL
25. Código conceptual del bloque
Obtener todas
def get_clinics(db: Session) -> list[Clinic]:
    statement = select(Clinic)


    result = db.execute(statement)


    clinics = result.scalars().all()


    return clinics
Obtener una
def get_clinic(db: Session, clinic_id: int) -> Clinic | None:
    statement = select(Clinic).where(Clinic.id == clinic_id)


    result = db.execute(statement)


    clinic = result.scalar_one_or_none()


    return clinic
26. Diferencia entre las dos consultas
get_clinics()
↓
select(Clinic)
↓
todos
↓
list[Clinic]

Mientras:

get_clinic()
↓
select(Clinic).where(Clinic.id == clinic_id)
↓
uno o ninguno
↓
Clinic | None

Esta diferencia debe quedar clara antes de avanzar.

27. Resultado del bloque

El sistema ahora cuenta con tres operaciones sobre Clinic:

POST /clinics/
↓
crear




GET /clinics/
↓
obtener todas




GET /clinics/{clinic_id}
↓
obtener una

El flujo actual de lectura es:

Cliente
   ↓
GET
   ↓
FastAPI
   ↓
Router
   ↓
Session
   ↓
Service
   ↓
SQLAlchemy
   ↓
PostgreSQL
   ↓
Clinic / lista de Clinic
   ↓
Response Schema
   ↓
JSON
28. Estado del bloque

Estado: COMPLETADO

Completado
GET /clinics/.
GET /clinics/{clinic_id}.
Consulta con select().
Filtrado con where().
Ejecución con execute().
Obtención de múltiples objetos con scalars().all().
Obtención de uno o ninguno con scalar_one_or_none().
Parámetro de ruta.
Clinic | None.
HTTPException.
404 Not Found.
Documentación del 404 en OpenAPI.
Pruebas desde Swagger.
Verificación de respuestas 200, 404 y 422.
Pendiente
Actualización de clínicas.
Eliminación de clínicas.
Validaciones de negocio.
Manejo más específico de errores de base de datos.
Evolución futura hacia CRUD completo.

No se incorporan todavía para mantener el desarrollo progresivo.

29. Próximo bloque

El siguiente paso será continuar con la parte de escritura del CRUD:

UPDATE

Antes de implementarlo se estudiará:

qué significa UPDATE;
cómo modificar un objeto SQLAlchemy;
qué diferencia existe entre modificar un objeto y persistir el cambio;
cuándo utilizar commit();
cómo manejar el caso de una clínica inexistente.

El objetivo será construir progresivamente algo equivalente a:

PUT /clinics/{clinic_id}

o el método HTTP que decidamos utilizar después de entender el concepto.

30. Git y documentación

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

La documentación de este bloque se mantiene separada del documento del Bloque 2 para conservar un historial independiente y evitar modificar documentación histórica ya cerrada.

31. Estado general del proyecto
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


Schemas
✅ ClinicCreate
✅ ClinicResponse


CRUD
✅ Create
✅ Read — lista
✅ Read — por id
⏳ Update
⏳ Delete


Documentación
✅ Bloque 1
✅ Bloque 2
✅ Bloque 3


Próximo
⏳ Update de Clinic
32. Metodología mantenida

Este bloque siguió exactamente la metodología acordada:

Concepto
    ↓
Explicación sencilla
    ↓
Ejemplo
    ↓
Aplicación al proyecto
    ↓
Prueba
    ↓
Comprensión
    ↓
Código definitivo
    ↓
Documentación
    ↓
Git/GitHub
    ↓
Siguiente bloque