# Medical CMS Platform

> Plataforma SaaS modular para la gestión integral de clínicas, consultorios y profesionales de la salud.

---

# Estado del proyecto

> **En desarrollo activo — Backend en construcción**

Medical CMS Platform es una plataforma SaaS orientada inicialmente al mercado argentino para la gestión de clínicas, consultorios y profesionales de la salud.

El proyecto se desarrolla de forma incremental, priorizando:

- Diseño correcto del modelo de datos.
- Separación clara de responsabilidades.
- Arquitectura modular.
- Escalabilidad y mantenibilidad.
- Pruebas y verificaciones durante el desarrollo.
- Documentación de las decisiones técnicas.
- Aprendizaje aplicado directamente sobre el proyecto.

Actualmente se completó una primera etapa importante del **bloque de modelos de datos** y se comenzó la preparación de la capa de **schemas**, que será seguida por repositories y services.

---

# Objetivos del proyecto

Medical CMS Platform busca centralizar la gestión administrativa y clínica de múltiples clínicas y consultorios desde una única plataforma.

Objetivos principales:

- Gestionar múltiples clínicas y consultorios.
- Administrar profesionales de diferentes especialidades.
- Gestionar pacientes.
- Administrar usuarios y acceso al sistema.
- Implementar roles y permisos mediante RBAC.
- Gestionar agendas y disponibilidad profesional.
- Administrar turnos.
- Incorporar historias clínicas.
- Gestionar pagos y finanzas.
- Gestionar inventario e insumos.
- Incorporar notificaciones.
- Integrar servicios externos mediante APIs oficiales cuando estén disponibles.
- Mantener una arquitectura preparada para crecimiento futuro.

El repositorio también documenta el proceso de desarrollo como material de aprendizaje y referencia técnica.

---

# Stack tecnológico actual

## Backend

- **Python**
- **FastAPI**
- **SQLAlchemy 2.0**
- **Psycopg 3**
- **Pydantic**
- **Alembic**

## Base de datos

- **PostgreSQL 17**

## Infraestructura

- **Docker**
- **Docker Compose**

## Frontend

Se encuentra planificado como una aplicación separada utilizando:

- HTML5
- CSS3
- JavaScript

No se incorporan cambios de stack sin evaluar previamente su necesidad y compatibilidad con el proyecto.

---

# Arquitectura actual

El backend utiliza una arquitectura modular basada en separación de responsabilidades.

Conceptualmente:

```text
Cliente
   │
   ▼
Routes / API
   │
   ▼
Schemas
   │
   ▼
Services
   │
   ▼
Repositories
   │
   ▼
SQLAlchemy Models
   │
   ▼
PostgreSQL
```

Responsabilidades principales:

### Routes / API

Reciben las solicitudes HTTP y exponen los endpoints de la aplicación.

### Schemas

Definen la estructura de entrada y salida de datos mediante Pydantic.

### Services

Contendrán la lógica de negocio.

### Repositories

Centralizan las operaciones de acceso a datos.

### Models

Representan las entidades y relaciones de la base de datos mediante SQLAlchemy.

### Alembic

Gestiona las migraciones de estructura de la base de datos.

---

# Estado actual del backend

La aplicación base de FastAPI se encuentra funcionando.

Se verificó previamente:

- Inicio mediante Uvicorn.
- Conexión con PostgreSQL.
- Ejecución de consultas mediante SQLAlchemy.
- Inicialización de tablas.
- Funcionamiento de Alembic.
- Organización modular del backend.

El endpoint raíz responde actualmente como API funcional.

---

# Base de datos

Base de datos utilizada durante el desarrollo:

```text
medical_cms
```

Motor:

```text
PostgreSQL 17
```

La conexión se realiza mediante SQLAlchemy utilizando Psycopg 3.

Ejemplo de URL utilizada durante las pruebas:

```text
postgresql+psycopg://...@localhost:5432/medical_cms
```

