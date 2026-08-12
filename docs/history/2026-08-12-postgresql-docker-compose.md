# Configuración de PostgreSQL con Docker Compose

**Fecha:** 2026-08-12  
**Rama:** `develop`  
**Proyecto:** Medical CMS Platform

## Contexto

Al retomar el desarrollo del proyecto se detectó que Docker no tenía configurado el entorno de PostgreSQL correspondiente a `medical-cms-platform`.

El proyecto contaba con la estructura de directorios `docker/` y un archivo `docker-compose.yml`, pero este último se encontraba vacío.

Además, Docker Desktop ya estaba funcionando y existía un contenedor perteneciente a otro proyecto. Ese contenedor no debía modificarse ni eliminarse.

## Situación inicial

El archivo `docker-compose.yml` se encontraba vacío:

```text
docker-compose.yml

Al ejecutar:

docker ps

no aparecía ningún contenedor correspondiente a medical-cms-platform.

Sin embargo, Docker Desktop estaba correctamente instalado y operativo.

También se comprobó que existía la imagen:

postgres:17

Esta imagen correspondía al proyecto y podía utilizarse para crear el servicio de PostgreSQL.

Configuración de Docker Compose

Se configuró docker-compose.yml para crear un servicio PostgreSQL:

services:

  postgres:
    image: postgres:17

    environment:
      POSTGRES_DB: medical_cms
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres

    ports:
      - "5432:5432"

    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
Componentes principales
postgres:17: imagen utilizada para PostgreSQL.
POSTGRES_DB: nombre de la base de datos.
POSTGRES_USER: usuario de PostgreSQL.
POSTGRES_PASSWORD: contraseña del usuario.
5432:5432: permite acceder a PostgreSQL desde el entorno local.
postgres_data: volumen persistente para conservar los datos de PostgreSQL.
Validación de Docker Compose

Antes de iniciar los servicios se ejecutó:

docker compose config

La configuración fue validada correctamente y Docker generó el servicio:

medical-cms-platform

con:

postgres

como servicio principal.

Creación del entorno

Se ejecutó:

docker compose up -d

Docker creó:

La red medical-cms-platform_default
El volumen medical-cms-platform_postgres_data
El contenedor medical-cms-platform-postgres-1

Resultado:

[+] up 3/3
 ✔ Network medical-cms-platform_default      Created
 ✔ Volume medical-cms-platform_postgres_data Created
 ✔ Container medical-cms-platform-postgres-1 Started
Verificación del contenedor

Se comprobó el estado mediante:

docker compose ps

Resultado:

NAME                              IMAGE         COMMAND                  SERVICE    CREATED          STATUS          PORTS
medical-cms-platform-postgres-1   postgres:17   "docker-entrypoint.s…"   postgres   Up             0.0.0.0:5432->5432/tcp

El contenedor quedó funcionando correctamente.

También se verificó mediante:

docker ps

sin modificar ni detener el contenedor correspondiente al otro proyecto.

Configuración del backend

Se agregaron las variables de conexión a PostgreSQL en backend/app/config/settings.py:

db_host: str = "localhost"
db_port: int = 5432
db_name: str = "medical_cms"
db_user: str = "postgres"
db_password: str = "postgres"

También se documentaron estas variables en:

backend/.env.example

con una contraseña de ejemplo:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=medical_cms
DB_USER=postgres
DB_PASSWORD=change_me

El archivo .env real permanece fuera del control de versiones.

Conexión SQLAlchemy + PostgreSQL

Se creó:

backend/app/database.py

con la configuración del engine de SQLAlchemy:

from sqlalchemy import create_engine

from app.config.settings import settings


DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}"
    f"/{settings.db_name}"
)


engine = create_engine(DATABASE_URL)

Esto permite que SQLAlchemy utilice psycopg como driver para conectarse a PostgreSQL.

Problema encontrado con psycopg

Inicialmente estaba instalado:

psycopg==3.3.4

pero al intentar crear el engine se produjo:

ImportError: no pq wrapper available.

El problema se debía a que psycopg no encontraba una implementación disponible de libpq en el entorno de Windows.

Se solucionó instalando:

pip install "psycopg[binary]==3.3.4"

Esto agregó:

psycopg==3.3.4
psycopg-binary==3.3.4

al entorno virtual.

Posteriormente se actualizó:

backend/requirements.txt

para incluir:

psycopg-binary==3.3.4
Prueba de conexión

Se verificó que SQLAlchemy pudiera crear correctamente el engine:

python -c "from app.database import engine; print(engine)"

Resultado:

Engine(postgresql+psycopg://postgres:***@localhost:5432/medical_cms)

Posteriormente se ejecutó una consulta real contra PostgreSQL:

python -c "from app.database import engine; from sqlalchemy import text; connection = engine.connect(); print(connection.execute(text('SELECT 1')).scalar()); connection.close()"

Resultado:

1

Esto confirmó que:

SQLAlchemy funciona correctamente.
psycopg funciona correctamente.
PostgreSQL está accesible.
El contenedor de PostgreSQL está funcionando.
La base de datos medical_cms responde correctamente.
La conexión entre el backend y PostgreSQL está establecida.
Control de cambios

Los cambios fueron revisados mediante:

git --no-pager diff --check

sin errores.

Se incorporaron los siguientes archivos:

backend/.env.example
backend/app/config/settings.py
backend/app/database.py
backend/requirements.txt
docker-compose.yml
Commits realizados
Configuración de Docker
771c5 build: configurar PostgreSQL con Docker Compose

Este commit agregó la configuración de PostgreSQL mediante Docker Compose.

Driver de PostgreSQL
5e3c0 build: agregar driver de PostgreSQL

Este commit incorporó el driver psycopg utilizado por SQLAlchemy.

Los cambios posteriores relacionados con la conexión de SQLAlchemy y psycopg-binary fueron enviados a la rama develop.

Estado final

Al finalizar el bloque:

git status

debe mostrar:

On branch develop
Your branch is up to date with 'origin/develop'.

nothing to commit, working tree clean

Y:

docker compose ps

debe mostrar el contenedor:

medical-cms-platform-postgres-1

en estado:

Up

con PostgreSQL disponible en:

localhost:5432
Resultado

El proyecto quedó con la infraestructura básica de persistencia configurada:

FastAPI
   │
   ▼
SQLAlchemy
   │
   ▼
psycopg
   │
   ▼
PostgreSQL 17
   │
   ▼
Docker Container

La conexión entre el backend y PostgreSQL fue probada mediante una consulta real y respondió correctamente.

Este bloque queda cerrado y listo para continuar con la siguiente etapa del desarrollo.


### Una observación importante

Hay un detalle que **no debemos dar por terminado todavía**: el archivo `backend/app/database.py` quedó creado, pero todavía no hemos integrado el `engine` con la aplicación FastAPI mediante una sesión (`Session`/`sessionmaker` o `sessionmaker` de SQLAlchemy 2.0).

Eso **no es un error**. Simplemente significa que en este bloque establecimos y comprobamos la conexión base. La creación de sesiones y su integración con los endpoints debería ser el siguiente bloque, no mezclarlo con este.

Por lo tanto, para mí el estado correcto es:

**Bloque PostgreSQL + Docker Compose + conexión SQLAlchemy → ✅ CERRADO**

**Integración de sesiones SQLAlchemy con FastAPI → ⏭️ SIGUIENTE BLOQUE**