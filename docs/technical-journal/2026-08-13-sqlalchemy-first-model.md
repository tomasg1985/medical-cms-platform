# Primer modelo SQLAlchemy y creación de la tabla `clinics`

**Fecha:** 2026-08-13
**Rama:** `develop`
**Proyecto:** Medical CMS Platform
**Bloque:** Configuración de base de datos y primer modelo SQLAlchemy

---

## 1. Contexto

Durante esta etapa del proyecto se continuó con la integración entre FastAPI, SQLAlchemy 2.0 y PostgreSQL.

El objetivo de este bloque fue crear el primer modelo real de la aplicación (`Clinic`), registrarlo correctamente en SQLAlchemy y comprobar que su estructura pudiera convertirse en una tabla real dentro de PostgreSQL.

Este bloque representa el primer recorrido completo:

```text
Modelo Python
    ↓
SQLAlchemy
    ↓
Base.metadata
    ↓
Engine
    ↓
PostgreSQL
    ↓
Tabla real

2. Situación inicial

El proyecto ya contaba con:

FastAPI funcionando.
PostgreSQL ejecutándose mediante Docker Compose.
SQLAlchemy instalado.
Psycopg 3 instalado.
Conexión comprobada contra PostgreSQL.
engine configurado.
SessionLocal configurado.
Dependencia get_db() creada.
Base creada para los modelos SQLAlchemy.

La conexión con PostgreSQL había sido comprobada mediante una consulta simple:

from app.database import engine
from sqlalchemy import text


connection = engine.connect()


print(
    connection.execute(
        text("SELECT 1")
    ).scalar()
)


connection.close()

Resultado:

1

Esto confirmó que SQLAlchemy podía conectarse correctamente a PostgreSQL.

3. Creación del primer modelo

Se creó el archivo:

backend/app/models/clinic.py

El modelo quedó definido de la siguiente manera:

from sqlalchemy.orm import Mapped, mapped_column


from app.database import Base




class Clinic(Base):
    __tablename__ = "clinics"


    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
4. Estructura del modelo
class Clinic(Base)
class Clinic(Base):

La clase Clinic representa un modelo de SQLAlchemy.

Hereda de Base, que es la clase base utilizada para nuestros modelos.

Esto permite que SQLAlchemy pueda interpretar Clinic como una entidad persistente de base de datos.

__tablename__
__tablename__ = "clinics"

Indica el nombre que tendrá la tabla correspondiente en PostgreSQL.

Por lo tanto:

Clase Python:
Clinic


Tabla PostgreSQL:
clinics
5. Uso de Mapped

Se utilizó la sintaxis moderna de SQLAlchemy 2.0:

Mapped[int]
Mapped[str]

Mapped pertenece a SQLAlchemy y se utiliza para indicar que un atributo de Python forma parte del mapeo entre el modelo y la base de datos.

Ejemplos:

id: Mapped[int]

indica que id contiene valores enteros.

Mientras que:

name: Mapped[str]

indica que name contiene texto.

Conceptualmente:

Python
   ↓
Mapped
   ↓
SQLAlchemy
   ↓
Columna de base de datos
6. Uso de mapped_column()

Se utilizó:

mapped_column()

para definir las características de las columnas.

Ejemplo:

id: Mapped[int] = mapped_column(primary_key=True)

y:

name: Mapped[str] = mapped_column(nullable=False)

Mapped indica el tipo y participación del atributo en el mapeo.

mapped_column() permite configurar las características de la columna.

7. Primary Key

La columna id fue definida como:

id: Mapped[int] = mapped_column(primary_key=True)

primary_key=True indica que id será la clave primaria de la tabla.

La clave primaria identifica de forma única cada registro.

Ejemplo conceptual:

clinics


id     name
----------------------
1      Clínica Central
2      Clínica Norte
3      Clínica Sur

Cada registro tendrá un id diferente.

8. nullable=False

La columna name fue definida como:

name: Mapped[str] = mapped_column(nullable=False)

nullable=False significa que la columna no puede quedar sin valor.

Ejemplo:

id     name
----------------------
1      Clínica Central
2      Clínica Norte
3      NULL              ❌

Una clínica debe tener un nombre.

9. unique=True

Durante el análisis de las restricciones se revisó también:

unique=True

Esta opción obliga a que los valores de una columna no se repitan.

No se aplicó a name porque dos clínicas podrían tener el mismo nombre.

Por ejemplo:

Clínica Central

podría existir en dos ciudades diferentes.

La decisión de utilizar unique=True debe depender del significado real del dato.

10. Registro del modelo en SQLAlchemy

Se utilizó:

backend/app/models/__init__.py

con:

from app.models.clinic import Clinic

El objetivo es importar los modelos para que SQLAlchemy los registre dentro de:

Base.metadata
11. Error de import circular

Al intentar inicializar la base de datos apareció el siguiente error:

ImportError: cannot import name 'Clinic'
from partially initialized module 'app.models'
(most likely due to a circular import)

El problema estaba en:

app/models/__init__.py

Se había escrito:

from app.models import Clinic

Esto generaba un ciclo de importación.

El recorrido era aproximadamente:

database_init.py
      ↓
app.models
      ↓
models/__init__.py
      ↓
app.models
      ↓
models/__init__.py
      ↓
Import circular
12. Solución del import circular

Se modificó:

app/models/__init__.py

para utilizar la ruta concreta del módulo:

from app.models.clinic import Clinic

El recorrido pasó a ser:

database_init.py
      ↓
app.models
      ↓
models/__init__.py
      ↓
models/clinic.py
      ↓
Clinic

Sin regresar nuevamente a app.models.

El problema quedó solucionado.

Concepto aprendido

Un import circular ocurre cuando dos módulos necesitan cargarse entre sí formando un ciclo.

Ejemplo simple:

A → B → A

En nuestro caso, el problema se produjo porque models/__init__.py intentaba importar nuevamente desde app.models.

13. Verificación del registro en Base.metadata

Se comprobó que SQLAlchemy reconociera la tabla:

python -c "from app.database import Base; from app.models.clinic import Clinic; print(Base.metadata.tables.keys())"

Resultado:

dict_keys(['clinics'])

Esto confirmó que Clinic había sido registrado correctamente en Base.metadata.

14. Verificación de las columnas conocidas por SQLAlchemy

Se comprobó la estructura conocida por SQLAlchemy:

python -c "from app.database import Base; from app.models.clinic import Clinic; table = Base.metadata.tables['clinics']; print(table.columns.keys())"

Resultado:

['id', 'name']

Esto confirmó que SQLAlchemy conocía la estructura:

clinics
├── id
└── name
15. Inicialización de la base de datos

Se creó:

backend/app/database_init.py

con:

from app.database import Base, engine
from app.models import Clinic




Base.metadata.create_all(bind=engine)

El propósito del archivo es inicializar las tablas definidas en los modelos.

16. Base.metadata.create_all()

La siguiente instrucción:

Base.metadata.create_all(bind=engine)

indica a SQLAlchemy que utilice el engine para crear las tablas conocidas por Base.metadata que todavía no existan en la base de datos.

Conceptualmente:

Base.metadata
      ↓
Tablas conocidas
      ↓
create_all()
      ↓
engine
      ↓
PostgreSQL

Importante:

create_all() no significa que SQLAlchemy borre las tablas existentes y las vuelva a crear cada vez.

Su objetivo es crear las tablas que no existen.

17. Ejecución de database_init.py

Se ejecutó:

python -c "import app.database_init"

Después de solucionar el import circular, el comando terminó sin errores.

Esto confirmó que:

El módulo pudo cargarse.
Clinic pudo importarse.
Base.metadata pudo utilizarse.
SQLAlchemy pudo utilizar el engine.
PostgreSQL pudo recibir la operación.
18. Verificación de la tabla en PostgreSQL

Se comprobó directamente qué tablas existen en PostgreSQL:

python -c "from sqlalchemy import inspect; from app.database import engine; inspector = inspect(engine); print(inspector.get_table_names())"

Resultado:

['clinics']

Esto confirmó que la tabla clinics existe realmente en PostgreSQL.

19. Verificación de las columnas reales

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
20. Correspondencia Python → PostgreSQL

El modelo Python:

id: Mapped[int] = mapped_column(primary_key=True)

terminó representándose en PostgreSQL como una columna:

id
INTEGER
NOT NULL
PRIMARY KEY
autoincrement=True

La columna:

name: Mapped[str] = mapped_column(nullable=False)

terminó representándose como:

name
VARCHAR
NOT NULL

Por lo tanto:

Python                     PostgreSQL


Mapped[int]        →       INTEGER


Mapped[str]        →       VARCHAR


nullable=False     →       NOT NULL


primary_key=True   →       PRIMARY KEY
21. Autoincrement de id

PostgreSQL creó una secuencia para generar automáticamente los valores del id.

En la inspección apareció:

nextval('clinics_id_seq'::regclass)

Esto permite generar valores consecutivos para la clave primaria.

Ejemplo conceptual:

1
2
3
4
5
...

El funcionamiento interno de nextval() y las secuencias de PostgreSQL no se profundizó todavía, ya que no es necesario para el objetivo actual.

22. Concepto de Base.metadata

Durante este bloque se introdujo el concepto de metadata.

Base.metadata contiene información sobre las tablas que SQLAlchemy conoce a partir de los modelos registrados.

En nuestro caso:

Base.metadata
└── clinics
    ├── id
    └── name

Esto permite que SQLAlchemy conozca la estructura que posteriormente puede utilizar para crear o manipular las tablas.

23. Diferencia entre modelo, metadata y tabla

Se estableció la siguiente distinción:

MODELO
↓
Clase Python que describe una entidad.


METADATA
↓
Información que SQLAlchemy tiene sobre la estructura de los modelos.


TABLA
↓
Estructura física existente en PostgreSQL.


REGISTROS
↓
Datos almacenados dentro de la tabla.

En este bloque se llegó desde el modelo hasta la tabla real:

Clinic
   ↓
Base.metadata
   ↓
clinics

Todavía no se trabajó con registros reales.

24. Estructura actual

Actualmente existe:

backend/
└── app/
    ├── database.py
    ├── database_init.py
    └── models/
        ├── __init__.py
        └── clinic.py

El modelo Clinic contiene actualmente:

from sqlalchemy.orm import Mapped, mapped_column


from app.database import Base




class Clinic(Base):
    __tablename__ = "clinics"


    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

Y PostgreSQL contiene la tabla:

clinics
├── id
└── name
25. Pruebas realizadas
Comprobar que Clinic existe
python -c "from app.models.clinic import Clinic; print(Clinic)"

Resultado:

<class 'app.models.clinic.Clinic'>
Comprobar que SQLAlchemy registra la tabla
python -c "from app.database import Base; from app.models.clinic import Clinic; print(Base.metadata.tables.keys())"

Resultado:

dict_keys(['clinics'])
Comprobar las columnas del modelo
python -c "from app.database import Base; from app.models.clinic import Clinic; table = Base.metadata.tables['clinics']; print(table.columns.keys())"

Resultado:

['id', 'name']
Crear las tablas
python -c "import app.database_init"

Resultado:

Sin errores.
Comprobar las tablas reales de PostgreSQL
python -c "from sqlalchemy import inspect; from app.database import engine; inspector = inspect(engine); print(inspector.get_table_names())"

Resultado:

['clinics']
Comprobar las columnas reales de PostgreSQL
python -c "from sqlalchemy import inspect; from app.database import engine; inspector = inspect(engine); print(inspector.get_columns('clinics'))"

Resultado:

id → INTEGER
name → VARCHAR
26. Aprendizajes del bloque

Durante este bloque se incorporaron los siguientes conceptos:

Modelo SQLAlchemy.
Herencia desde Base.
Mapped.
mapped_column().
Tipos int y str.
primary_key=True.
nullable=False.
unique=True.
Base.metadata.
Registro de modelos.
Importación de módulos.
Import circular.
Base.metadata.create_all().
Inspección de tablas mediante SQLAlchemy.
Diferencia entre modelo y tabla real.
Relación entre Python, SQLAlchemy y PostgreSQL.
27. Próximo paso

El siguiente objetivo será trabajar con Session.

Ya se había comprobado anteriormente que:

SessionLocal()

produce una instancia:

<class 'sqlalchemy.orm.session.Session'>

El próximo bloque utilizará esa sesión para realizar el primer ciclo real de persistencia:

Crear objeto Clinic
       ↓
Agregarlo a Session
       ↓
Commit
       ↓
PostgreSQL
       ↓
Consultar el registro

Ejemplo conceptual:

Clinic
name = "Clínica Central"
       ↓
INSERT
       ↓
clinics

No se agregarán todavía más modelos ni relaciones hasta comprender correctamente este ciclo.

28. Estado del bloque

Estado: COMPLETADO

Se logró crear y verificar el primer modelo SQLAlchemy y su correspondiente tabla real en PostgreSQL.

El proyecto ya cuenta con el primer recorrido completo entre:

Python
  ↓
SQLAlchemy
  ↓
PostgreSQL

El siguiente bloque comenzará con la creación y persistencia del primer registro utilizando Session.

2. Situación inicial

El proyecto ya contaba con:

FastAPI funcionando.
PostgreSQL ejecutándose mediante Docker Compose.
SQLAlchemy instalado.
Psycopg 3 instalado.
Conexión comprobada contra PostgreSQL.
engine configurado.
SessionLocal configurado.
Dependencia get_db() creada.
Base creada para los modelos SQLAlchemy.

La conexión con PostgreSQL había sido comprobada mediante una consulta simple:

from app.database import engine
from sqlalchemy import text


connection = engine.connect()


print(
    connection.execute(
        text("SELECT 1")
    ).scalar()
)


connection.close()

Resultado:

1

Esto confirmó que SQLAlchemy podía conectarse correctamente a PostgreSQL.

3. Creación del primer modelo

Se creó el archivo:

backend/app/models/clinic.py

El modelo quedó definido de la siguiente manera:

from sqlalchemy.orm import Mapped, mapped_column


from app.database import Base




class Clinic(Base):
    __tablename__ = "clinics"


    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
4. Estructura del modelo
class Clinic(Base)
class Clinic(Base):

La clase Clinic representa un modelo de SQLAlchemy.

Hereda de Base, que es la clase base utilizada para nuestros modelos.

Esto permite que SQLAlchemy pueda interpretar Clinic como una entidad persistente de base de datos.

__tablename__
__tablename__ = "clinics"

Indica el nombre que tendrá la tabla correspondiente en PostgreSQL.

Por lo tanto:

Clase Python:
Clinic


Tabla PostgreSQL:
clinics
5. Uso de Mapped

Se utilizó la sintaxis moderna de SQLAlchemy 2.0:

Mapped[int]
Mapped[str]

Mapped pertenece a SQLAlchemy y se utiliza para indicar que un atributo de Python forma parte del mapeo entre el modelo y la base de datos.

Ejemplos:

id: Mapped[int]

indica que id contiene valores enteros.

Mientras que:

name: Mapped[str]

indica que name contiene texto.

Conceptualmente:

Python
   ↓
Mapped
   ↓
SQLAlchemy
   ↓
Columna de base de datos
6. Uso de mapped_column()

Se utilizó:

mapped_column()

para definir las características de las columnas.

Ejemplo:

id: Mapped[int] = mapped_column(primary_key=True)

y:

name: Mapped[str] = mapped_column(nullable=False)

Mapped indica el tipo y participación del atributo en el mapeo.

mapped_column() permite configurar las características de la columna.

7. Primary Key

La columna id fue definida como:

id: Mapped[int] = mapped_column(primary_key=True)

primary_key=True indica que id será la clave primaria de la tabla.

La clave primaria identifica de forma única cada registro.

Ejemplo conceptual:

clinics


id     name
----------------------
1      Clínica Central
2      Clínica Norte
3      Clínica Sur

Cada registro tendrá un id diferente.

8. nullable=False

La columna name fue definida como:

name: Mapped[str] = mapped_column(nullable=False)

nullable=False significa que la columna no puede quedar sin valor.

Ejemplo:

id     name
----------------------
1      Clínica Central
2      Clínica Norte
3      NULL              ❌

Una clínica debe tener un nombre.

9. unique=True

Durante el análisis de las restricciones se revisó también:

unique=True

Esta opción obliga a que los valores de una columna no se repitan.

No se aplicó a name porque dos clínicas podrían tener el mismo nombre.

Por ejemplo:

Clínica Central

podría existir en dos ciudades diferentes.

La decisión de utilizar unique=True debe depender del significado real del dato.

10. Registro del modelo en SQLAlchemy

Se utilizó:

backend/app/models/__init__.py

con:

from app.models.clinic import Clinic

El objetivo es importar los modelos para que SQLAlchemy los registre dentro de:

Base.metadata
11. Error de import circular

Al intentar inicializar la base de datos apareció el siguiente error:

ImportError: cannot import name 'Clinic'
from partially initialized module 'app.models'
(most likely due to a circular import)

El problema estaba en:

app/models/__init__.py

Se había escrito:

from app.models import Clinic

Esto generaba un ciclo de importación.

El recorrido era aproximadamente:

database_init.py
      ↓
app.models
      ↓
models/__init__.py
      ↓
app.models
      ↓
models/__init__.py
      ↓
Import circular
12. Solución del import circular

Se modificó:

app/models/__init__.py

para utilizar la ruta concreta del módulo:

from app.models.clinic import Clinic

El recorrido pasó a ser:

database_init.py
      ↓
app.models
      ↓
models/__init__.py
      ↓
models/clinic.py
      ↓
Clinic

Sin regresar nuevamente a app.models.

El problema quedó solucionado.

Concepto aprendido

Un import circular ocurre cuando dos módulos necesitan cargarse entre sí formando un ciclo.

Ejemplo simple:

A → B → A

En nuestro caso, el problema se produjo porque models/__init__.py intentaba importar nuevamente desde app.models.

13. Verificación del registro en Base.metadata

Se comprobó que SQLAlchemy reconociera la tabla:

python -c "from app.database import Base; from app.models.clinic import Clinic; print(Base.metadata.tables.keys())"

Resultado:

dict_keys(['clinics'])

Esto confirmó que Clinic había sido registrado correctamente en Base.metadata.

14. Verificación de las columnas conocidas por SQLAlchemy

Se comprobó la estructura conocida por SQLAlchemy:

python -c "from app.database import Base; from app.models.clinic import Clinic; table = Base.metadata.tables['clinics']; print(table.columns.keys())"

Resultado:

['id', 'name']

Esto confirmó que SQLAlchemy conocía la estructura:

clinics
├── id
└── name
15. Inicialización de la base de datos

Se creó:

backend/app/database_init.py

con:

from app.database import Base, engine
from app.models import Clinic




Base.metadata.create_all(bind=engine)

El propósito del archivo es inicializar las tablas definidas en los modelos.

16. Base.metadata.create_all()

La siguiente instrucción:

Base.metadata.create_all(bind=engine)

indica a SQLAlchemy que utilice el engine para crear las tablas conocidas por Base.metadata que todavía no existan en la base de datos.

Conceptualmente:

Base.metadata
      ↓
Tablas conocidas
      ↓
create_all()
      ↓
engine
      ↓
PostgreSQL

Importante:

create_all() no significa que SQLAlchemy borre las tablas existentes y las vuelva a crear cada vez.

Su objetivo es crear las tablas que no existen.

17. Ejecución de database_init.py

Se ejecutó:

python -c "import app.database_init"

Después de solucionar el import circular, el comando terminó sin errores.

Esto confirmó que:

El módulo pudo cargarse.
Clinic pudo importarse.
Base.metadata pudo utilizarse.
SQLAlchemy pudo utilizar el engine.
PostgreSQL pudo recibir la operación.
18. Verificación de la tabla en PostgreSQL

Se comprobó directamente qué tablas existen en PostgreSQL:

python -c "from sqlalchemy import inspect; from app.database import engine; inspector = inspect(engine); print(inspector.get_table_names())"

Resultado:

['clinics']

Esto confirmó que la tabla clinics existe realmente en PostgreSQL.

19. Verificación de las columnas reales

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
20. Correspondencia Python → PostgreSQL

El modelo Python:

id: Mapped[int] = mapped_column(primary_key=True)

terminó representándose en PostgreSQL como una columna:

id
INTEGER
NOT NULL
PRIMARY KEY
autoincrement=True

La columna:

name: Mapped[str] = mapped_column(nullable=False)

terminó representándose como:

name
VARCHAR
NOT NULL

Por lo tanto:

Python                     PostgreSQL


Mapped[int]        →       INTEGER


Mapped[str]        →       VARCHAR


nullable=False     →       NOT NULL


primary_key=True   →       PRIMARY KEY
21. Autoincrement de id

PostgreSQL creó una secuencia para generar automáticamente los valores del id.

En la inspección apareció:

nextval('clinics_id_seq'::regclass)

Esto permite generar valores consecutivos para la clave primaria.

Ejemplo conceptual:

1
2
3
4
5
...

El funcionamiento interno de nextval() y las secuencias de PostgreSQL no se profundizó todavía, ya que no es necesario para el objetivo actual.

22. Concepto de Base.metadata

Durante este bloque se introdujo el concepto de metadata.

Base.metadata contiene información sobre las tablas que SQLAlchemy conoce a partir de los modelos registrados.

En nuestro caso:

Base.metadata
└── clinics
    ├── id
    └── name

Esto permite que SQLAlchemy conozca la estructura que posteriormente puede utilizar para crear o manipular las tablas.

23. Diferencia entre modelo, metadata y tabla

Se estableció la siguiente distinción:

MODELO
↓
Clase Python que describe una entidad.


METADATA
↓
Información que SQLAlchemy tiene sobre la estructura de los modelos.


TABLA
↓
Estructura física existente en PostgreSQL.


REGISTROS
↓
Datos almacenados dentro de la tabla.

En este bloque se llegó desde el modelo hasta la tabla real:

Clinic
   ↓
Base.metadata
   ↓
clinics

Todavía no se trabajó con registros reales.

24. Estructura actual

Actualmente existe:

backend/
└── app/
    ├── database.py
    ├── database_init.py
    └── models/
        ├── __init__.py
        └── clinic.py

El modelo Clinic contiene actualmente:

from sqlalchemy.orm import Mapped, mapped_column


from app.database import Base




class Clinic(Base):
    __tablename__ = "clinics"


    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

Y PostgreSQL contiene la tabla:

clinics
├── id
└── name
25. Pruebas realizadas
Comprobar que Clinic existe
python -c "from app.models.clinic import Clinic; print(Clinic)"

Resultado:

<class 'app.models.clinic.Clinic'>
Comprobar que SQLAlchemy registra la tabla
python -c "from app.database import Base; from app.models.clinic import Clinic; print(Base.metadata.tables.keys())"

Resultado:

dict_keys(['clinics'])
Comprobar las columnas del modelo
python -c "from app.database import Base; from app.models.clinic import Clinic; table = Base.metadata.tables['clinics']; print(table.columns.keys())"

Resultado:

['id', 'name']
Crear las tablas
python -c "import app.database_init"

Resultado:

Sin errores.
Comprobar las tablas reales de PostgreSQL
python -c "from sqlalchemy import inspect; from app.database import engine; inspector = inspect(engine); print(inspector.get_table_names())"

Resultado:

['clinics']
Comprobar las columnas reales de PostgreSQL
python -c "from sqlalchemy import inspect; from app.database import engine; inspector = inspect(engine); print(inspector.get_columns('clinics'))"

Resultado:

id → INTEGER
name → VARCHAR
26. Aprendizajes del bloque

Durante este bloque se incorporaron los siguientes conceptos:

Modelo SQLAlchemy.
Herencia desde Base.
Mapped.
mapped_column().
Tipos int y str.
primary_key=True.
nullable=False.
unique=True.
Base.metadata.
Registro de modelos.
Importación de módulos.
Import circular.
Base.metadata.create_all().
Inspección de tablas mediante SQLAlchemy.
Diferencia entre modelo y tabla real.
Relación entre Python, SQLAlchemy y PostgreSQL.
27. Próximo paso

El siguiente objetivo será trabajar con Session.

Ya se había comprobado anteriormente que:

SessionLocal()

produce una instancia:

<class 'sqlalchemy.orm.session.Session'>

El próximo bloque utilizará esa sesión para realizar el primer ciclo real de persistencia:

Crear objeto Clinic
       ↓
Agregarlo a Session
       ↓
Commit
       ↓
PostgreSQL
       ↓
Consultar el registro

Ejemplo conceptual:

Clinic
name = "Clínica Central"
       ↓
INSERT
       ↓
clinics

No se agregarán todavía más modelos ni relaciones hasta comprender correctamente este ciclo.

28. Estado del bloque

Estado: COMPLETADO

Se logró crear y verificar el primer modelo SQLAlchemy y su correspondiente tabla real en PostgreSQL.

El proyecto ya cuenta con el primer recorrido completo entre:

Python
  ↓
SQLAlchemy
  ↓
PostgreSQL

El siguiente bloque comenzará con la creación y persistencia del primer registro utilizando Session.