Las credenciales se mantienen fuera del repositorio mediante variables de entorno.

---

# Modelos implementados

El bloque de modelos actualmente desarrollado incluye las entidades principales y sus relaciones.

## Clinic

Representa una clínica o centro médico.

Relaciones actuales:

- Profesionales.
- Pacientes.
- Especialidades.
- Turnos.
- Disponibilidad profesional.
- Usuarios mediante relación muchos-a-muchos.

Tabla:

```text
clinics
```

---

## Patient

Representa a un paciente.

Datos principales:

- Nombre.
- Apellido.
- Fecha de nacimiento.
- DNI.
- Email.
- Teléfono.
- Dirección.
- Obra social / seguro.

Relaciones actuales:

- Clínicas.
- Turnos.
- Usuario asociado opcionalmente.

Tabla:

```text
patients
```

La asociación con `User` utiliza `user_id` nullable y único, permitiendo que un paciente exista sin una cuenta de acceso.

---

## Professional

Representa a un profesional de la salud.

Datos principales:

- Nombre.
- Apellido.
- Género.
- Fecha de nacimiento.
- Teléfono.
- Email.
- Matrícula / credential.
- Vencimiento de matrícula.
- DNI.
- Dirección.
- Institución médica.
- Obra social / seguro de trabajo.

Relaciones actuales:

- Clínicas.
- Especialidades.
- Turnos.
- Disponibilidad.
- Usuario asociado opcionalmente.

Tabla:

```text
professionals
```

La asociación con `User` utiliza `user_id` nullable y único.

---

## Specialty

Representa una especialidad médica.

Datos principales:

- Nombre oficial.
- Nombre alternativo.
- Descripción.
- Código SNOMED.
- Ejercicio profesional.

Relaciones:

- Clínicas.
- Profesionales.
- Turnos.
- Disponibilidad.

Tabla:

```text
specialties
```

---

## Appointment

Representa un turno médico.

Incluye actualmente:

- Código de reserva.
- Fecha.
- Hora.
- Duración.
- Modalidad.
- Estado.
- Motivo de consulta.
- Motivo de cancelación.
- Importe abonado.
- Estado del pago.
- Clínica.
- Paciente.
- Profesional.
- Especialidad.
- Disponibilidad asociada.

Tabla:

```text
appointments
```

---

## ScheduleAvailability

Representa la disponibilidad de un profesional para una clínica y especialidad.

Incluye:

- Día de la semana.
- Hora de inicio.
- Hora de finalización.
- Duración de consulta.
- Vigencia.
- Estado de actividad.
- Profesional.
- Clínica.
- Especialidad.

Tabla:

```text
schedule_availability
```

---

# Sistema de usuarios y RBAC

Se incorporó el primer bloque de control de acceso basado en **RBAC (Role-Based Access Control)**.

La decisión actual es separar:

```text
User
    ↓
Cuenta / acceso al sistema
```

de:

```text
Patient
Professional
    ↓
Datos clínicos o profesionales
```

Esto permite que la identidad de acceso no sea responsable de almacenar directamente la información clínica o profesional.

---

# User

Representa una cuenta de usuario del sistema.

Campos actuales:

- `id`
- `email`
- `is_active`
- `created_at`
- `updated_at`

Tabla:

```text
users
```

Relaciones actuales:

- Professional — uno a uno.
- Patient — uno a uno.
- Clinic — muchos a muchos.
- Role — muchos a muchos.

> La autenticación completa todavía no está implementada.

---

# Role

Representa un rol dentro del sistema.

Campos:

- `id`
- `name`
- `description`
- `is_active`
- `created_at`
- `updated_at`

Tabla:

```text
roles
```

Relaciones:

- Users — muchos a muchos.
- Permissions — muchos a muchos.

---

# Permission

Representa un permiso específico.

Campos:

- `id`
- `name`
- `description`
- `resource`
- `action`
- `is_active`
- `created_at`
- `updated_at`

Tabla:

```text
permissions
```

