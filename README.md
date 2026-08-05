# Medical CMS Platform

> Plataforma SaaS para la gestión integral de clínicas, consultorios y profesionales de la salud.

---

# Estado del proyecto

>  **En desarrollo activo**

Este repositorio documenta el desarrollo completo de una plataforma SaaS enfocada en la administración de clínicas y consultorios médicos. El proyecto se desarrolla siguiendo una metodología incremental basada en **SCRUM**, documentando cada decisión técnica, cada sprint y la evolución de la arquitectura.

El objetivo es construir una aplicación escalable, mantenible y preparada para incorporar nuevas funcionalidades sin comprometer la calidad del software.

---

# Objetivos del proyecto

Medical CMS Platform tiene como finalidad centralizar la gestión administrativa y clínica de consultorios y centros médicos mediante una plataforma moderna, segura y modular.

Entre los objetivos principales se encuentran:

* Gestionar múltiples clínicas y consultorios desde una única plataforma.
* Administrar profesionales de distintas especialidades médicas.
* Gestionar pacientes e historias clínicas.
* Administrar agendas médicas y disponibilidad de profesionales.
* Permitir la reserva, reprogramación y cancelación de turnos.
* Gestionar pagos y finanzas.
* Integrar proveedores mediante APIs oficiales y, cuando sea estrictamente necesario y legalmente permitido, mediante procesos de scraping.
* Incorporar notificaciones por correo electrónico y WhatsApp.
* Mantener un diseño modular que facilite la incorporación de nuevas funcionalidades.

Además del producto en sí, este repositorio tiene un segundo objetivo: documentar de forma transparente el proceso completo de desarrollo para servir como material de aprendizaje y referencia profesional.

---

# Características principales

La plataforma estará compuesta por distintos módulos funcionales que trabajarán de forma integrada.

## Gestión de usuarios

* Autenticación mediante JWT.
* Contraseñas protegidas con bcrypt.
* Gestión de roles y permisos.
* Administración de múltiples clínicas.

## Gestión de pacientes

* Alta de pacientes.
* Actualización de datos.
* Historial de consultas.
* Información de contacto.
* Seguimiento clínico.

## Agenda médica

* Reserva de turnos.
* Reprogramación.
* Cancelaciones.
* Control de disponibilidad.
* Agenda por profesional.
* Agenda por consultorio.

## Historia clínica

* Registro histórico permanente.
* Formularios dinámicos según especialidad.
* Actualización de registros.
* Consulta de antecedentes clínicos.

## Finanzas

* Registro de ingresos.
* Registro de gastos.
* Costos operativos.
* Márgenes de rentabilidad.
* Reportes financieros.

## Inventario

* Gestión de insumos.
* Seguimiento de stock.
* Proveedores.
* Actualización de precios.

## Integraciones

* APIs oficiales de proveedores cuando estén disponibles.
* Procesos de scraping únicamente cuando no exista una API oficial y se verifique previamente que las condiciones de uso lo permiten.
* Integración con servicios de correo electrónico.
* Integración con WhatsApp Business para confirmaciones y notificaciones.
* Integración con pasarelas de pago para reservas y consultas.

## Arquitectura

El proyecto será desarrollado utilizando una arquitectura modular basada en FastAPI y SQLAlchemy, separando claramente las responsabilidades de cada componente para favorecer la mantenibilidad, escalabilidad y facilidad de aprendizaje.


# Infraestructura

## Docker

Utilizado para contenerizar los servicios del proyecto.

Objetivos:

* Mantener ambientes reproducibles.
* Facilitar instalación.
* Evitar problemas entre diferentes equipos.

---

## Docker Compose

Utilizado para administrar múltiples servicios.

Inicialmente gestionará:

* Backend.
* PostgreSQL.
* Servicios adicionales futuros.

---

# Seguridad

Tecnologías utilizadas:

## JWT

Sistema de autenticación basado en tokens.

Será utilizado para:

* Inicio de sesión.
* Autorización de usuarios.
* Protección de endpoints.

---

## bcrypt

Algoritmo utilizado para proteger contraseñas.

Las contraseñas nunca serán almacenadas en texto plano.

Proceso:

```
Contraseña usuario

        ↓

bcrypt

        ↓

Hash almacenado en PostgreSQL
```

---

# Estructura del proyecto

El repositorio seguirá una organización separada por responsabilidades:

```
medical-cms-platform/

├── backend/
│
├── frontend/
│
├── docs/
│
├── docker/
│
├── .github/
│
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
└── docker-compose.yml
```

---

## Backend

```
backend/

├── app/
│
├── tests/
│
├── requirements.txt
│
├── .env
│
└── Dockerfile
```

---

## Frontend

```
frontend/

├── login/
├── dashboard/
├── patients/
├── appointments/
├── medical-records/
├── finance/
├── inventory/
└── shared/
```

Cada módulo estará separado por funcionalidad para facilitar mantenimiento y crecimiento del sistema.

---

## Documentación

```
docs/

├── architecture/
├── setup/
├── learning/
├── decisions/
├── sprints/
└── technical-journal/
```

Esta documentación acompañará todo el ciclo de vida del proyecto.


# Resumen de módulos

| Módulo                 | Estado      |
| ---------------------- | ----------- |
| Autenticación          | Planificado |
| Usuarios               | Planificado |
| Clínicas               | Planificado |
| Profesionales          | Planificado |
| Pacientes              | Planificado |
| Agenda                 | Planificado |
| Historia clínica       | Planificado |
| Inventario             | Planificado |
| Finanzas               | Planificado |
| Pagos                  | Planificado |
| WhatsApp               | Planificado |
| Chatbot                | Planificado |
| Integraciones externas | Planificado |

```
```