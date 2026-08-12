# Configuración de SQLAlchemy y conexión con PostgreSQL

**Fecha:** 2026-08-12  
**Rama:** `develop`  
**Proyecto:** Medical CMS Platform  
**Archivo documentado:** `backend/app/database.py`

---

## 1. Objetivo

El archivo `database.py` establece la conexión entre el backend y PostgreSQL mediante SQLAlchemy.

Su responsabilidad actual es:

- importar la configuración de la aplicación;
- construir la URL de conexión a PostgreSQL;
- indicar que el driver utilizado será `psycopg`;
- crear el `engine` de SQLAlchemy.

Este archivo constituye la primera capa de acceso a la base de datos del backend.

---

## 2. Ubicación

El archivo se encuentra en:

```text
backend/
└── app/
    └── database.py
3. Código actual

El archivo contiene:

from sqlalchemy import create_engine

from app.config.settings import settings


DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}"
    f"/{settings.db_name}"
)


engine = create_engine(DATABASE_URL)
4. Importación de SQLAlchemy

El archivo comienza con:

from sqlalchemy import create_engine

create_engine() es la función de SQLAlchemy utilizada para crear el Engine.

El Engine representa el punto de entrada principal de SQLAlchemy hacia la base de datos.

En este proyecto será utilizado posteriormente por la capa de persistencia.

5. Importación de la configuración

Se importa la instancia global settings:

from app.config.settings import settings

Esta instancia fue definida en:

backend/app/config/settings.py

Gracias a esto, database.py no necesita definir nuevamente:

host;
puerto;
nombre de la base de datos;
usuario;
contraseña.

En lugar de duplicar esos valores, los obtiene desde settings.

6. Construcción de DATABASE_URL

El archivo construye la URL de conexión mediante:

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}"
    f"/{settings.db_name}"
)

La URL sigue el formato general:

postgresql+psycopg://usuario:contraseña@host:puerto/base_de_datos

En nuestro entorno actual los valores son:

usuario:        postgres
contraseña:     postgres
host:           localhost
puerto:         5432
base de datos:  medical_cms
driver:         psycopg

Por lo tanto, conceptualmente la conexión queda:

postgresql+psycopg://postgres:postgres@localhost:5432/medical_cms

SQLAlchemy oculta la contraseña cuando muestra el objeto Engine.

7. ¿Qué significa postgresql+psycopg?

La primera parte:

postgresql

indica el sistema gestor de base de datos.

En este caso:

PostgreSQL

La segunda parte:

psycopg

indica el driver que SQLAlchemy utilizará para comunicarse con PostgreSQL.

Por lo tanto:

postgresql+psycopg

significa:

Utilizar SQLAlchemy para conectarse a PostgreSQL mediante el driver Psycopg.

8. Driver psycopg

El proyecto utiliza:

psycopg==3.3.4

Durante la configuración inicial se detectó que la instalación básica de psycopg no podía encontrar una implementación disponible de libpq en Windows.

El error obtenido fue:

ImportError: no pq wrapper available.

Entre los intentos indicados por Psycopg se encontraba:

libpq library not found
9. Solución mediante psycopg-binary

Para solucionar el problema se instaló:

pip install "psycopg[binary]==3.3.4"

Esto agregó:

psycopg==3.3.4
psycopg-binary==3.3.4

El paquete psycopg-binary proporciona los componentes binarios necesarios para utilizar Psycopg sin tener que instalar manualmente libpq en el entorno local.

Posteriormente se verificó:

pip freeze | Select-String "psycopg"

Resultado:

psycopg==3.3.4
psycopg-binary==3.3.4

También se incorporó:

psycopg-binary==3.3.4

al archivo:

backend/requirements.txt
10. Creación del Engine

Una vez construida la URL, se crea el engine:

engine = create_engine(DATABASE_URL)

El resultado es un objeto Engine de SQLAlchemy.

Este objeto será el encargado de administrar la comunicación con PostgreSQL.

La creación del engine fue comprobada mediante:

python -c "from app.database import engine; print(engine)"

Resultado:

Engine(postgresql+psycopg://postgres:***@localhost:5432/medical_cms)

La contraseña aparece ocultada:

***

Esto es el comportamiento esperado al representar el objeto de conexión.

11. Prueba real de conexión

La creación del Engine por sí sola no garantiza que PostgreSQL sea accesible.

Por este motivo se realizó una prueba real mediante SQLAlchemy.

Se ejecutó:

python -c "from app.database import engine; from sqlalchemy import text; connection = engine.connect(); print(connection.execute(text('SELECT 1')).scalar()); connection.close()"

Resultado:

1

Esta prueba fue especialmente importante porque confirmó que la cadena completa funciona:

Aplicación
    ↓
SQLAlchemy
    ↓
Psycopg
    ↓
localhost:5432
    ↓
Docker
    ↓
PostgreSQL 17
    ↓
medical_cms
12. ¿Qué comprueba SELECT 1?

La consulta:

SELECT 1;

es una consulta mínima utilizada para comprobar que la base de datos responde.

No consulta ninguna tabla ni modifica información.

Si devuelve:

1

significa que la conexión pudo establecerse correctamente y PostgreSQL procesó la consulta.

Por lo tanto, fue una prueba adecuada para validar la infraestructura antes de comenzar a crear modelos y tablas.

13. Relación con Docker Compose

PostgreSQL se ejecuta actualmente dentro del contenedor:

medical-cms-platform-postgres-1

El servicio utiliza:

postgres:17

y publica:

5432:5432

Por este motivo, desde Windows el backend puede conectarse utilizando:

localhost:5432

La relación es:

Windows
  │
  │ localhost:5432
  ▼
Docker
  │
  ▼
medical-cms-platform-postgres-1
  │
  ▼
PostgreSQL 17
14. Relación con settings.py

database.py depende de la configuración definida en:

backend/app/config/settings.py

La relación es:

settings.py
     │
     │ proporciona
     ▼
db_host
db_port
db_name
db_user
db_password
     │
     ▼
database.py
     │
     │ construye
     ▼
DATABASE_URL
     │
     ▼
create_engine()
     │
     ▼
SQLAlchemy Engine

Esto evita duplicar la configuración de conexión.

15. Separación de responsabilidades

Actualmente cada componente tiene una responsabilidad específica.

.env

Contiene valores específicos del entorno local.

.env
settings.py

Lee y organiza esos valores.

Settings
database.py

Utiliza esos valores para configurar SQLAlchemy.

DATABASE_URL
Engine
docker-compose.yml

Define y ejecuta PostgreSQL.

PostgreSQL 17

La arquitectura queda:

.env
 │
 ▼
settings.py
 │
 ▼
database.py
 │
 ▼
SQLAlchemy
 │
 ▼
psycopg
 │
 ▼
PostgreSQL
16. Estado actual del archivo

Actualmente database.py solamente se encarga de crear el Engine.

Todavía no contiene:

Session;
sessionmaker;
dependencias de FastAPI;
modelos ORM;
creación de tablas;
migraciones;
repositorios.

Esto es intencional.

El objetivo de este bloque fue establecer primero una conexión funcional y comprobada con PostgreSQL.

17. Próxima evolución

En un siguiente bloque se podrá agregar la gestión de sesiones de SQLAlchemy.

Conceptualmente:

Engine
  │
  ▼
Session
  │
  ▼
FastAPI Dependency
  │
  ▼
Endpoint

Esto permitirá que los endpoints puedan solicitar una sesión de base de datos y ejecutar operaciones mediante SQLAlchemy.

Posteriormente se podrán incorporar los modelos ORM.

18. Seguridad

Actualmente la contraseña utilizada en desarrollo es:

postgres

Esto corresponde exclusivamente al entorno local.

La contraseña no debería estar escrita directamente dentro de database.py.

Actualmente se obtiene desde:

settings.db_password

Esto mantiene las credenciales fuera de la lógica de conexión.

La configuración real se encuentra en:

backend/.env

mientras que el repositorio utiliza:

backend/.env.example

como plantilla.

Antes de utilizar el sistema en producción deberán utilizarse credenciales seguras y una gestión adecuada de secretos.

19. Verificaciones realizadas

Durante este bloque se realizaron las siguientes comprobaciones.

Verificación del driver
pip freeze | Select-String "psycopg"

Resultado:

psycopg==3.3.4
psycopg-binary==3.3.4
Verificación del engine
python -c "from app.database import engine; print(engine)"

Resultado:

Engine(postgresql+psycopg://postgres:***@localhost:5432/medical_cms)
Verificación de conexión
python -c "from app.database import engine; from sqlalchemy import text; connection = engine.connect(); print(connection.execute(text('SELECT 1')).scalar()); connection.close()"

Resultado:

1

Estas comprobaciones confirmaron que la conexión funcional quedó establecida.

20. Archivos relacionados

Este archivo forma parte del bloque de configuración de persistencia junto con:

backend/
├── .env
├── .env.example
├── requirements.txt
└── app/
    ├── config/
    │   └── settings.py
    └── database.py

También depende de la infraestructura definida en:

docker-compose.yml
21. Resultado

El archivo database.py permite al backend crear un Engine de SQLAlchemy conectado a PostgreSQL 17 mediante Psycopg.

La conexión fue probada mediante una consulta real:

SELECT 1;

obteniendo:

1

Por lo tanto, queda validada la primera conexión funcional entre el backend y PostgreSQL.

El bloque de infraestructura y conexión queda compuesto por:

Docker Compose
      │
      ▼
PostgreSQL 17
      │
      ▲
      │
   psycopg
      │
      ▲
      │
SQLAlchemy
      │
      ▲
      │
database.py
      ▲
      │
settings.py
      ▲
      │
     .env

Estado: COMPLETADO


### Con esto cerramos la documentación del bloque

Los archivos documentados quedan:

1. `docker-compose.yml`
2. `backend/app/config/settings.py`
3. `backend/app/database.py`

Y como soporte de configuración:

4. `backend/.env.example`
5. `backend/requirements.txt`

**Importante:** todavía no haría otro commit hasta que guardes este documento y revisemos juntos `git status`. Así mantenemos el cierre del bloque limpio y podemos decidir si la documentación entra en **un único commit documental** o si conviene agruparla con el trabajo técnico anterior.