Relaciones:

- Roles — muchos a muchos.

---

# Tablas intermedias RBAC

## user_roles

Relaciona usuarios con roles.

Clave primaria compuesta:

```text
user_id
role_id
```

Relación:

```text
User N ─── N Role
```

---

## role_permissions

Relaciona roles con permisos.

Clave primaria compuesta:

```text
role_id
permission_id
```

Relación:

```text
Role N ─── N Permission
```

---

## user_clinics

Relaciona usuarios con clínicas.

Clave primaria compuesta:

```text
user_id
clinic_id
```

Relación:

```text
User N ─── N Clinic
```

Esto permite que una cuenta pueda tener acceso a múltiples clínicas.

---

# Relaciones principales

El modelo actual contempla, entre otras, las siguientes relaciones:

```text
Clinic N ─── N Professional
Clinic N ─── N Patient
Clinic N ─── N Specialty
Clinic N ─── N User

Professional N ─── N Specialty

Professional 1 ─── N ScheduleAvailability
Clinic       1 ─── N ScheduleAvailability
Specialty    1 ─── N ScheduleAvailability

Clinic       1 ─── N Appointment
Patient      1 ─── N Appointment
Professional 1 ─── N Appointment
Specialty    1 ─── N Appointment
ScheduleAvailability 1 ─── N Appointment

User 1 ─── 0..1 Professional
User 1 ─── 0..1 Patient

User N ─── N Role
Role N ─── N Permission
```

Las relaciones y cardinalidades fueron revisadas antes de continuar con la implementación de las capas superiores.

---

# Migraciones

Alembic está incorporado al proyecto para controlar la evolución de la estructura de PostgreSQL.

Una de las migraciones más recientes incorpora:

```text
420c6cc931ec_add_users_roles_and_permissions.py
```

Esta migración agrega:

- `users`
- `roles`
- `permissions`
- `user_roles`
- `role_permissions`
- `user_clinics`
- `patients.user_id`
- `professionals.user_id`

También contiene el cambio correspondiente de `appointments.consulting_reason` a `NOT NULL`.

---

# Schemas

La capa de schemas se encuentra actualmente en construcción.

Schemas existentes o incorporados durante esta etapa:

```text
appointment_schema.py
clinic_schema.py
clinic_specialty_schema.py
patient_schema.py
patient_clinic_schema.py
professional_schema.py
professional_specialty_schema.py
schedule_availability_schema.py
specialty_schema.py
user_schema.py
user_clinic_schema.py
user_role_schema.py
role_schema.py
permission_schema.py
role_permission_schema.py
```

## Principales patrones utilizados

### Create

Define los datos necesarios para crear una entidad.

### Update

Define los campos que pueden modificarse, normalmente como opcionales.

### Response

Define los datos devueltos por la API.

### Summary

Define representaciones reducidas utilizadas para relaciones anidadas.

Por ejemplo:

```text
ClinicResponse
 ├── ProfessionalSummary
 ├── PatientSummary
 └── UserSummary
```

y:

```text
ProfessionalResponse
 ├── SpecialtyResponse
 ├── ClinicResponse
 └── UserSummary
```

Los schemas de respuesta utilizan:

```python
model_config = {
    "from_attributes": True
}
```

para permitir su construcción a partir de objetos SQLAlchemy.

---

# Repositories

La capa de repositories ya contiene implementaciones para varias entidades existentes.

Actualmente se encuentran:

```text
appointment_repository.py
clinic_repository.py
clinic_specialty_repository.py
patient_clinics_repository.py
patient_repository.py
professional_clinic_repository.py
professional_repository.py
professional_specialty_repository.py
schedule_avilability_repository.py
specialty_repository.py
```

La siguiente etapa consiste en revisar estos repositories y crear o ajustar los correspondientes al bloque de usuarios y RBAC.

Pendientes principales:

```text
user_repository.py
role_repository.py
permission_repository.py
user_clinic_repository.py
user_role_repository.py
role_permission_repository.py
```

