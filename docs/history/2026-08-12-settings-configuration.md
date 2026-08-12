# Configuración de Settings del Backend

**Fecha:** 2026-08-12  
**Rama:** `develop`  
**Proyecto:** Medical CMS Platform  
**Archivo documentado:** `backend/app/config/settings.py`

---

## 1. Objetivo

El archivo `settings.py` centraliza la configuración de la aplicación backend.

Su responsabilidad es definir los valores de configuración que necesita Medical CMS Platform y permitir que estos valores puedan ser obtenidos desde variables de entorno, principalmente mediante el archivo `.env`.

Esto evita tener toda la configuración distribuida dentro del código de la aplicación.

---

## 2. Ubicación

El archivo se encuentra en:

```text
backend/
└── app/
    └── config/
        └── settings.py

Actualmente contiene la clase Settings y una instancia global llamada settings.

3. Código actual

El archivo contiene:

"""
Configuración principal de la aplicación.

Los valores se obtienen desde variables de entorno
y/o desde el archivo .env.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings:
    """
    Configuración de Medical CMS Platform.
    """

    app_name: str = "Medical CMS Platform API"
    app_version: str = "0.1.0"
    debug: bool = True

    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "medical_cms"
    db_user: str = "postgres"
    db_password: str = "postgres"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()

Nota: la clase debe heredar de BaseSettings. La implementación correcta es:

class Settings(BaseSettings):

Esto es necesario para que pydantic-settings gestione correctamente las variables de entorno.

4. Importaciones

Se utilizan dos elementos principales:

from pydantic_settings import BaseSettings, SettingsConfigDict
BaseSettings

BaseSettings proporciona el comportamiento necesario para crear una configuración basada en variables de entorno.

Permite que los valores definidos en la clase puedan ser reemplazados por valores provenientes del entorno o de un archivo .env.

Por ejemplo:

db_port: int = 5432

define 5432 como valor por defecto.

Pero si existe:

DB_PORT=5433

la configuración puede utilizar 5433.

SettingsConfigDict

SettingsConfigDict permite indicar cómo debe comportarse BaseSettings.

En nuestro caso se utiliza para indicar:

dónde está el archivo .env;
qué codificación debe utilizar;
qué hacer con variables adicionales.
5. Clase Settings

La configuración se agrupa dentro de:

class Settings(BaseSettings):

Esto permite tener un único objeto responsable de almacenar la configuración de la aplicación.

La ventaja principal es que el resto del proyecto puede acceder a la configuración mediante:

settings

en lugar de leer directamente el archivo .env.

6. Configuración general de la aplicación

Actualmente existen tres variables generales.

app_name
app_name: str = "Medical CMS Platform API"

Define el nombre de la aplicación.

Tipo:

str

Valor por defecto:

Medical CMS Platform API

Esta configuración puede utilizarse posteriormente en FastAPI, documentación OpenAPI u otros componentes del sistema.

app_version
app_version: str = "0.1.0"

Define la versión actual de la API.

Tipo:

str

Valor:

0.1.0

La versión puede utilizarse posteriormente para identificar la versión de la API expuesta por el backend.

debug
debug: bool = True

Indica si la aplicación está ejecutándose en modo de desarrollo.

Tipo:

bool

Valor actual:

True

Esta configuración deberá revisarse posteriormente cuando se prepare el entorno de producción.

7. Configuración de PostgreSQL

Como parte de la integración con PostgreSQL, se agregaron las siguientes variables:

db_host: str = "localhost"
db_port: int = 5432
db_name: str = "medical_cms"
db_user: str = "postgres"
db_password: str = "postgres"

Estas variables permiten construir posteriormente la URL de conexión utilizada por SQLAlchemy.

db_host
db_host: str = "localhost"

Indica dónde se encuentra disponible PostgreSQL.

Actualmente:

localhost

Esto es correcto para el escenario actual porque el backend se está ejecutando directamente desde Windows y PostgreSQL está publicado por Docker en el puerto local 5432.

db_port
db_port: int = 5432

Indica el puerto utilizado para conectarse a PostgreSQL.

Tipo:

int

Valor:

5432

Docker actualmente realiza el siguiente mapeo:

5432:5432

Por lo tanto, PostgreSQL queda disponible desde:

localhost:5432
db_name
db_name: str = "medical_cms"

Define el nombre de la base de datos que utiliza el proyecto.

Valor:

medical_cms

Este nombre coincide con la configuración de PostgreSQL definida en docker-compose.yml.

db_user
db_user: str = "postgres"

Define el usuario utilizado para conectarse a PostgreSQL.

Actualmente:

postgres
db_password
db_password: str = "postgres"

Define la contraseña utilizada para la conexión.

En el entorno actual de desarrollo coincide con la contraseña configurada para el contenedor de PostgreSQL.

Esta configuración deberá mejorarse antes de utilizar el proyecto en producción. Las credenciales reales no deben quedar almacenadas directamente en el código fuente.

8. model_config

La clase contiene:

model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore",
)

Esta configuración define cómo BaseSettings obtiene y procesa los valores.

env_file
env_file=".env"

Indica que se debe utilizar el archivo:

.env

como fuente de variables de entorno.

En nuestro proyecto:

backend/
├── .env
└── .env.example

El archivo .env contiene los valores utilizados por el entorno local.

env_file_encoding
env_file_encoding="utf-8"

Indica que el archivo .env debe interpretarse utilizando codificación UTF-8.

Esto evita problemas relacionados con caracteres especiales.

extra
extra="ignore"

Indica que las variables adicionales presentes en .env, pero que no estén declaradas dentro de Settings, deben ignorarse.

Esto permite que el archivo .env pueda contener otras variables sin provocar un error de validación.

9. Instancia global

Al final del archivo se crea:

settings = Settings()

Esto crea una única instancia de la configuración.

El resto de la aplicación puede importarla mediante:

from app.config.settings import settings

Por ejemplo:

from app.config.settings import settings

print(settings.db_host)
print(settings.db_port)

Resultado esperado:

localhost
5432
10. Relación con .env

El archivo .env utilizado actualmente contiene:

APP_NAME=Medical CMS Platform API
APP_VERSION=0.1.0
DEBUG=true

DB_HOST=localhost
DB_PORT=5432
DB_NAME=medical_cms
DB_USER=postgres
DB_PASSWORD=postgres

BaseSettings relaciona estas variables con los atributos de la clase.

Por ejemplo:

APP_NAME

se relaciona con:

app_name

y:

DB_HOST

con:

db_host

Pydantic Settings realiza la conversión de tipos cuando corresponde.

11. Validación de tipos

Una de las ventajas de utilizar BaseSettings es que los valores pueden tener tipos definidos.

Actualmente:

Configuración	Tipo
app_name	str
app_version	str
debug	bool
db_host	str
db_port	int
db_name	str
db_user	str
db_password	str

Se comprobó mediante Python que los valores de conexión se cargan correctamente:

print(type(settings.db_host))
print(type(settings.db_port))
print(type(settings.db_name))
print(type(settings.db_user))
print(type(settings.db_password))

Resultado:

<class 'str'>
<class 'int'>
<class 'str'>
<class 'str'>
<class 'str'>

Esto confirma que DB_PORT, por ejemplo, se transforma correctamente en un entero.

12. Relación con SQLAlchemy

settings.py no establece directamente la conexión con PostgreSQL.

Su responsabilidad es proporcionar los datos necesarios para que otro módulo pueda hacerlo.

Actualmente esa responsabilidad corresponde a:

backend/app/database.py

Este archivo utiliza:

from app.config.settings import settings

y posteriormente obtiene:

settings.db_user
settings.db_password
settings.db_host
settings.db_port
settings.db_name

para construir la URL de conexión:

postgresql+psycopg://usuario:contraseña@host:puerto/base_de_datos

Por lo tanto, la relación entre ambos archivos es:

.env
 │
 ▼
Settings
 │
 ▼
settings
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
13. Separación de responsabilidades

Es importante mantener separadas las responsabilidades.

settings.py

Se ocupa de:

Configuración
database.py

Se ocupa de:

Conexión con la base de datos
docker-compose.yml

Se ocupa de:

Infraestructura de PostgreSQL
.env

Se ocupa de:

Valores específicos del entorno

Esta separación permite modificar la infraestructura o la configuración sin tener que modificar toda la aplicación.

14. Seguridad

Actualmente existen valores de desarrollo como:

DB_USER=postgres
DB_PASSWORD=postgres

Estos valores son adecuados únicamente para el entorno local actual.

No deben utilizarse como credenciales de producción.

La estrategia prevista es mantener:

.env

fuera del repositorio y proporcionar:

.env.example

como plantilla.

Por ejemplo:

DB_PASSWORD=change_me

en .env.example.

De esta manera, otros desarrolladores pueden conocer qué variables necesita el proyecto sin conocer las credenciales reales del entorno.

15. Verificación realizada

Se comprobó que la configuración carga correctamente:

python -c "from backend.app.config.settings import settings; print(settings.db_host); print(settings.db_port); print(settings.db_name); print(settings.db_user); print(settings.db_password)"

Resultado:

localhost
5432
medical_cms
postgres
postgres

También se verificaron los tipos de los valores.

Posteriormente, esta configuración fue utilizada para crear correctamente el engine de SQLAlchemy.

16. Problema detectado y corrección

Durante la integración inicial se produjo un error al importar database.py desde la raíz del proyecto:

ModuleNotFoundError: No module named 'app'

El motivo era el contexto desde el cual se ejecutaba Python.

El módulo utilizaba:

from app.config.settings import settings

Por lo tanto, cuando se trabaja directamente desde:

backend/

el paquete app queda disponible en el PYTHONPATH.

La prueba correcta se realizó desde:

medical-cms-platform/backend

mediante:

python -c "from app.database import engine; print(engine)"
17. Estado actual

El archivo settings.py ya permite centralizar:

Identidad de la aplicación.
Versión de la API.
Modo debug.
Host de PostgreSQL.
Puerto de PostgreSQL.
Nombre de la base de datos.
Usuario de PostgreSQL.
Contraseña de PostgreSQL.

La configuración fue probada junto con SQLAlchemy y PostgreSQL.

18. Próximo paso

El siguiente archivo a documentar dentro de este bloque es:

backend/app/database.py

Ese módulo será responsable de utilizar la configuración definida aquí para crear el engine de SQLAlchemy.

Posteriormente se podrá avanzar hacia la creación de sesiones de base de datos y su integración con FastAPI.

Resultado

El sistema de configuración del backend quedó preparado para centralizar los parámetros de la aplicación y de PostgreSQL.

La configuración se encuentra separada de la lógica de conexión y puede ser modificada mediante variables de entorno sin necesidad de cambiar directamente el código de la aplicación.

Estado: COMPLETADO