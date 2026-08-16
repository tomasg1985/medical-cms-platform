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

---

# 62. ACTUALIZACIÓN DEL PROYECTO — CONTEXTO POSTERIOR AL HANDOFF ORIGINAL

**Fecha de actualización:** 2026-08-16

Esta sección se agrega al HANDOFF original y constituye la información más reciente del estado del proyecto.

IMPORTANTE:

El contenido anterior del HANDOFF NO debe modificarse.

Esta sección funciona como actualización posterior y debe considerarse prioritaria cuando exista información contradictoria con secciones históricas anteriores.

---

# 63. Metodología de desarrollo y aprendizaje — Regla permanente

La metodología original continúa vigente y NO debe modificarse.

La forma de trabajo debe mantenerse exactamente como se desarrolló durante los primeros bloques:

```text
Concepto
    ↓
Explicación sencilla
    ↓
Ejemplo
    ↓
Aplicación al proyecto
    ↓
Intento propio
    ↓
Corrección
    ↓
Prueba
    ↓
Verificación
    ↓
Documentación
    ↓
Git
    ↓
Siguiente bloque

El proyecto sigue teniendo dos objetivos simultáneos:

avanzar técnicamente el Medical CMS Platform;
desarrollar progresivamente la independencia del desarrollador.

La IA debe continuar funcionando principalmente como:

Profesor
+
Mentor
+
Revisor
+
Guía

y no solamente como:

Generador automático de código

El usuario debe intentar construir las partes nuevas por sí mismo siempre que el concepto ya haya sido explicado.

Cuando un intento propio contenga errores, primero se debe explicar:

qué está intentando hacer;
qué parte está correcta;
qué parte está incorrecta;
por qué está incorrecta;
cómo corregirla.

No entregar automáticamente código completo cuando sea más conveniente permitir un nuevo intento del usuario.

64. Regla nueva — Cambios de arquitectura, stack o tecnología

Se establece explícitamente:

No modificar tecnologías, lenguajes, arquitectura principal ni incorporar nuevas tecnologías sin autorización previa del usuario.

Actualmente NO se autoriza ningún cambio en el stack.

Stack actual confirmado:

Python
FastAPI
SQLAlchemy 2.0
Psycopg 3
PostgreSQL 17
Docker
Docker Compose
HTML5
CSS3
JavaScript

Si durante el desarrollo aparece una propuesta de mejora tecnológica:

explicar qué problema resuelve;
explicar ventajas;
explicar desventajas;
explicar alternativas;
explicar impacto sobre el proyecto existente;
esperar autorización del usuario;
recién después implementar.

La filosofía es:

MEJORAR
≠
REEMPLAZAR TODO

La evolución del sistema debe ser incremental.

65. Nueva visión estratégica del producto

La visión del proyecto evolucionó.

El objetivo ya no se limita a construir un CMS básico para una clínica.

La visión actual es:

Medical CMS Platform
↓
Plataforma SaaS médica
↓
Multi-tenant / Multi-centro
↓
Orientada al mercado argentino
↓
Profesionales médicos
Odontólogos
Ortodoncistas
Especialidades
Subespecialidades
Clínicas
Policonsultorios
Centros de diagnóstico
Hospitales / centros con internación como evolución futura

El sistema debe poder evolucionar hacia una plataforma centralizada capaz de manejar múltiples organizaciones y centros manteniendo aislamiento correcto de datos.

66. Posicionamiento estratégico

No se busca competir contra SAP Healthcare mediante cantidad absoluta de funcionalidades.

La estrategia es competir mediante:

Agilidad
+
Costo
+
Usabilidad
+
Implementación rápida
+
Adaptación al mercado argentino
+
Automatización
+
Interoperabilidad
+
Experiencia moderna

Mercado objetivo inicial recomendado:

Clínicas medianas
10–50 profesionales aproximadamente
Policonsultorios
Centros de diagnóstico
Redes de profesionales
Organizaciones médicas que necesitan crecer

No se debe intentar inicialmente competir directamente por funcionalidad empresarial contra:

SAP
Epic
grandes plataformas hospitalarias enterprise

La ventaja buscada es:

Software moderno
+
SaaS
+
Localización argentina
+
Menor complejidad
+
Menor costo de implementación
+
Automatización
+
UX moderna

La expresión:

"El SAP de las clínicas medianas"

puede utilizarse como referencia estratégica interna.

No se considera todavía un slogan comercial definitivo.

67. Diferenciadores futuros identificados

La investigación de mercado permitió identificar los siguientes posibles diferenciadores.

No todos deben implementarse inmediatamente.

Se mantienen como roadmap estratégico.

Multi-tenant / Multi-centro
        ↓
Inventario inteligente
        ↓
Scraping / integración de medicamentos
        ↓
Receta electrónica
        ↓
Historia clínica asistida por IA
        ↓
WhatsApp / Omnicanalidad
        ↓
Telemedicina
        ↓
Auditoría médica
        ↓
Camas y quirófanos
        ↓
Nomenclador de prestaciones
        ↓
Portal paciente
        ↓
Facturación
        ↓
Auditoría y seguridad avanzada
68. Multi-tenant y Multi-centro

La arquitectura debe evolucionar pensando desde el principio en múltiples organizaciones.

Conceptualmente:

Tenant / Organización
        ↓
Clínicas / Centros
        ↓
Profesionales
        ↓
Pacientes
        ↓
Turnos
        ↓
Historias clínicas
        ↓
Recetas
        ↓
Facturación

Una organización puede tener múltiples centros.

Ejemplo:

Organización Médica Central
    ├── Centro Palermo
    ├── Centro Belgrano
    ├── Centro Caballito
    └── Centro Norte

El objetivo es evitar construir el sistema suponiendo que una instalación equivale a una única clínica.

69. Estrategia de aislamiento de tenants

Se investigó como alternativa utilizar:

Una base de datos PostgreSQL
        ↓
múltiples schemas
        ↓
un schema por tenant / clínica

Ejemplo conceptual:

public
clinica_central
clinica_oeste
clinica_norte

También se investigó el uso de:

SET search_path TO ...

como mecanismo para seleccionar el schema de trabajo.

IMPORTANTE:

Esto NO está aprobado como arquitectura definitiva.

No debe implementarse todavía.

search_path por sí solo no debe considerarse una garantía completa de aislamiento de seguridad.

Antes de adoptar este enfoque será necesario comparar:

Schemas por tenant
vs.
tenant_id en tablas
vs.
Row Level Security
vs.
Arquitectura híbrida

La decisión debe realizarse posteriormente considerando:

seguridad;
complejidad;
migraciones;
rendimiento;
mantenimiento;
backup;
escalabilidad;
recuperación;
aislamiento.
70. Escalabilidad PostgreSQL

Se investigaron buenas prácticas para evitar que una base centralizada se convierta en un problema de rendimiento.

Se consideran especialmente:

Indexación inteligente
+
consultas optimizadas
+
UUIDs para determinadas entidades
+
almacenamiento externo de archivos

No significa que debamos aplicar todas estas decisiones inmediatamente.

Se deben introducir cuando el modelo correspondiente sea diseñado.

71. UUID — decisión futura

Se identificó como posible mejora utilizar UUID para entidades sensibles o que puedan exponerse mediante APIs.

Especialmente:

Patient
MedicalRecord
Prescription
Study
Document

Motivos:

evitar identificadores secuenciales predecibles;
facilitar determinadas integraciones;
facilitar migraciones/fusiones;
desacoplar identificadores internos del orden de creación.

IMPORTANTE:

No cambiar actualmente:

Clinic.id

No realizar una migración a UUID solamente por anticipación.

La decisión deberá evaluarse antes de crear las entidades sensibles correspondientes.

72. Archivos médicos y almacenamiento externo

Las historias clínicas pueden contener archivos grandes:

DICOM
PDF
Imágenes
Estudios
Fotos
Audio
Video

La dirección arquitectónica futura recomendada es:

PostgreSQL
↓
metadatos
+
referencia al archivo


Object Storage
↓
archivo físico

Posibles tecnologías futuras:

AWS S3
Google Cloud Storage
Azure Blob Storage
MinIO
Servidor propio

No se autoriza todavía ninguna tecnología de almacenamiento específica.

La decisión se tomará cuando aparezca la necesidad real del módulo de documentos/estudios.

73. Seguridad y datos médicos

La seguridad pasa a considerarse una característica transversal del sistema.

Las historias clínicas y datos de salud deben manejarse como información especialmente sensible.

Aspectos futuros prioritarios:

Autenticación
        ↓
Autorización
        ↓
Tenant
        ↓
Centro
        ↓
Profesional
        ↓
Paciente
        ↓
Historia clínica

También:

Auditoría
↓
quién
↓
qué hizo
↓
sobre qué dato
↓
cuándo

La Ley 25.326 establece reglas específicas para datos relativos a la salud y exige medidas técnicas y organizativas para preservar seguridad y confidencialidad. Esta normativa deberá considerarse desde el diseño de los módulos clínicos y de seguridad.

74. Auditoría médica

Se identificó como posible diferenciador de alto valor comercial.

Objetivo:

Prestación
    ↓
Código
    ↓
Obra social / Prepaga
    ↓
Reglas
    ↓
¿Requiere autorización?
    ↓
¿Falta documentación?
    ↓
¿Existe riesgo de débito?

La idea es que el sistema pueda detectar problemas antes de que la clínica facture una prestación que luego sea rechazada.

Este módulo se considera futuro.

No implementar todavía.

75. Scraping e inteligencia de inventario

El scraping deja de considerarse únicamente una función para obtener datos.

La visión futura es:

Fuentes externas
      ↓
Medicamentos
      ↓
Código / Troquel
      ↓
Precios
      ↓
Stock
      ↓
Alertas
      ↓
Gestión de inventario

Posibles fuentes y referencias a investigar posteriormente:

Vademécums
Manual Farmacéutico / Kairos
Alfabeta
Proveedores
Fuentes oficiales

IMPORTANTE:

No asumir que una fuente puede scrapearse legal o técnicamente sin restricciones.

Antes de implementar cada integración se deberá comprobar:

disponibilidad;
permisos;
términos de uso;
API oficial si existe;
frecuencia de actualización;
estructura de datos;
estabilidad;
legalidad de la extracción.
76. Obras sociales y prepagas

Se identificó una posible evolución del inventario y facturación:

Paciente
↓
Obra social / Prepaga
↓
Plan
↓
Medicamento / práctica / prestación
↓
Cobertura
↓
Autorización
↓
Facturación

El objetivo sería ayudar a reducir:

errores
+
débitos
+
prestaciones rechazadas

Esta área se considera uno de los posibles diferenciales comerciales del sistema en Argentina.

77. Receta electrónica

La receta electrónica pasa a formar parte de la visión futura del producto.

IMPORTANTE:

No implementar una solución propia suponiendo que basta con generar un PDF firmado.

La normativa argentina vigente establece que las plataformas de prescripción deben cumplir requisitos específicos y estar inscriptas/aprobadas por ReNaPDiS. Además, la Resolución 2214/2025 amplía el alcance de las prescripciones electrónicas a medicamentos, dispositivos, estudios, prácticas y procedimientos, y establece requisitos de interoperabilidad y conservación.

Por lo tanto, cuando llegue este módulo se deberá investigar:

ReNaPDiS
Normativa vigente
Interoperabilidad
CUIR
Repositorios
Prestadores
Farmacias
Plataformas habilitadas

La integración deberá diseñarse a partir de la normativa vigente en el momento de implementación.

78. Firma digital

Se incorporó como conocimiento futuro:

Ley 25.506
Firma electrónica
Firma digital
Certificados
Infraestructura de Firma Digital

La Ley 25.506 reconoce la firma electrónica y digital y establece la eficacia jurídica de la firma digital bajo las condiciones previstas legalmente.

La firma digital también proporciona mecanismos de presunción de autoría e integridad según el marco legal aplicable.

No implementar todavía.

Cuando llegue el módulo de recetas/documentos se deberá investigar:

certificadores licenciados;
certificados;
firma digital remota;
normativa vigente;
interoperabilidad;
requisitos de las plataformas sanitarias.
79. Historias clínicas + IA

Se identificó como posible diferenciador de alto valor.

Concepto:

Médico habla
    ↓
Audio
    ↓
Transcripción
    ↓
Estructuración
    ↓
Resumen
    ↓
Historia clínica

Posibles datos:

Motivo de consulta
Síntomas
Antecedentes
Observaciones
Diagnóstico
Plan
Indicaciones

IMPORTANTE:

La IA debe plantearse inicialmente como:

Asistente del profesional

y no como:

sustituto de decisión clínica

El profesional debe mantener el control sobre la información clínica final.

Se investigarán posteriormente:

LLMs locales
APIs
Speech-to-text
Procesamiento de lenguaje
Privacidad
Anonimización
Auditoría

No implementar todavía.

80. WhatsApp y omnicanalidad

Se identificó como posible diferenciador comercial importante.

Concepto futuro:

Turno
↓
Confirmación
↓
WhatsApp


Turno
↓
Recordatorio
↓
WhatsApp


Cancelación
↓
WhatsApp


Reagendamiento
↓
WhatsApp

También podrían incorporarse:

Email
SMS
Portal paciente

La integración debe evaluarse posteriormente mediante APIs oficiales y requisitos del proveedor correspondiente.

No incorporar ahora.

81. Telemedicina

Se identificó como módulo futuro.

Conceptualmente:

Turno
↓
Videollamada
↓
Historia clínica
↓
Consulta
↓
Registro
↓
Receta / indicaciones

Se mencionaron proveedores como:

Daily.co
Agora

pero ninguno está aprobado todavía como tecnología definitiva.

La selección futura deberá considerar:

seguridad;
privacidad;
estabilidad;
costos;
grabación;
almacenamiento;
integración con HCE;
requisitos legales;
experiencia de usuario.
82. Camas y quirófanos

Como posible evolución hacia clínicas con internación:

Camas
├── Disponible
├── Ocupada
├── Limpieza
└── Mantenimiento

Y:

Quirófanos
├── Disponible
├── Reservado
├── Preparación
└── Ocupado

La interfaz futura podría utilizar un tablero visual similar a Kanban.

No implementar todavía.

83. Nomenclador de prestaciones

Se identificó como posible módulo complementario al scraping de medicamentos.

Conceptualmente:

Práctica médica
↓
Código estándar
↓
Prestación
↓
Facturación

El objetivo sería evitar errores de carga y ayudar a la administración.

Antes de implementarlo habrá que identificar la fuente oficial/actualizada correspondiente y las reglas de uso.

No implementar todavía.

84. Portal del paciente

Módulo futuro:

Portal Paciente
├── Turnos
├── Recetas
├── Estudios
├── Documentos
└── Historial disponible

Objetivo:

reducir la dependencia de la atención administrativa por teléfono o canales manuales.

El portal deberá respetar:

Autenticación
Autorización
Privacidad
Tenant
Auditoría

No implementar todavía.

85. Facturación

Se identificó como módulo futuro:

Consulta
↓
Pago
↓
Facturación
↓
Comprobante

Se investigará posteriormente la integración vigente con los servicios de facturación electrónica de Argentina.

No fijar todavía:

librería
wrapper
API
proveedor

La selección debe realizarse al llegar al módulo y revisar la documentación oficial vigente.

86. Stack tecnológico — conclusión de la investigación

Después de analizar la nueva visión, NO se considera necesario cambiar el stack actual.

Stack confirmado:

Python
FastAPI
SQLAlchemy 2.0
Psycopg 3
PostgreSQL 17
Docker
Docker Compose
HTML
CSS
JavaScript

Ventajas para la evolución futura:

Python
→ IA
→ scraping
→ automatización
→ procesamiento


FastAPI
→ APIs
→ integraciones
→ servicios


SQLAlchemy
→ ORM
→ relaciones
→ consultas
→ PostgreSQL


PostgreSQL
→ datos relacionales
→ integridad
→ indexación
→ auditoría
→ multi-tenant


Docker
→ despliegue
→ aislamiento
→ servicios futuros

No se autoriza ningún cambio de stack actualmente.

87. GitHub — nuevo estado

El repositorio:

medical-cms-platform

ahora se encuentra:

PRIVATE

El único colaborador actualmente es el propietario del proyecto.

Esto se decidió porque el software se considera propietario y todavía se encuentra en desarrollo.

Flujo de trabajo:

Local
↓
develop
↓
commit
↓
push
↓
GitHub privado

No se modificó el flujo de Git.

IMPORTANTE:

Nunca subir al repositorio:

.env
Contraseñas
Tokens
API Keys
JWT secrets
Certificados privados
Claves privadas
Credenciales
Datos reales de pacientes
Historias clínicas reales
Recetas reales
Documentos médicos reales
88. Documentación de bloques completados

Durante las conversaciones posteriores al HANDOFF original se completaron y documentaron los siguientes bloques:

Bloque 2
POST /clinics/

Documento:

docs/technical-journal/2026-08-15-fastapi-first-clinic-endpoint.md
Bloque 3
GET /clinics/
GET /clinics/{clinic_id}

Documento:

docs/technical-journal/2026-08-15-clinic-read-endpoints.md
Bloque 4
PUT /clinics/{clinic_id}

Documento:

docs/technical-journal/2026-08-15-clinic-update-endpoint.md
Bloque 5
DELETE /clinics/{clinic_id}

Documento:

docs/technical-journal/2026-08-15-clinic-delete-endpoint.md

Los documentos se mantienen separados para conservar un historial independiente por bloque.

89. CRUD completo de Clinic

El sistema actualmente posee un CRUD funcional completo para Clinic.

CREATE
POST /clinics/
        ✅


READ
GET /clinics/
        ✅


READ ONE
GET /clinics/{clinic_id}
        ✅


UPDATE
PUT /clinics/{clinic_id}
        ✅


DELETE
DELETE /clinics/{clinic_id}
        ✅
90. Schemas actuales de Clinic

Actualmente deben existir:

ClinicCreate
ClinicUpdate
ClinicResponse

Conceptualmente:

ClinicCreate
↓
entrada para CREATE


ClinicUpdate
↓
entrada para UPDATE


ClinicResponse
↓
salida de API

No crear:

ClinicDelete

porque el DELETE actual no necesita request body.

91. Services actuales de Clinic

El service contiene actualmente:

create_clinic()
get_clinics()
get_clinic()
update_clinic()
delete_clinic()

La responsabilidad conceptual:

create_clinic()
→ crear


get_clinics()
→ obtener todos


get_clinic()
→ obtener uno


update_clinic()
→ actualizar uno


delete_clinic()
→ eliminar uno
92. Refactorización del Bloque 6

Se identificó duplicación en:

get_clinic()
update_clinic()
delete_clinic()

Antes update_clinic() y delete_clinic() repetían:

statement = select(Clinic).where(Clinic.id == clinic_id)
result = db.execute(statement)
clinic = result.scalar_one_or_none()

La refactorización fue:

get_clinic()
      ↑
      ├── GET
      ├── UPDATE
      └── DELETE

Ahora:

clinic = get_clinic(
    db=db,
    clinic_id=clinic_id,
)

se reutiliza desde update_clinic() y delete_clinic().

93. Resultado de la refactorización

La refactorización fue realizada sin introducir nuevas capas.

NO se incorporaron:

GenericRepository
BaseCRUD
BaseService
UnitOfWork
Repository Pattern genérico

La decisión fue mantener la arquitectura sencilla.

Razón:

la eliminación de duplicación conseguida ya aporta valor suficiente y las diferencias entre CREATE, UPDATE y DELETE todavía justifican mantener sus bloques de transacción separados.

94. Pruebas de regresión del Bloque 6

Después de la refactorización se comprobaron:

GET /clinics/3
        ✅


PUT /clinics/10
        ✅


PUT /clinics/10
        ✅


DELETE /clinics/11
        ✅

También se verificó directamente mediante SQLAlchemy que:

get_clinic(10)
→ Clinic encontrada

y:

get_clinics()
→ lista completa

No se detectó que el PUT generara un INSERT.

Durante las pruebas se observó un nuevo registro temporal y posteriormente se comprobó mediante los logs de Uvicorn que dicho registro había sido generado por:

POST /clinics/

y no por:

PUT /clinics/10

Esto confirmó que la refactorización no estaba generando registros adicionales accidentalmente.

95. Codificación UTF-8

Durante el Bloque 6 apareció repetidamente el problema:

No se encontrÃ³ la clÃnica solicitada

El problema correspondía a una representación incorrecta de caracteres.

Se corrigió el archivo:

backend/app/routes/clinic.py

y se verificó mediante Python:

MOJIBAKE: False
UTF8_CORRECTO: True

También se comprobó mediante OpenAPI que GET, PUT y DELETE reciben correctamente:

No se encontró la clínica solicitada

Regla futura:

Archivos del proyecto
↓
UTF-8

No utilizar escapes Unicode como solución normal para textos estáticos en español.

96. Saltos de línea Windows / Git

Durante la comprobación de Git apareció:

LF will be replaced by CRLF

Esto no representa un error funcional.

Es una advertencia relacionada con la normalización de finales de línea en Windows.

No se modificó todavía la configuración de Git ni se agregó .gitattributes.

Si este comportamiento comienza a generar problemas repetitivos en múltiples archivos, se podrá evaluar una política de finales de línea posteriormente.

No realizar cambios solamente por esta advertencia.

97. Estado de base de datos después de las pruebas

Estado conservado observado:

1 → Clínica Central
2 → Clínica del Oeste
3 → Clínica del Norte Premium
5 → Clínica del Sur
7 → Clinica especial del Oeste

Durante las pruebas del Bloque 6 se creó temporalmente:

10 → Clinica para prueba DELETE

Este registro quedó presente al momento de la última verificación.

IMPORTANTE:

Antes de comenzar a trabajar con nuevas entidades, revisar si el registro id = 10 sigue siendo un dato temporal.

No eliminarlo automáticamente sin verificar su estado.

98. Aprendizajes consolidados

Durante los bloques posteriores al HANDOFF original se consolidaron:

FastAPI
├── APIRouter
├── Depends
├── response_model
├── HTTPException
├── path parameters
├── OpenAPI
└── Swagger


Pydantic
├── BaseModel
├── validación de entrada
├── response schemas
└── ClinicCreate / ClinicUpdate / ClinicResponse


SQLAlchemy
├── Session
├── select()
├── where()
├── execute()
├── scalars()
├── all()
├── scalar_one_or_none()
├── add()
├── commit()
├── refresh()
├── delete()
└── rollback()


HTTP
├── POST
├── GET
├── PUT
├── DELETE
├── 200
├── 204
├── 404
└── 422
99. Conceptos HTTP aprendidos

Se consolidó:

POST
↓
crear


GET
↓
consultar


PUT
↓
actualizar


DELETE
↓
eliminar

Respuestas:

200
↓
operación exitosa con contenido


204
↓
operación exitosa sin contenido


404
↓
recurso inexistente


422
↓
datos recibidos inválidos
100. Diferencia entre Service y Endpoint

Se reforzó una separación importante.

El Service se encarga de lógica relacionada con datos:

Service
↓
Clinic / None
True / False

El Endpoint se encarga de traducir ese resultado a HTTP:

Clinic
↓
200


None
↓
404


True
↓
204


False
↓
404

Esto debe mantenerse en futuras entidades.

101. Primera experiencia de refactorización

El Bloque 6 introdujo una nueva etapa del aprendizaje:

Antes:
escribir código que funciona


Ahora:
escribir código que funciona
+
analizar si puede mantenerse mejor

Regla aprendida:

Refactorizar
≠
cambiar mucho código


Refactorizar
=
mejorar el código
manteniendo el comportamiento

No realizar abstracciones únicamente porque "se ven profesionales".

102. Regla para futuras refactorizaciones

Antes de introducir una abstracción:

Identificar una repetición real.
Confirmar que la repetición genera mantenimiento adicional.
Evaluar si la abstracción mantiene claridad.
Evaluar el beneficio.
Evitar sobre-arquitectura.
Probar que el comportamiento anterior sigue funcionando.
103. Estado actual de Clinic
Modelo
✅


Schema Create
✅


Schema Update
✅


Schema Response
✅


Service Create
✅


Service Read
✅


Service Update
✅


Service Delete
✅


Router Create
✅


Router Read
✅


Router Read One
✅


Router Update
✅


Router Delete
✅


Swagger
✅


OpenAPI
✅


PostgreSQL
✅
104. Estado del Bloque 6

Actualmente:

Bloque 6 — Refactorización

Estado:

Análisis
✅


Duplicación identificada
✅


Refactorización de get_clinic()
✅


update_clinic() reutiliza get_clinic()
✅


delete_clinic() reutiliza get_clinic()
✅


Pruebas GET
✅


Pruebas UPDATE
✅


Pruebas DELETE
✅


Verificación PostgreSQL
✅


Codificación UTF-8
✅


Revisión de diff
✅


Documentación
⏳


Commit
⏳


Push
⏳

El bloque se considera técnicamente terminado, pero todavía debe cerrarse formalmente mediante documentación y Git.

105. Próximo paso inmediato

Antes de crear Patient, completar:

Bloque 6
↓
documentación
↓
git add
↓
git diff --cached
↓
commit
↓
push

Después de cerrar Bloque 6:

Clinic CRUD
        ↓
patrón CRUD de referencia
        ↓
diseño de Patient
106. Próxima entidad — Patient

La siguiente entidad principal candidata es:

Patient

Pero NO comenzar directamente escribiendo el modelo.

Primero analizar:

¿Qué es Patient?
¿Qué datos necesita?
¿Qué datos son sensibles?
¿Qué identifica de forma única al paciente?
¿Qué pertenece al tenant?
¿Qué pertenece al centro?
¿Qué relaciones tendrá?
¿Qué identificadores deberá utilizar?

Se debe evaluar especialmente:

UUID
Tenant
Clinic / Center
DNI
Obra Social / Prepaga
Datos de contacto
Auditoría
Privacidad

No agregar campos anticipadamente sin definir primero el dominio.

107. Modelo conceptual futuro de Patient

No es implementación todavía.

Es solamente una referencia conceptual:

Tenant
   ↓
Clinic / Center
   ↓
Patient
   ├── Datos personales
   ├── Identificación
   ├── Contacto
   ├── Cobertura
   ├── Turnos
   ├── Historias clínicas
   ├── Recetas
   ├── Estudios
   └── Documentos

Las relaciones se definirán posteriormente.

108. Nueva regla para entidades médicas

Antes de crear entidades como:

Patient
MedicalRecord
Prescription
Study

se debe evaluar:

Seguridad
+
Privacidad
+
Auditoría
+
Tenant
+
Identificador
+
Relaciones

No empezar por el CRUD simplemente porque ya sabemos hacerlo.

Primero definir correctamente el modelo de negocio.

109. Diferencia entre CRUD de ejemplo y dominio real

Clinic fue utilizado como entidad de aprendizaje.

Su CRUD sirvió para aprender:

CREATE
READ
UPDATE
DELETE

Pero las entidades médicas futuras pueden tener reglas mucho más complejas.

Por ejemplo:

Patient
↓
no debería eliminarse físicamente de cualquier forma

y:

MedicalRecord
↓
requiere trazabilidad
↓
auditoría
↓
historial

Por lo tanto no asumir que todos los recursos del sistema tendrán exactamente el mismo comportamiento que Clinic.

110. Estrategia futura de CRUD

El CRUD aprendido con Clinic debe utilizarse como:

Patrón de aprendizaje
+
referencia

No como una plantilla que se copie ciegamente a todas las entidades.

Cada nueva entidad debe analizar:

¿CRUD simple?
¿CRUD con reglas?
¿Soft delete?
¿Auditoría?
¿Histórico?
¿Inmutabilidad?
¿Relaciones?
¿Permisos?
111. Repositorio GitHub

Estado actual:

medical-cms-platform
↓
PRIVATE

Rama:

develop

Rama estable:

main

El flujo continúa:

develop
↓
commit
↓
push
↓
GitHub privado

El repositorio es propiedad del usuario y no debe hacerse público sin decisión explícita.

112. Propiedad intelectual y exposición del código

El proyecto se considera software propietario.

Por esta razón:

Repositorio
→ privado


Código
→ no publicar sin autorización


Documentación técnica
→ privada


Secrets
→ nunca subir


Datos reales
→ nunca subir

No convertir el repositorio en público sin evaluar previamente:

propiedad intelectual;
licenciamiento;
código que se desea revelar;
documentación que se desea publicar;
dependencias;
secretos;
copias/forks existentes.
113. Nueva visión comercial

La propuesta de valor futura se basa en:

SaaS
+
Multi-tenant
+
Multi-centro
+
UX moderna
+
Mercado argentino
+
Automatización
+
WhatsApp
+
Receta electrónica
+
Inventario
+
Auditoría
+
HCE
+
IA
+
Facturación

Pero estas funcionalidades deben implementarse progresivamente.

No intentar construirlas todas al mismo tiempo.

114. Prioridad de producto

La prioridad sigue siendo:

1.
Base técnica sólida


2.
Modelo de dominio correcto


3.
Seguridad


4.
CRUDs y funcionalidades fundamentales


5.
Multi-tenant


6.
Integraciones


7.
Automatización


8.
IA


9.
Funcionalidades avanzadas


10.
Escalabilidad comercial

La prioridad exacta puede ajustarse mediante el roadmap.

115. Regla fundamental sobre nuevas tecnologías

No agregar:

React
Vue
Next.js
Redis
RabbitMQ
Kafka
Celery
MongoDB
Kubernetes
AWS
etc.

solamente porque puedan ser útiles en algún momento.

Cada tecnología futura deberá pasar por:

Problema
↓
Necesidad
↓
Alternativas
↓
Ventajas
↓
Desventajas
↓
Impacto
↓
Autorización
↓
Implementación

El stack actual permanece vigente.

116. Regla fundamental sobre funcionalidades futuras

Las funcionalidades futuras identificadas:

Scraping
IA
WhatsApp
Telemedicina
Receta electrónica
Facturación
Portal paciente
Auditoría
Camas
Quirófanos
Nomenclador

son:

ROADMAP

No son funcionalidades autorizadas para implementación inmediata.

Antes de implementarlas:

Analizar
↓
investigar
↓
explicar
↓
estimar impacto
↓
autorizar
↓
implementar
117. Arquitectura conceptual futura

La arquitectura objetivo continúa siendo una evolución de:

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

Con futuras integraciones:

FastAPI
   ├── WhatsApp
   ├── Receta electrónica
   ├── AFIP / servicios fiscales
   ├── Telemedicina
   ├── Fuentes de medicamentos
   ├── Nomencladores
   └── IA

Y:

PostgreSQL
   ↓
metadatos
   +
datos relacionales

mientras:

Object Storage
   ↓
documentos y archivos pesados

Esta arquitectura es una visión futura y no implica cambios inmediatos.

118. Principio de seguridad futura

Para una plataforma médica se deberá diseñar bajo el principio:

Seguridad desde el diseño

y no:

Seguridad al final

Aspectos futuros:

Password hashing
JWT / autenticación
RBAC
Tenant isolation
Auditoría
Logs
Cifrado
Gestión de secretos
Control de acceso
Backups
Recuperación
Trazabilidad

No implementar todo simultáneamente.

Se deben introducir progresivamente.

119. Regla sobre IA clínica

La IA debe plantearse inicialmente como:

Asistente

No como:

Autoridad clínica

Toda generación automática de contenido médico debe poder:

ser revisada
ser corregida
ser aceptada/rechazada
quedar auditada

El médico debe conservar el control sobre la información clínica final.

120. Regla sobre normativa argentina

Toda integración regulada deberá verificarse con documentación oficial vigente en el momento de implementación.

Especialmente:

Receta electrónica
Firma digital
AFIP / ARCA
SISA
Datos personales
Obras sociales
Facturación
Interoperabilidad sanitaria

No asumir que una investigación realizada hoy será válida indefinidamente.

La normativa debe revisarse nuevamente cuando el módulo vaya a implementarse.

121. Estado final actualizado para continuidad
PROJECT
update_clinic()
delete_clinic()
✅


REGRESSION TESTS
✅


UTF-8
✅


SECURITY STRATEGY
En diseño progresivo


MULTI-TENANT
Visión estratégica
No implementado todavía


PATIENT
Próxima entidad a analizar


NEXT
Cerrar Bloque 6
↓
Commit
↓
Push
↓
Diseñar Patient
122. Punto exacto para retomar en una nueva conversación

Al abrir una nueva conversación:

Leer el HANDOFF original completo.
Leer desde la sección 62 de este documento agregado.
No repetir los bloques 1–5.
Reconocer que Clinic posee CRUD completo.
Reconocer que el repositorio es privado.
Reconocer que el Bloque 6 está técnicamente terminado pero pendiente de cierre documental/Git.
Finalizar el cierre del Bloque 6.
Después comenzar el diseño de Patient.

El siguiente objetivo NO es comenzar inmediatamente a copiar el CRUD de Clinic.

Primero:

Patient
↓
analizar dominio
↓
identificar datos
↓
identificar relaciones
↓
identificar tenant
↓
identificar seguridad
↓
evaluar UUID
↓
crear modelo

Después se construirá progresivamente su CRUD.

123. Recordatorio final de metodología

Mantener siempre:

Pequeño paso
     ↓
Explicación
     ↓
Ejemplo
     ↓
Intento propio
     ↓
Corrección
     ↓
Aplicación
     ↓
Prueba
     ↓
Verificación
     ↓
Documentación
     ↓
Git
     ↓
Siguiente paso

No avanzar más rápido sacrificando comprensión.

No introducir tecnologías sin autorización.

No introducir arquitectura innecesaria.

No copiar patrones sin entenderlos.

No modificar bloques históricos ya documentados salvo que exista un error real que requiera corrección.

Cada bloque debe dejar:

Proyecto mejor
+
Desarrollador con más conocimiento
124. Regla definitiva de continuidad

Este HANDOFF actualizado mantiene como prioridad absoluta:

CONTINUIDAD
+
APRENDIZAJE
+
DESARROLLO PROGRESIVO
+
PROPIEDAD DEL SOFTWARE
+
SEGURIDAD
+
EVOLUCIÓN CONTROLADA

La nueva información estratégica amplía la visión del producto.

NO reemplaza las decisiones técnicas ya tomadas.

Las nuevas ideas deberán integrarse progresivamente cuando exista una necesidad concreta y después de la correspondiente evaluación y autorización.

El proyecto sigue teniendo dos objetivos simultáneos:

avanzar técnicamente el Medical CMS Platform;
desarrollar progresivamente la independencia del desarrollador.

La IA debe continuar funcionando principalmente como:

Profesor
+
Mentor
+
Revisor
+
Guía

y no solamente como:

Generador automático de código

El usuario debe intentar construir las partes nuevas por sí mismo siempre que el concepto ya haya sido explicado.

Cuando un intento propio contenga errores, primero se debe explicar:

qué está intentando hacer;
qué parte está correcta;
qué parte está incorrecta;
por qué está incorrecta;
cómo corregirla.

No entregar automáticamente código completo cuando sea más conveniente permitir un nuevo intento del usuario.

64. Regla nueva — Cambios de arquitectura, stack o tecnología

Se establece explícitamente:

No modificar tecnologías, lenguajes, arquitectura principal ni incorporar nuevas tecnologías sin autorización previa del usuario.

Actualmente NO se autoriza ningún cambio en el stack.

Stack actual confirmado:

Python
FastAPI
SQLAlchemy 2.0
Psycopg 3
PostgreSQL 17
Docker
Docker Compose
HTML5
CSS3
JavaScript

Si durante el desarrollo aparece una propuesta de mejora tecnológica:

explicar qué problema resuelve;
explicar ventajas;
explicar desventajas;
explicar alternativas;
explicar impacto sobre el proyecto existente;
esperar autorización del usuario;
recién después implementar.

La filosofía es:

MEJORAR
≠
REEMPLAZAR TODO

La evolución del sistema debe ser incremental.

65. Nueva visión estratégica del producto

La visión del proyecto evolucionó.

El objetivo ya no se limita a construir un CMS básico para una clínica.

La visión actual es:

Medical CMS Platform
↓
Plataforma SaaS médica
↓
Multi-tenant / Multi-centro
↓
Orientada al mercado argentino
↓
Profesionales médicos
Odontólogos
Ortodoncistas
Especialidades
Subespecialidades
Clínicas
Policonsultorios
Centros de diagnóstico
Hospitales / centros con internación como evolución futura

El sistema debe poder evolucionar hacia una plataforma centralizada capaz de manejar múltiples organizaciones y centros manteniendo aislamiento correcto de datos.

66. Posicionamiento estratégico

No se busca competir contra SAP Healthcare mediante cantidad absoluta de funcionalidades.

La estrategia es competir mediante:

Agilidad
+
Costo
+
Usabilidad
+
Implementación rápida
+
Adaptación al mercado argentino
+
Automatización
+
Interoperabilidad
+
Experiencia moderna

Mercado objetivo inicial recomendado:

Clínicas medianas
10–50 profesionales aproximadamente
Policonsultorios
Centros de diagnóstico
Redes de profesionales
Organizaciones médicas que necesitan crecer

No se debe intentar inicialmente competir directamente por funcionalidad empresarial contra:

SAP
Epic
grandes plataformas hospitalarias enterprise

La ventaja buscada es:

Software moderno
+
SaaS
+
Localización argentina
+
Menor complejidad
+
Menor costo de implementación
+
Automatización
+
UX moderna

La expresión:

"El SAP de las clínicas medianas"

puede utilizarse como referencia estratégica interna.

No se considera todavía un slogan comercial definitivo.

67. Diferenciadores futuros identificados

La investigación de mercado permitió identificar los siguientes posibles diferenciadores.

No todos deben implementarse inmediatamente.

Se mantienen como roadmap estratégico.

Multi-tenant / Multi-centro
        ↓
Inventario inteligente
        ↓
Scraping / integración de medicamentos
        ↓
Receta electrónica
        ↓
Historia clínica asistida por IA
        ↓
WhatsApp / Omnicanalidad
        ↓
Telemedicina
        ↓
Auditoría médica
        ↓
Camas y quirófanos
        ↓
Nomenclador de prestaciones
        ↓
Portal paciente
        ↓
Facturación
        ↓
Auditoría y seguridad avanzada
68. Multi-tenant y Multi-centro

La arquitectura debe evolucionar pensando desde el principio en múltiples organizaciones.

Conceptualmente:

Tenant / Organización
        ↓
Clínicas / Centros
        ↓
Profesionales
        ↓
Pacientes
        ↓
Turnos
        ↓
Historias clínicas
        ↓
Recetas
        ↓
Facturación

Una organización puede tener múltiples centros.

Ejemplo:

Organización Médica Central
    ├── Centro Palermo
    ├── Centro Belgrano
    ├── Centro Caballito
    └── Centro Norte

El objetivo es evitar construir el sistema suponiendo que una instalación equivale a una única clínica.

69. Estrategia de aislamiento de tenants

Se investigó como alternativa utilizar:

Una base de datos PostgreSQL
        ↓
múltiples schemas
        ↓
un schema por tenant / clínica

Ejemplo conceptual:

public
clinica_central
clinica_oeste
clinica_norte

También se investigó el uso de:

SET search_path TO ...

como mecanismo para seleccionar el schema de trabajo.

IMPORTANTE:

Esto NO está aprobado como arquitectura definitiva.

No debe implementarse todavía.

search_path por sí solo no debe considerarse una garantía completa de aislamiento de seguridad.

Antes de adoptar este enfoque será necesario comparar:

Schemas por tenant
vs.
tenant_id en tablas
vs.
Row Level Security
vs.
Arquitectura híbrida

La decisión debe realizarse posteriormente considerando:

seguridad;
complejidad;
migraciones;
rendimiento;
mantenimiento;
backup;
escalabilidad;
recuperación;
aislamiento.
70. Escalabilidad PostgreSQL

Se investigaron buenas prácticas para evitar que una base centralizada se convierta en un problema de rendimiento.

Se consideran especialmente:

Indexación inteligente
+
consultas optimizadas
+
UUIDs para determinadas entidades
+
almacenamiento externo de archivos

No significa que debamos aplicar todas estas decisiones inmediatamente.

Se deben introducir cuando el modelo correspondiente sea diseñado.

71. UUID — decisión futura

Se identificó como posible mejora utilizar UUID para entidades sensibles o que puedan exponerse mediante APIs.

Especialmente:

Patient
MedicalRecord
Prescription
Study
Document

Motivos:

evitar identificadores secuenciales predecibles;
facilitar determinadas integraciones;
facilitar migraciones/fusiones;
desacoplar identificadores internos del orden de creación.

IMPORTANTE:

No cambiar actualmente:

Clinic.id

No realizar una migración a UUID solamente por anticipación.

La decisión deberá evaluarse antes de crear las entidades sensibles correspondientes.

72. Archivos médicos y almacenamiento externo

Las historias clínicas pueden contener archivos grandes:

DICOM
PDF
Imágenes
Estudios
Fotos
Audio
Video

La dirección arquitectónica futura recomendada es:

PostgreSQL
↓
metadatos
+
referencia al archivo


Object Storage
↓
archivo físico

Posibles tecnologías futuras:

AWS S3
Google Cloud Storage
Azure Blob Storage
MinIO
Servidor propio

No se autoriza todavía ninguna tecnología de almacenamiento específica.

La decisión se tomará cuando aparezca la necesidad real del módulo de documentos/estudios.

73. Seguridad y datos médicos

La seguridad pasa a considerarse una característica transversal del sistema.

Las historias clínicas y datos de salud deben manejarse como información especialmente sensible.

Aspectos futuros prioritarios:

Autenticación
        ↓
Autorización
        ↓
Tenant
        ↓
Centro
        ↓
Profesional
        ↓
Paciente
        ↓
Historia clínica

También:

Auditoría
↓
quién
↓
qué hizo
↓
sobre qué dato
↓
cuándo

La Ley 25.326 establece reglas específicas para datos relativos a la salud y exige medidas técnicas y organizativas para preservar seguridad y confidencialidad. Esta normativa deberá considerarse desde el diseño de los módulos clínicos y de seguridad.

74. Auditoría médica

Se identificó como posible diferenciador de alto valor comercial.

Objetivo:

Prestación
    ↓
Código
    ↓
Obra social / Prepaga
    ↓
Reglas
    ↓
¿Requiere autorización?
    ↓
¿Falta documentación?
    ↓
¿Existe riesgo de débito?

La idea es que el sistema pueda detectar problemas antes de que la clínica facture una prestación que luego sea rechazada.

Este módulo se considera futuro.

No implementar todavía.

75. Scraping e inteligencia de inventario

El scraping deja de considerarse únicamente una función para obtener datos.

La visión futura es:

Fuentes externas
      ↓
Medicamentos
      ↓
Código / Troquel
      ↓
Precios
      ↓
Stock
      ↓
Alertas
      ↓
Gestión de inventario

Posibles fuentes y referencias a investigar posteriormente:

Vademécums
Manual Farmacéutico / Kairos
Alfabeta
Proveedores
Fuentes oficiales

IMPORTANTE:

No asumir que una fuente puede scrapearse legal o técnicamente sin restricciones.

Antes de implementar cada integración se deberá comprobar:

disponibilidad;
permisos;
términos de uso;
API oficial si existe;
frecuencia de actualización;
estructura de datos;
estabilidad;
legalidad de la extracción.
76. Obras sociales y prepagas

Se identificó una posible evolución del inventario y facturación:

Paciente
↓
Obra social / Prepaga
↓
Plan
↓
Medicamento / práctica / prestación
↓
Cobertura
↓
Autorización
↓
Facturación

El objetivo sería ayudar a reducir:

errores
+
débitos
+
prestaciones rechazadas

Esta área se considera uno de los posibles diferenciales comerciales del sistema en Argentina.

77. Receta electrónica

La receta electrónica pasa a formar parte de la visión futura del producto.

IMPORTANTE:

No implementar una solución propia suponiendo que basta con generar un PDF firmado.

La normativa argentina vigente establece que las plataformas de prescripción deben cumplir requisitos específicos y estar inscriptas/aprobadas por ReNaPDiS. Además, la Resolución 2214/2025 amplía el alcance de las prescripciones electrónicas a medicamentos, dispositivos, estudios, prácticas y procedimientos, y establece requisitos de interoperabilidad y conservación.

Por lo tanto, cuando llegue este módulo se deberá investigar:

ReNaPDiS
Normativa vigente
Interoperabilidad
CUIR
Repositorios
Prestadores
Farmacias
Plataformas habilitadas

La integración deberá diseñarse a partir de la normativa vigente en el momento de implementación.

78. Firma digital

Se incorporó como conocimiento futuro:

Ley 25.506
Firma electrónica
Firma digital
Certificados
Infraestructura de Firma Digital

La Ley 25.506 reconoce la firma electrónica y digital y establece la eficacia jurídica de la firma digital bajo las condiciones previstas legalmente.

La firma digital también proporciona mecanismos de presunción de autoría e integridad según el marco legal aplicable.

No implementar todavía.

Cuando llegue el módulo de recetas/documentos se deberá investigar:

certificadores licenciados;
certificados;
firma digital remota;
normativa vigente;
interoperabilidad;
requisitos de las plataformas sanitarias.
79. Historias clínicas + IA

Se identificó como posible diferenciador de alto valor.

Concepto:

Médico habla
    ↓
Audio
    ↓
Transcripción
    ↓
Estructuración
    ↓
Resumen
    ↓
Historia clínica

Posibles datos:

Motivo de consulta
Síntomas
Antecedentes
Observaciones
Diagnóstico
Plan
Indicaciones

IMPORTANTE:

La IA debe plantearse inicialmente como:

Asistente del profesional

y no como:

sustituto de decisión clínica

El profesional debe mantener el control sobre la información clínica final.

Se investigarán posteriormente:

LLMs locales
APIs
Speech-to-text
Procesamiento de lenguaje
Privacidad
Anonimización
Auditoría

No implementar todavía.

80. WhatsApp y omnicanalidad

Se identificó como posible diferenciador comercial importante.

Concepto futuro:

Turno
↓
Confirmación
↓
WhatsApp


Turno
↓
Recordatorio
↓
WhatsApp


Cancelación
↓
WhatsApp


Reagendamiento
↓
WhatsApp

También podrían incorporarse:

Email
SMS
Portal paciente

La integración debe evaluarse posteriormente mediante APIs oficiales y requisitos del proveedor correspondiente.

No incorporar ahora.

81. Telemedicina

Se identificó como módulo futuro.

Conceptualmente:

Turno
↓
Videollamada
↓
Historia clínica
↓
Consulta
↓
Registro
↓
Receta / indicaciones

Se mencionaron proveedores como:

Daily.co
Agora

pero ninguno está aprobado todavía como tecnología definitiva.

La selección futura deberá considerar:

seguridad;
privacidad;
estabilidad;
costos;
grabación;
almacenamiento;
integración con HCE;
requisitos legales;
experiencia de usuario.
82. Camas y quirófanos

Como posible evolución hacia clínicas con internación:

Camas
├── Disponible
├── Ocupada
├── Limpieza
└── Mantenimiento

Y:

Quirófanos
├── Disponible
├── Reservado
├── Preparación
└── Ocupado

La interfaz futura podría utilizar un tablero visual similar a Kanban.

No implementar todavía.

83. Nomenclador de prestaciones

Se identificó como posible módulo complementario al scraping de medicamentos.

Conceptualmente:

Práctica médica
↓
Código estándar
↓
Prestación
↓
Facturación

El objetivo sería evitar errores de carga y ayudar a la administración.

Antes de implementarlo habrá que identificar la fuente oficial/actualizada correspondiente y las reglas de uso.

No implementar todavía.

84. Portal del paciente

Módulo futuro:

Portal Paciente
├── Turnos
├── Recetas
├── Estudios
├── Documentos
└── Historial disponible

Objetivo:

reducir la dependencia de la atención administrativa por teléfono o canales manuales.

El portal deberá respetar:

Autenticación
Autorización
Privacidad
Tenant
Auditoría

No implementar todavía.

85. Facturación

Se identificó como módulo futuro:

Consulta
↓
Pago
↓
Facturación
↓
Comprobante

Se investigará posteriormente la integración vigente con los servicios de facturación electrónica de Argentina.

No fijar todavía:

librería
wrapper
API
proveedor

La selección debe realizarse al llegar al módulo y revisar la documentación oficial vigente.

86. Stack tecnológico — conclusión de la investigación

Después de analizar la nueva visión, NO se considera necesario cambiar el stack actual.

Stack confirmado:

Python
FastAPI
SQLAlchemy 2.0
Psycopg 3
PostgreSQL 17
Docker
Docker Compose
HTML
CSS
JavaScript

Ventajas para la evolución futura:

Python
→ IA
→ scraping
→ automatización
→ procesamiento


FastAPI
→ APIs
→ integraciones
→ servicios


SQLAlchemy
→ ORM
→ relaciones
→ consultas
→ PostgreSQL


PostgreSQL
→ datos relacionales
→ integridad
→ indexación
→ auditoría
→ multi-tenant


Docker
→ despliegue
→ aislamiento
→ servicios futuros

No se autoriza ningún cambio de stack actualmente.

87. GitHub — nuevo estado

El repositorio:

medical-cms-platform

ahora se encuentra:

PRIVATE

El único colaborador actualmente es el propietario del proyecto.

Esto se decidió porque el software se considera propietario y todavía se encuentra en desarrollo.

Flujo de trabajo:

Local
↓
develop
↓
commit
↓
push
↓
GitHub privado

No se modificó el flujo de Git.

IMPORTANTE:

Nunca subir al repositorio:

.env
Contraseñas
Tokens
API Keys
JWT secrets
Certificados privados
Claves privadas
Credenciales
Datos reales de pacientes
Historias clínicas reales
Recetas reales
Documentos médicos reales
88. Documentación de bloques completados

Durante las conversaciones posteriores al HANDOFF original se completaron y documentaron los siguientes bloques:

Bloque 2
POST /clinics/

Documento:

docs/technical-journal/2026-08-15-fastapi-first-clinic-endpoint.md
Bloque 3
GET /clinics/
GET /clinics/{clinic_id}

Documento:

docs/technical-journal/2026-08-15-clinic-read-endpoints.md
Bloque 4
PUT /clinics/{clinic_id}

Documento:

docs/technical-journal/2026-08-15-clinic-update-endpoint.md
Bloque 5
DELETE /clinics/{clinic_id}

Documento:

docs/technical-journal/2026-08-15-clinic-delete-endpoint.md

Los documentos se mantienen separados para conservar un historial independiente por bloque.

89. CRUD completo de Clinic

El sistema actualmente posee un CRUD funcional completo para Clinic.

CREATE
POST /clinics/
        ✅


READ
GET /clinics/
        ✅


READ ONE
GET /clinics/{clinic_id}
        ✅


UPDATE
PUT /clinics/{clinic_id}
        ✅


DELETE
DELETE /clinics/{clinic_id}
        ✅
90. Schemas actuales de Clinic

Actualmente deben existir:

ClinicCreate
ClinicUpdate
ClinicResponse

Conceptualmente:

ClinicCreate
↓
entrada para CREATE


ClinicUpdate
↓
entrada para UPDATE


ClinicResponse
↓
salida de API

No crear:

ClinicDelete

porque el DELETE actual no necesita request body.

91. Services actuales de Clinic

El service contiene actualmente:

create_clinic()
get_clinics()
get_clinic()
update_clinic()
delete_clinic()

La responsabilidad conceptual:

create_clinic()
→ crear


get_clinics()
→ obtener todos


get_clinic()
→ obtener uno


update_clinic()
→ actualizar uno


delete_clinic()
→ eliminar uno
92. Refactorización del Bloque 6

Se identificó duplicación en:

get_clinic()
update_clinic()
delete_clinic()

Antes update_clinic() y delete_clinic() repetían:

statement = select(Clinic).where(Clinic.id == clinic_id)
result = db.execute(statement)
clinic = result.scalar_one_or_none()

La refactorización fue:

get_clinic()
      ↑
      ├── GET
      ├── UPDATE
      └── DELETE

Ahora:

clinic = get_clinic(
    db=db,
    clinic_id=clinic_id,
)

se reutiliza desde update_clinic() y delete_clinic().

93. Resultado de la refactorización

La refactorización fue realizada sin introducir nuevas capas.

NO se incorporaron:

GenericRepository
BaseCRUD
BaseService
UnitOfWork
Repository Pattern genérico

La decisión fue mantener la arquitectura sencilla.

Razón:

la eliminación de duplicación conseguida ya aporta valor suficiente y las diferencias entre CREATE, UPDATE y DELETE todavía justifican mantener sus bloques de transacción separados.

94. Pruebas de regresión del Bloque 6

Después de la refactorización se comprobaron:

GET /clinics/3
        ✅


PUT /clinics/10
        ✅


PUT /clinics/10
        ✅


DELETE /clinics/11
        ✅

También se verificó directamente mediante SQLAlchemy que:

get_clinic(10)
→ Clinic encontrada

y:

get_clinics()
→ lista completa

No se detectó que el PUT generara un INSERT.

Durante las pruebas se observó un nuevo registro temporal y posteriormente se comprobó mediante los logs de Uvicorn que dicho registro había sido generado por:

POST /clinics/

y no por:

PUT /clinics/10

Esto confirmó que la refactorización no estaba generando registros adicionales accidentalmente.

95. Codificación UTF-8

Durante el Bloque 6 apareció repetidamente el problema:

No se encontrÃ³ la clÃnica solicitada

El problema correspondía a una representación incorrecta de caracteres.

Se corrigió el archivo:

backend/app/routes/clinic.py

y se verificó mediante Python:

MOJIBAKE: False
UTF8_CORRECTO: True

También se comprobó mediante OpenAPI que GET, PUT y DELETE reciben correctamente:

No se encontró la clínica solicitada

Regla futura:

Archivos del proyecto
↓
UTF-8

No utilizar escapes Unicode como solución normal para textos estáticos en español.

96. Saltos de línea Windows / Git

Durante la comprobación de Git apareció:

LF will be replaced by CRLF

Esto no representa un error funcional.

Es una advertencia relacionada con la normalización de finales de línea en Windows.

No se modificó todavía la configuración de Git ni se agregó .gitattributes.

Si este comportamiento comienza a generar problemas repetitivos en múltiples archivos, se podrá evaluar una política de finales de línea posteriormente.

No realizar cambios solamente por esta advertencia.

97. Estado de base de datos después de las pruebas

Estado conservado observado:

1 → Clínica Central
2 → Clínica del Oeste
3 → Clínica del Norte Premium
5 → Clínica del Sur
7 → Clinica especial del Oeste

Durante las pruebas del Bloque 6 se creó temporalmente:

10 → Clinica para prueba DELETE

Este registro quedó presente al momento de la última verificación.

IMPORTANTE:

Antes de comenzar a trabajar con nuevas entidades, revisar si el registro id = 10 sigue siendo un dato temporal.

No eliminarlo automáticamente sin verificar su estado.

98. Aprendizajes consolidados

Durante los bloques posteriores al HANDOFF original se consolidaron:

FastAPI
├── APIRouter
├── Depends
├── response_model
├── HTTPException
├── path parameters
├── OpenAPI
└── Swagger


Pydantic
├── BaseModel
├── validación de entrada
├── response schemas
└── ClinicCreate / ClinicUpdate / ClinicResponse


SQLAlchemy
├── Session
├── select()
├── where()
├── execute()
├── scalars()
├── all()
├── scalar_one_or_none()
├── add()
├── commit()
├── refresh()
├── delete()
└── rollback()


HTTP
├── POST
├── GET
├── PUT
├── DELETE
├── 200
├── 204
├── 404
└── 422
99. Conceptos HTTP aprendidos

Se consolidó:

POST
↓
crear


GET
↓
consultar


PUT
↓
actualizar


DELETE
↓
eliminar

Respuestas:

200
↓
operación exitosa con contenido


204
↓
operación exitosa sin contenido


404
↓
recurso inexistente


422
↓
datos recibidos inválidos
100. Diferencia entre Service y Endpoint

Se reforzó una separación importante.

El Service se encarga de lógica relacionada con datos:

Service
↓
Clinic / None
True / False

El Endpoint se encarga de traducir ese resultado a HTTP:

Clinic
↓
200


None
↓
404


True
↓
204


False
↓
404

Esto debe mantenerse en futuras entidades.

101. Primera experiencia de refactorización

El Bloque 6 introdujo una nueva etapa del aprendizaje:

Antes:
escribir código que funciona


Ahora:
escribir código que funciona
+
analizar si puede mantenerse mejor

Regla aprendida:

Refactorizar
≠
cambiar mucho código


Refactorizar
=
mejorar el código
manteniendo el comportamiento

No realizar abstracciones únicamente porque "se ven profesionales".

102. Regla para futuras refactorizaciones

Antes de introducir una abstracción:

Identificar una repetición real.
Confirmar que la repetición genera mantenimiento adicional.
Evaluar si la abstracción mantiene claridad.
Evaluar el beneficio.
Evitar sobre-arquitectura.
Probar que el comportamiento anterior sigue funcionando.
103. Estado actual de Clinic
Modelo
✅


Schema Create
✅


Schema Update
✅


Schema Response
✅


Service Create
✅


Service Read
✅


Service Update
✅


Service Delete
✅


Router Create
✅


Router Read
✅


Router Read One
✅


Router Update
✅


Router Delete
✅


Swagger
✅


OpenAPI
✅


PostgreSQL
✅
104. Estado del Bloque 6

Actualmente:

Bloque 6 — Refactorización

Estado:

Análisis
✅


Duplicación identificada
✅


Refactorización de get_clinic()
✅


update_clinic() reutiliza get_clinic()
✅


delete_clinic() reutiliza get_clinic()
✅


Pruebas GET
✅


Pruebas UPDATE
✅


Pruebas DELETE
✅


Verificación PostgreSQL
✅


Codificación UTF-8
✅


Revisión de diff
✅


Documentación
⏳


Commit
⏳


Push
⏳

El bloque se considera técnicamente terminado, pero todavía debe cerrarse formalmente mediante documentación y Git.

105. Próximo paso inmediato

Antes de crear Patient, completar:

Bloque 6
↓
documentación
↓
git add
↓
git diff --cached
↓
commit
↓
push

Después de cerrar Bloque 6:

Clinic CRUD
        ↓
patrón CRUD de referencia
        ↓
diseño de Patient
106. Próxima entidad — Patient

La siguiente entidad principal candidata es:

Patient

Pero NO comenzar directamente escribiendo el modelo.

Primero analizar:

¿Qué es Patient?
¿Qué datos necesita?
¿Qué datos son sensibles?
¿Qué identifica de forma única al paciente?
¿Qué pertenece al tenant?
¿Qué pertenece al centro?
¿Qué relaciones tendrá?
¿Qué identificadores deberá utilizar?

Se debe evaluar especialmente:

UUID
Tenant
Clinic / Center
DNI
Obra Social / Prepaga
Datos de contacto
Auditoría
Privacidad

No agregar campos anticipadamente sin definir primero el dominio.

107. Modelo conceptual futuro de Patient

No es implementación todavía.

Es solamente una referencia conceptual:

Tenant
   ↓
Clinic / Center
   ↓
Patient
   ├── Datos personales
   ├── Identificación
   ├── Contacto
   ├── Cobertura
   ├── Turnos
   ├── Historias clínicas
   ├── Recetas
   ├── Estudios
   └── Documentos

Las relaciones se definirán posteriormente.

108. Nueva regla para entidades médicas

Antes de crear entidades como:

Patient
MedicalRecord
Prescription
Study

se debe evaluar:

Seguridad
+
Privacidad
+
Auditoría
+
Tenant
+
Identificador
+
Relaciones

No empezar por el CRUD simplemente porque ya sabemos hacerlo.

Primero definir correctamente el modelo de negocio.

109. Diferencia entre CRUD de ejemplo y dominio real

Clinic fue utilizado como entidad de aprendizaje.

Su CRUD sirvió para aprender:

CREATE
READ
UPDATE
DELETE

Pero las entidades médicas futuras pueden tener reglas mucho más complejas.

Por ejemplo:

Patient
↓
no debería eliminarse físicamente de cualquier forma

y:

MedicalRecord
↓
requiere trazabilidad
↓
auditoría
↓
historial

Por lo tanto no asumir que todos los recursos del sistema tendrán exactamente el mismo comportamiento que Clinic.

110. Estrategia futura de CRUD

El CRUD aprendido con Clinic debe utilizarse como:

Patrón de aprendizaje
+
referencia

No como una plantilla que se copie ciegamente a todas las entidades.

Cada nueva entidad debe analizar:

¿CRUD simple?
¿CRUD con reglas?
¿Soft delete?
¿Auditoría?
¿Histórico?
¿Inmutabilidad?
¿Relaciones?
¿Permisos?
111. Repositorio GitHub

Estado actual:

medical-cms-platform
↓
PRIVATE

Rama:

develop

Rama estable:

main

El flujo continúa:

develop
↓
commit
↓
push
↓
GitHub privado

El repositorio es propiedad del usuario y no debe hacerse público sin decisión explícita.

112. Propiedad intelectual y exposición del código

El proyecto se considera software propietario.

Por esta razón:

Repositorio
→ privado


Código
→ no publicar sin autorización


Documentación técnica
→ privada


Secrets
→ nunca subir


Datos reales
→ nunca subir

No convertir el repositorio en público sin evaluar previamente:

propiedad intelectual;
licenciamiento;
código que se desea revelar;
documentación que se desea publicar;
dependencias;
secretos;
copias/forks existentes.
113. Nueva visión comercial

La propuesta de valor futura se basa en:

SaaS
+
Multi-tenant
+
Multi-centro
+
UX moderna
+
Mercado argentino
+
Automatización
+
WhatsApp
+
Receta electrónica
+
Inventario
+
Auditoría
+
HCE
+
IA
+
Facturación

Pero estas funcionalidades deben implementarse progresivamente.

No intentar construirlas todas al mismo tiempo.

114. Prioridad de producto

La prioridad sigue siendo:

1.
Base técnica sólida


2.
Modelo de dominio correcto


3.
Seguridad


4.
CRUDs y funcionalidades fundamentales


5.
Multi-tenant


6.
Integraciones


7.
Automatización


8.
IA


9.
Funcionalidades avanzadas


10.
Escalabilidad comercial

La prioridad exacta puede ajustarse mediante el roadmap.

115. Regla fundamental sobre nuevas tecnologías

No agregar:

React
Vue
Next.js
Redis
RabbitMQ
Kafka
Celery
MongoDB
Kubernetes
AWS
etc.

solamente porque puedan ser útiles en algún momento.

Cada tecnología futura deberá pasar por:

Problema
↓
Necesidad
↓
Alternativas
↓
Ventajas
↓
Desventajas
↓
Impacto
↓
Autorización
↓
Implementación

El stack actual permanece vigente.

116. Regla fundamental sobre funcionalidades futuras

Las funcionalidades futuras identificadas:

Scraping
IA
WhatsApp
Telemedicina
Receta electrónica
Facturación
Portal paciente
Auditoría
Camas
Quirófanos
Nomenclador

son:

ROADMAP

No son funcionalidades autorizadas para implementación inmediata.

Antes de implementarlas:

Analizar
↓
investigar
↓
explicar
↓
estimar impacto
↓
autorizar
↓
implementar
117. Arquitectura conceptual futura

La arquitectura objetivo continúa siendo una evolución de:

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

Con futuras integraciones:

FastAPI
   ├── WhatsApp
   ├── Receta electrónica
   ├── AFIP / servicios fiscales
   ├── Telemedicina
   ├── Fuentes de medicamentos
   ├── Nomencladores
   └── IA

Y:

PostgreSQL
   ↓
metadatos
   +
datos relacionales

mientras:

Object Storage
   ↓
documentos y archivos pesados

Esta arquitectura es una visión futura y no implica cambios inmediatos.

118. Principio de seguridad futura

Para una plataforma médica se deberá diseñar bajo el principio:

Seguridad desde el diseño

y no:

Seguridad al final

Aspectos futuros:

Password hashing
JWT / autenticación
RBAC
Tenant isolation
Auditoría
Logs
Cifrado
Gestión de secretos
Control de acceso
Backups
Recuperación
Trazabilidad

No implementar todo simultáneamente.

Se deben introducir progresivamente.

119. Regla sobre IA clínica

La IA debe plantearse inicialmente como:

Asistente

No como:

Autoridad clínica

Toda generación automática de contenido médico debe poder:

ser revisada
ser corregida
ser aceptada/rechazada
quedar auditada

El médico debe conservar el control sobre la información clínica final.

120. Regla sobre normativa argentina

Toda integración regulada deberá verificarse con documentación oficial vigente en el momento de implementación.

Especialmente:

Receta electrónica
Firma digital
AFIP / ARCA
SISA
Datos personales
Obras sociales
Facturación
Interoperabilidad sanitaria

No asumir que una investigación realizada hoy será válida indefinidamente.

La normativa debe revisarse nuevamente cuando el módulo vaya a implementarse.

121. Estado final actualizado para continuidad
PROJECT
update_clinic()
delete_clinic()
✅


REGRESSION TESTS
✅


UTF-8
✅


SECURITY STRATEGY
En diseño progresivo


MULTI-TENANT
Visión estratégica
No implementado todavía


PATIENT
Próxima entidad a analizar


NEXT
Cerrar Bloque 6
↓
Commit
↓
Push
↓
Diseñar Patient
122. Punto exacto para retomar en una nueva conversación

Al abrir una nueva conversación:

Leer el HANDOFF original completo.
Leer desde la sección 62 de este documento agregado.
No repetir los bloques 1–5.
Reconocer que Clinic posee CRUD completo.
Reconocer que el repositorio es privado.
Reconocer que el Bloque 6 está técnicamente terminado pero pendiente de cierre documental/Git.
Finalizar el cierre del Bloque 6.
Después comenzar el diseño de Patient.

El siguiente objetivo NO es comenzar inmediatamente a copiar el CRUD de Clinic.

Primero:

Patient
↓
analizar dominio
↓
identificar datos
↓
identificar relaciones
↓
identificar tenant
↓
identificar seguridad
↓
evaluar UUID
↓
crear modelo

Después se construirá progresivamente su CRUD.

123. Recordatorio final de metodología

Mantener siempre:

Pequeño paso
     ↓
Explicación
     ↓
Ejemplo
     ↓
Intento propio
     ↓
Corrección
     ↓
Aplicación
     ↓
Prueba
     ↓
Verificación
     ↓
Documentación
     ↓
Git
     ↓
Siguiente paso

No avanzar más rápido sacrificando comprensión.

No introducir tecnologías sin autorización.

No introducir arquitectura innecesaria.

No copiar patrones sin entenderlos.

No modificar bloques históricos ya documentados salvo que exista un error real que requiera corrección.

Cada bloque debe dejar:

Proyecto mejor
+
Desarrollador con más conocimiento
124. Regla definitiva de continuidad

Este HANDOFF actualizado mantiene como prioridad absoluta:

CONTINUIDAD
+
APRENDIZAJE
+
DESARROLLO PROGRESIVO
+
PROPIEDAD DEL SOFTWARE
+
SEGURIDAD
+
EVOLUCIÓN CONTROLADA

La nueva información estratégica amplía la visión del producto.

NO reemplaza las decisiones técnicas ya tomadas.

Las nuevas ideas deberán integrarse progresivamente cuando exista una necesidad concreta y después de la correspondiente evaluación y autorización.