Los nombres definitivos deberán mantenerse consistentes con la estructura actual del proyecto.

---

# Services

La capa de services ya contiene lógica para varias entidades.

Actualmente:

```text
appointment_service.py
clinic_service.py
clinic_specialty_service.py
patient_clinic_service.py
patient_service.py
professional_service.py
professional_specialty_service.py
specialty_service.py
```

La siguiente etapa consiste en revisar y completar los services relacionados con:

```text
User
Role
Permission
UserClinic
UserRole
RolePermission
```

La lógica de negocio debe permanecer en services y no mezclarse directamente con routes o repositories.

---

# API y rutas

El proyecto ya dispone de rutas para las entidades desarrolladas previamente.

El objetivo arquitectónico es mantener:

```text
Route
   ↓
Service
   ↓
Repository
   ↓
Model
```

Las rutas no deberían concentrar lógica de negocio.

El bloque RBAC todavía debe avanzar por las capas de repository, service y posteriormente routes/endpoints.

---

# Seguridad

## Estado actual

La autenticación completa todavía está pendiente.

Está previsto incorporar:

- JWT.
- Hash seguro de contraseñas.
- Autorización basada en roles y permisos.
- Protección de endpoints.
- Control de acceso por clínica.

La decisión actual es **no implementar Auth0 por el momento**.

El modelo `User` se está preparando para soportar posteriormente el sistema de autenticación propio de la aplicación.

---

# Docker

Docker forma parte de la infraestructura del proyecto.

Actualmente se utiliza PostgreSQL mediante Docker Compose.

Servicio principal:

```text
PostgreSQL 17
```

Puerto utilizado durante el desarrollo:

```text
5432
```

La contenerización permite mantener un entorno reproducible entre desarrolladores.

---

# Estructura del repositorio

La estructura general del proyecto contempla:

```text
medical-cms-platform/

├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── config/
│   │   ├── core/
│   │   ├── database/
│   │   ├── dependencies/
│   │   ├── middleware/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── security/
│   │   ├── services/
│   │   └── utils/
│   │
│   ├── alembic/
│   │   └── versions/
│   │
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│
├── docs/
│   ├── architecture/
│   ├── decisions/
│   ├── history/
│   ├── learning/
│   ├── product/
│   ├── roadmap/
│   └── technical-journal/
│
├── .github/
│
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
└── docker-compose.yml
```

La estructura puede evolucionar durante el desarrollo, pero se mantiene el principio de separación de responsabilidades.

---

# Módulos del sistema

| Módulo | Estado |
|---|---|
| Infraestructura Docker | Implementado |
| PostgreSQL | Implementado |
| FastAPI | Implementado |
| SQLAlchemy | Implementado |
| Alembic | Implementado |
| Clinic | Modelo + schemas + repository + service |
| Patient | Modelo + schemas + repository + service |
| Professional | Modelo + schemas + repository + service |
| Specialty | Modelo + schemas + repository + service |
| Appointment | Modelo + schemas + repository + service |
| Schedule Availability | Modelo + schema + repository/service en revisión |
| Professional-Specialty | Modelo + schemas + repository + service |
| Clinic-Specialty | Modelo + schemas + repository + service |
| User | Modelo + schema |
| User-Clinic | Modelo + schema |
| Role | Modelo + schema |
| Permission | Modelo + schema |
| User-Role | Modelo + schema |
| Role-Permission | Modelo + schema |
| Repositories RBAC | Pendiente |
| Services RBAC | Pendiente |
| Routes RBAC | Pendiente |
| Autenticación | Pendiente |
| JWT | Pendiente |
| Hash de contraseñas | Pendiente |
| Autorización RBAC | Pendiente |
| Historias clínicas | Pendiente |
| Finanzas | Pendiente |
| Inventario | Pendiente |
| Pagos | Pendiente |
| Notificaciones | Pendiente |
| WhatsApp Business | Pendiente |
| Integraciones externas | Pendiente |
| Frontend | Pendiente |

