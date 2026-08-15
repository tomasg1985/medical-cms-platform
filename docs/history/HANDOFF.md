# HANDOFF — Medical CMS Platform

**Proyecto:** Medical CMS Platform
**Estado:** Desarrollo activo
**Rama actual:** `develop`
**Última actualización:** 2026-08-13
**Último commit:** `bd03f`
**Mensaje del commit:** `feat: add clinic model and database initialization`

---

# 1. Propósito de este documento

Este documento funciona como punto de continuidad del proyecto.

Su objetivo es permitir retomar el desarrollo en una nueva conversación sin perder:

- contexto técnico;
- decisiones tomadas;
- estructura actual;
- avances realizados;
- problemas solucionados;
- conceptos aprendidos;
- metodología de trabajo;
- próximos pasos.

La prioridad no es solamente construir el sistema, sino utilizar el proyecto como medio para aprender desarrollo backend de forma progresiva y adquirir independencia al programar.

---

# 2. Proyecto

## Nombre

```text
Medical CMS Platform

Descripción

Plataforma SaaS orientada a la gestión integral de clínicas, consultorios y profesionales de la salud.

El sistema está pensado para permitir la administración de diferentes áreas de una organización médica desde una plataforma centralizada.

3. Objetivo general

Construir una plataforma backend profesional utilizando:

Descripción

Plataforma SaaS orientada a la gestión integral de clínicas, consultorios y profesionales de la salud.

El sistema está pensado para permitir la administración de diferentes áreas de una organización médica desde una plataforma centralizada.

3. Objetivo general

Construir una plataforma backend profesional utilizando:

El desarrollo se realiza de forma progresiva, priorizando primero una base sólida antes de agregar funcionalidades complejas.

4. Stack tecnológico actual
Backend
Python
FastAPI
SQLAlchemy 2.0
Psycopg 3
Base de datos
PostgreSQL 17
Infraestructura
Docker
Docker Compose
Frontend

Actualmente se mantiene separado del backend.

Tecnologías previstas:

HTML5
CSS3
JavaScript
5. Entorno de desarrollo

Sistema operativo:

Windows 11

Editor:

Visual Studio Code

Entorno virtual:

.venv

El entorno virtual se encuentra dentro del repositorio.

Los comandos Python se ejecutan normalmente con el entorno virtual activado.

Ejemplo:

(.venv) PS H:\...\medical-cms-platform>
6. Repositorio Git

Repositorio:

medical-cms-platform

Rama principal de trabajo:

develop

Rama estable:

main

La estrategia actual es desarrollar en:

develop

y posteriormente integrar los cambios en:

main
7. Estado de Git

Último commit:

bd03f

Mensaje:

feat: add clinic model and database initialization

El commit contiene:

configuración de SQLAlchemy;
inicialización de base de datos;
primer modelo Clinic;
registro de modelos;
documentación del bloque;
eliminación de archivos de documentación vacíos.

Antes de continuar, verificar siempre:

git status

El estado esperado después del push es:

nothing to commit, working tree clean
8. Docker y PostgreSQL

PostgreSQL se ejecuta mediante Docker Compose.

La imagen utilizada es:

postgres:17

El contenedor actual es:

medical-cms-platform-postgres-1

El puerto publicado es:

5432:5432

La base de datos utilizada por la aplicación es:

medical_cms
9. Verificación de PostgreSQL

Para iniciar el entorno:

docker compose up -d

Para comprobar el estado:

docker compose ps

El contenedor debe aparecer como:

Up

Ejemplo:

medical-cms-platform-postgres-1
postgres:17
Up
0.0.0.0:5432->5432/tcp
10. Configuración de SQLAlchemy

El archivo principal de conexión es:

backend/app/database.py

Actualmente contiene una estructura equivalente a:

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


from app.config.settings import settings




DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}"
    f"/{settings.db_name}"
)




engine = create_engine(DATABASE_URL)




class Base(DeclarativeBase):
    pass




SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Además existe la dependencia:

def get_db():
    db = SessionLocal()


    try:
        yield db
    finally:
        db.close()
11. Concepto de engine

engine representa la conexión/configuración que SQLAlchemy utiliza para comunicarse con PostgreSQL.

Se comprobó:

python -c "from app.database import engine; print(engine)"

Resultado:

Engine(postgresql+psycopg://postgres:***@localhost:5432/medical_cms)

Esto confirmó que SQLAlchemy está utilizando:

PostgreSQL
+
Psycopg
+
medical_cms
12. Verificación de conexión

Se ejecutó una consulta sencilla:

python -c "from app.database import engine; from sqlalchemy import text; connection = engine.connect(); print(connection.execute(text('SELECT 1')).scalar()); connection.close()"

Resultado:

1

Esto confirmó que:

FastAPI/Python
       ↓
SQLAlchemy
       ↓
Psycopg
       ↓
PostgreSQL

pueden comunicarse correctamente.

13. Concepto de Session

Se configuró:

SessionLocal = sessionmaker(...)

Una instancia:

db = SessionLocal()

produce:

<class 'sqlalchemy.orm.session.Session'>

La Session será utilizada para trabajar con los datos.

Conceptualmente:

Session
   ↓
prepara y gestiona operaciones
   ↓
SQLAlchemy
   ↓
PostgreSQL

Todavía estamos comenzando a trabajar con este concepto.

14. Concepto de get_db()

La dependencia actual es:

def get_db():
    db = SessionLocal()


    try:
        yield db
    finally:
        db.close()

yield se utiliza aquí para entregar temporalmente la sesión al código que la necesita.

Después de terminar el uso de la sesión:

finally:
    db.close()

la sesión se cierra.

Conceptualmente:

Crear Session
     ↓
Entregar Session
     ↓
Utilizar Session
     ↓
Cerrar Session
15. FastAPI

El punto de entrada principal es:

backend/app/main.py

La aplicación se crea mediante:

app = FastAPI(
    title=settings.app_name,
    description="API principal para gestión de clínicas y consultorios médicos",
    version=settings.app_version,
    debug=settings.debug,
)

Actualmente existe un endpoint inicial:

@app.get("/")
def root():
    return {
        "message": "✅ Medical CMS API funcionando correctamente",
        "status": "🟢 Online",
    }

También se verificó que la aplicación puede cargarse:

python -c "from app.main import app; print(app)"

Resultado:

<fastapi.applications.FastAPI object ...>
16. Servidor FastAPI

Para iniciar el servidor:

uvicorn app.main:app --reload

Resultado esperado:

Uvicorn running on http://127.0.0.1:8000
Application startup complete.

La ruta:

GET /

responde correctamente con:

{
    "message": "✅ Medical CMS API funcionando correctamente",
    "status": "🟢 Online"
}
17. Primer modelo SQLAlchemy

Se creó:

backend/app/models/clinic.py

Contenido actual:

from sqlalchemy.orm import Mapped, mapped_column


from app.database import Base




class Clinic(Base):
    __tablename__ = "clinics"


    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
18. Concepto de Clinic

Clinic es una clase Python que representa una entidad del sistema.

Conceptualmente:

Clinic
   ↓
modelo Python
   ↓
SQLAlchemy
   ↓
tabla clinics

La clase hereda de:

Base

para que SQLAlchemy pueda reconocerla como modelo.

19. __tablename__

Se definió:

__tablename__ = "clinics"

Esto indica el nombre de la tabla en PostgreSQL.

Por lo tanto:

Python:
Clinic


PostgreSQL:
clinics
20. Mapped

Se está utilizando la sintaxis moderna de SQLAlchemy 2.0.

Ejemplo:

id: Mapped[int]

indica que el atributo:

id

forma parte del mapeo SQLAlchemy y utiliza un tipo:

int

Otro ejemplo:

name: Mapped[str]

indica:

name
↓
texto

Mapped pertenece a SQLAlchemy.

No es una comprensión de listas de Python.

Es una herramienta de tipado y mapeo proporcionada por SQLAlchemy.

21. mapped_column()

Se utiliza para configurar las columnas.

Ejemplo:

id: Mapped[int] = mapped_column(primary_key=True)

Conceptualmente:

Mapped
   ↓
qué tipo de dato representa


mapped_column()
   ↓
cómo se configura la columna
22. Primary Key

El campo:

id: Mapped[int] = mapped_column(primary_key=True)

define la clave primaria.

Su función es identificar de forma única cada registro.

Ejemplo:

id     name
--------------------
1      Clínica Norte
2      Clínica Sur
3      Clínica Central
23. nullable=False

La columna:

name: Mapped[str] = mapped_column(nullable=False)

indica que name no puede quedar vacío (NULL).

Ejemplo:

id     name
--------------------
1      Clínica Norte
2      Clínica Sur
3      NULL            ❌
24. unique=True

unique=True fue estudiado como una restricción que impide valores repetidos.

Ejemplo:

name: Mapped[str] = mapped_column(unique=True)

impediría:

Clínica Norte
Clínica Norte

No se aplicó actualmente a Clinic.name porque diferentes clínicas podrían tener el mismo nombre.

La decisión depende de las reglas reales del negocio.

25. Base.metadata

Los modelos registrados forman parte de:

Base.metadata

Se comprobó:

python -c "from app.database import Base; from app.models.clinic import Clinic; print(Base.metadata.tables.keys())"

Resultado:

dict_keys(['clinics'])

Esto demuestra que SQLAlchemy conoce la tabla:

clinics
26. Columnas registradas

Se comprobó:

python -c "from app.database import Base; from app.models.clinic import Clinic; table = Base.metadata.tables['clinics']; print(table.columns.keys())"

Resultado:

['id', 'name']

Por lo tanto SQLAlchemy reconoce:

clinics
├── id
└── name
27. Registro de modelos

Se creó:

backend/app/models/__init__.py

con:

from app.models.clinic import Clinic

Esto permite importar el modelo desde el paquete:

app.models

y ayuda a que el modelo sea cargado antes de ejecutar la creación de tablas.

28. Error de import circular

Durante la configuración apareció:

ImportError: cannot import name 'Clinic'
from partially initialized module 'app.models'
(most likely due to a circular import)

La causa fue utilizar:

from app.models import Clinic

dentro de:

app/models/__init__.py

Esto generaba un ciclo:

app.models
    ↓
models/__init__.py
    ↓
app.models
    ↓
models/__init__.py

La solución fue utilizar:

from app.models.clinic import Clinic

Esto eliminó el ciclo.

29. Inicialización de base de datos

Se creó:

backend/app/database_init.py

Contenido:

from app.database import Base, engine
from app.models import Clinic




Base.metadata.create_all(bind=engine)
30. Base.metadata.create_all()

Esta instrucción:

Base.metadata.create_all(bind=engine)

le indica a SQLAlchemy que cree las tablas conocidas por Base.metadata que todavía no existen en PostgreSQL.

Conceptualmente:

Modelos
   ↓
Base.metadata
   ↓
create_all()
   ↓
engine
   ↓
PostgreSQL
31. Creación de la tabla

Se ejecutó:

python -c "import app.database_init"

El comando terminó sin errores.

Posteriormente se comprobó:

python -c "from sqlalchemy import inspect; from app.database import engine; inspector = inspect(engine); print(inspector.get_table_names())"

Resultado:

['clinics']

Esto confirmó que la tabla existe realmente en PostgreSQL.

32. Estructura real de PostgreSQL

Se ejecutó:

python -c "from sqlalchemy import inspect; from app.database import engine; inspector = inspect(engine); print(inspector.get_columns('clinics'))"

Resultado:

[
    {
        'name': 'id',
        'type': INTEGER(),
        'nullable': False,
        'default': "nextval('clinics_id_seq'::regclass)",
        'autoincrement': True,
        'comment': None
    },
    {
        'name': 'name',
        'type': VARCHAR(),
        'nullable': False,
        'default': None,
        'autoincrement': False,
        'comment': None
    }
]

Esto confirma:

clinics
├── id
│   ├── INTEGER
│   ├── NOT NULL
│   ├── PRIMARY KEY
│   └── autoincrement
│
└── name
    ├── VARCHAR
    └── NOT NULL
33. Primer recorrido completo

Hasta este punto se consiguió completar el primer recorrido real:

Clase Python
     ↓
Modelo SQLAlchemy
     ↓
Base.metadata
     ↓
create_all()
     ↓
Engine
     ↓
PostgreSQL
     ↓
Tabla real

Esto es un hito importante del proyecto.

34. Estructura actual relevante

La estructura relevante del backend actualmente es:

backend/
└── app/
    ├── api/
    ├── config/
    ├── core/
    ├── database/
    ├── database.py
    ├── database_init.py
    ├── dependencies/
    ├── main.py
    ├── middleware/
    ├── models/
    │   ├── __init__.py
    │   └── clinic.py
    ├── repositories/
    ├── routes/
    ├── schemas/
    ├── security/
    ├── services/
    └── utils/

No todas estas carpetas están siendo utilizadas todavía.

Muchas forman parte de la arquitectura prevista para etapas posteriores.

35. Documentación

La documentación del proyecto se mantiene dentro de:

docs/

Estructura actual relevante:

docs/
├── architecture/
├── decisions/
├── history/
├── learning/
├── product/
├── project-management/
├── roadmap/
├── setup/
├── sprints/
├── technical-journal/
├── glossary.md
├── project-history.md
└── README.md
36. Diario técnico

El diario técnico se encuentra en:

docs/technical-journal/

Actualmente se mantiene:

development-log.md

Este archivo contiene información histórica inicial del proyecto.

También se creó:

2026-08-13-sqlalchemy-first-model.md

Este documento contiene la documentación completa del bloque del primer modelo SQLAlchemy.

Los archivos:

day-01.md
day-02.md

estaban vacíos y fueron eliminados.

37. Convención de documentación

A partir de ahora, cuando se documente un bloque:

Se identificará el archivo exacto.
Se entregará el contenido completo.
El contenido estará listo para copiar y guardar.
No se dividirá la documentación en múltiples archivos salvo que sea necesario.
Los documentos deben incluir:
contexto;
situación inicial;
cambios realizados;
conceptos aprendidos;
comandos utilizados;
resultados;
errores encontrados;
soluciones;
estado del bloque;
próximo paso.
38. Metodología de aprendizaje

El usuario se encuentra todavía en una etapa inicial de aprendizaje de programación.

Actualmente lleva aproximadamente cinco meses aprendiendo.

Por esta razón, las explicaciones deben ser:

sencillas;
progresivas;
claras;
con ejemplos concretos;
evitando asumir conocimientos que todavía no fueron explicados;
explicando primero el concepto y después la sintaxis;
mostrando para qué sirve cada elemento;
relacionando código con situaciones reales.
39. Objetivo de aprendizaje

El objetivo no es depender permanentemente de la IA para escribir código.

La meta es desarrollar progresivamente independencia.

El proyecto debe utilizarse como herramienta de aprendizaje.

La IA debe funcionar principalmente como:

Profesor
+
Mentor
+
Revisor
+
Guía

y no solamente como:

Generador automático de código
40. Forma recomendada de explicar código

Para cada concepto nuevo se debe intentar seguir este esquema:

1. ¿Qué es?
2. ¿Para qué sirve?
3. ¿Qué problema resuelve?
4. Sintaxis mínima.
5. Ejemplo sencillo.
6. Ejemplo aplicado al proyecto.
7. Qué ocurre internamente de forma conceptual.
8. Verificación.

Ejemplo:

Si aparece:

id: Mapped[int] = mapped_column(primary_key=True)

primero explicar:

id
↓
nombre del atributo


Mapped[int]
↓
SQLAlchemy sabe que es un valor entero


mapped_column()
↓
configuración de la columna


primary_key=True
↓
identifica de forma única cada registro

Después relacionarlo con PostgreSQL.

41. Evitar sobrecargar al usuario

No introducir demasiados conceptos nuevos simultáneamente.

Si aparece un concepto secundario que no es necesario para continuar, se puede registrar como:

Pendiente de profundizar

y continuar con el objetivo principal.

Ejemplo:

nextval()

fue observado en PostgreSQL, pero no se profundizó porque no era necesario todavía.

42. Uso de la consola

La consola se utiliza principalmente para:

verificar conceptos;
comprobar imports;
comprobar conexiones;
inspeccionar SQLAlchemy;
comprobar PostgreSQL;
validar cambios.

No se debe crear lógica permanente del sistema mediante comandos de consola.

Cuando una funcionalidad forma parte real del proyecto, debe implementarse en su archivo correspondiente.

43. Mejoras de salida de consola

Se planteó mejorar las salidas de consola para hacerlas más visuales.

Por ahora:

NO IMPLEMENTAR

La prioridad actual es comprender primero:

FastAPI;
SQLAlchemy;
sesiones;
modelos;
PostgreSQL;
persistencia.

Las mejoras de presentación de consola se pueden realizar posteriormente.

44. Manejo de errores

Se conversó sobre incorporar manejo de excepciones mediante:

try:
    ...
except:
    ...

Por ahora no se debe introducir manejo de errores complejo sin necesidad.

Primero se debe comprender correctamente:

qué operación hacemos
↓
qué puede fallar
↓
cómo funciona normalmente

Después se incorporarán estrategias de manejo de errores apropiadas.

45. Estado actual del modelo Clinic

Actualmente:

class Clinic(Base):
    __tablename__ = "clinics"


    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

Todavía no se agregaron:

dirección;
teléfono;
email;
ciudad;
país;
timestamps;
relaciones;
usuarios;
profesionales.

No agregar campos solamente por anticipación.

Primero comprender el flujo básico.

46. Próximo bloque

El siguiente paso recomendado es trabajar con Session.

Objetivo:

Crear el primer registro real.

Flujo:

Crear objeto Clinic
       ↓
Session
       ↓
add()
       ↓
commit()
       ↓
PostgreSQL
       ↓
Registro persistido

Posteriormente:

SELECT
   ↓
consultar registro
   ↓
mostrar resultado
47. Primer objetivo práctico siguiente

Crear algo conceptualmente equivalente a:

clinic = Clinic(
    name="Clínica Central"
)

Después:

db.add(clinic)

Luego:

db.commit()

Y finalmente consultar el registro.

No avanzar a relaciones entre modelos hasta comprender este ciclo.

48. Conceptos pendientes inmediatos

Antes de avanzar demasiado, deben quedar claros:

qué es una Session;
qué hace add();
qué hace commit();
qué hace refresh();
diferencia entre objeto Python y registro SQL;
qué significa INSERT;
cómo consultar registros;
qué hace SELECT;
cómo cerrar correctamente una sesión.
49. Arquitectura conceptual actual

El sistema se está construyendo con esta idea:

Frontend
    ↓
FastAPI
    ↓
Routes / API
    ↓
Services
    ↓
Repositories
    ↓
SQLAlchemy
    ↓
PostgreSQL

No todas las capas están implementadas todavía.

La arquitectura completa se construirá progresivamente.

50. Regla importante para el desarrollo

No introducir tecnologías nuevas sin consultarlo previamente.

El stack acordado actualmente es:

Python
FastAPI
SQLAlchemy 2.0
PostgreSQL
Docker
Docker Compose
HTML
CSS
JavaScript

Si aparece la necesidad de incorporar una nueva tecnología, primero se debe explicar:

qué problema resuelve;
por qué podría ser necesaria;
alternativas;
impacto en el proyecto.

Después se decide si se incorpora.

51. Git — flujo de trabajo

Antes de modificar:

git status

Después de trabajar:

git status

Comprobar problemas de formato:

git --no-pager diff --check

Antes del commit:

git --no-pager diff --cached --stat
git --no-pager diff --cached --check

Después:

git commit -m "tipo: descripción"

Y finalmente:

git push origin develop
52. Convención de commits

Actualmente se utiliza una convención similar a Conventional Commits.

Ejemplos:

feat: add clinic model
fix: resolve database connection issue
docs: update project documentation
refactor: reorganize database module

El último commit utilizó:

feat: add clinic model and database initialization
53. Último commit

Commit:

bd03f

Mensaje:

feat: add clinic model and database initialization

Incluyó:

backend/app/database.py
backend/app/database_init.py
backend/app/main.py
backend/app/models/__init__.py
backend/app/models/clinic.py
docs/technical-journal/2026-08-13-sqlalchemy-first-model.md
docs/technical-journal/day-01.md
docs/technical-journal/day-02.md

Los dos últimos fueron eliminados porque estaban vacíos.

Se conservó:

docs/technical-journal/development-log.md

porque contenía información histórica.

54. Estado funcional actual

Actualmente se ha comprobado:

Docker PostgreSQL
        ↓
Funcionando


SQLAlchemy
        ↓
Conectado


FastAPI
        ↓
Funcionando


Base
        ↓
Configurada


Clinic
        ↓
Modelo creado


Base.metadata
        ↓
Reconoce clinics


PostgreSQL
        ↓
Tabla clinics creada
55. Lo que todavía NO está implementado

Todavía no se ha desarrollado:

CRUD completo de clínicas;
endpoints de clínicas;
schemas Pydantic;
repositories;
services;
autenticación;
usuarios;
JWT;
permisos;
relaciones entre modelos;
migraciones con Alembic;
tests automatizados;
frontend funcional;
integración completa entre frontend y backend.

No implementar estas partes anticipadamente.

Se deben introducir progresivamente.

56. Próximo objetivo técnico

El siguiente objetivo inmediato es:

Persistencia de un registro Clinic

La sesión será el concepto central.

El recorrido será:

Clinic(...)
    ↓
Session.add()
    ↓
Session.commit()
    ↓
PostgreSQL
    ↓
SELECT
    ↓
Resultado

Este bloque debe utilizarse también para reforzar los conceptos de:

ORM
Session
INSERT
SELECT
commit
refresh
persistencia
57. Punto exacto para retomar

Cuando se retome el proyecto, comenzar desde:

Primer registro de Clinic mediante SQLAlchemy Session

No comenzar nuevamente desde Docker ni desde la creación del modelo.

Ya está comprobado:

PostgreSQL funcionando
SQLAlchemy conectado
Clinic creado
Tabla clinics creada
58. Comandos útiles para comprobar el estado
Git
git status
Docker
docker compose ps
Comprobar engine
python -c "from app.database import engine; print(engine)"
Comprobar Base
python -c "from app.database import Base; print(Base)"
Comprobar Clinic
python -c "from app.models.clinic import Clinic; print(Clinic)"
Comprobar tablas SQLAlchemy
python -c "from app.database import Base; from app.models.clinic import Clinic; print(Base.metadata.tables.keys())"
Comprobar PostgreSQL
python -c "from sqlalchemy import inspect; from app.database import engine; inspector = inspect(engine); print(inspector.get_table_names())"
59. Regla de continuidad

Al comenzar una nueva conversación:

Leer este archivo.
Revisar el estado de Git.
Revisar el último commit.
Confirmar que Docker/PostgreSQL continúa funcionando.
Retomar desde el apartado "Próximo objetivo técnico".
No repetir bloques ya completados salvo que exista una duda concreta.
60. Estado final del HANDOFF
Proyecto:
Medical CMS Platform


Rama:
develop


Último commit:
bd03f


Estado:
Primer modelo SQLAlchemy creado y persistido como tabla PostgreSQL.


Modelo:
Clinic


Tabla:
clinics


Base de datos:
medical_cms


PostgreSQL:
17


ORM:
SQLAlchemy 2.0


API:
FastAPI


Contenedores:
Docker Compose


Próximo bloque:
Persistencia del primer registro Clinic mediante Session.
61. Recordatorio de metodología

El proyecto debe continuar desarrollándose de forma:

Pequeño paso
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
Documentación
     ↓
Git
     ↓
Siguiente paso

La prioridad es que cada bloque deje dos resultados:

1. El proyecto avanza.
2. El desarrollador aprende.

El segundo objetivo es tan importante como el primero.


Este `HANDOFF.md` queda como **documento maestro de continuidad** para las próximas conversaciones.