---

# Próxima etapa de desarrollo

Con el bloque de modelos incorporado al repositorio, el desarrollo continúa con la capa de acceso y lógica de negocio.

Orden previsto:

```text
1. Revisión de schemas
        ↓
2. Repositories
        ↓
3. Services
        ↓
4. Routes / endpoints
        ↓
5. Pruebas
        ↓
6. Correcciones
        ↓
7. Commit y push
```

Para el bloque RBAC:

```text
User
Role
Permission
UserClinic
UserRole
RolePermission
        │
        ▼
Schemas
        │
        ▼
Repositories
        │
        ▼
Services
        │
        ▼
Routes
        │
        ▼
Autorización
```

---

# Control de versiones

El desarrollo se realiza principalmente sobre la rama:

```text
develop
```

La rama:

```text
main
```

se mantiene como rama estable.

Se utilizan commits siguiendo una convención basada en Conventional Commits.

Ejemplo reciente:

```text
feat: Se agregaron los modelos RBAC de usuarios, roles y permisos
```

El bloque de modelos RBAC fue incorporado mediante el commit:

```text
ff42d
```

---

# Metodología de desarrollo

El proyecto utiliza una metodología incremental inspirada en SCRUM.

Cada etapa intenta seguir este ciclo:

```text
Analizar
   ↓
Diseñar
   ↓
Implementar
   ↓
Verificar
   ↓
Corregir
   ↓
Documentar
   ↓
Commit
```

La documentación del proyecto se mantiene como parte del desarrollo y no como una actividad posterior.

---

# Próximos módulos funcionales

Una vez consolidada la arquitectura base, se prevé avanzar progresivamente hacia:

## Gestión de usuarios

- Registro.
- Inicio de sesión.
- Gestión de cuentas.
- Roles.
- Permisos.
- Acceso por clínica.

## Gestión de pacientes

- Alta y actualización.
- Información clínica.
- Historial.
- Asociación con centros.

## Agenda

- Disponibilidad.
- Reservas.
- Reprogramaciones.
- Cancelaciones.
- Agenda por profesional.
- Agenda por clínica.

## Historia clínica

- Evolución clínica.
- Antecedentes.
- Registros por especialidad.
- Formularios específicos.

## Finanzas

- Pagos.
- Ingresos.
- Gastos.
- Reportes.

## Inventario

- Insumos.
- Stock.
- Proveedores.
- Movimientos.

## Integraciones

- Correo electrónico.
- WhatsApp Business.
- Pasarelas de pago.
- APIs externas.

---

# Principios del proyecto

El desarrollo mantiene los siguientes principios:

1. **Separación de responsabilidades.**
2. **Modelado explícito de relaciones.**
3. **Migraciones controladas mediante Alembic.**
4. **Validación mediante Pydantic.**
5. **Lógica de negocio en Services.**
6. **Acceso a datos en Repositories.**
7. **API desacoplada de la persistencia.**
8. **Seguridad como parte de la arquitectura.**
9. **Documentación continua.**
10. **Cambios pequeños y verificables.**
11. **No incorporar tecnologías innecesarias sin evaluación previa.**
12. **Mantener el código comprensible y mantenible.**

---

# Estado general

Actualmente el proyecto pasó de la etapa inicial de infraestructura y modelos básicos a una etapa de consolidación de la arquitectura de aplicación.

El bloque de entidades principales ya incluye:

```text
Clinic
Patient
Professional
Specialty
Appointment
ScheduleAvailability
User
Role
Permission
```

y sus principales tablas de asociación.

El siguiente objetivo técnico es completar las capas:

```text
Schemas
Repositories
Services
Routes
Tests
```

comenzando por el bloque de usuarios y RBAC y manteniendo la misma arquitectura para los módulos siguientes.

---

# Licencia

Proyecto en desarrollo.

La licencia definitiva será definida antes de la publicación de una versión estable.
