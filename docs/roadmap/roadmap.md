# Roadmap del proyecto

El desarrollo de Medical CMS Platform será realizado mediante una metodología incremental basada en **SCRUM**, organizando el trabajo en épicas y sprints.

Cada sprint tendrá:

* Objetivo principal.
* Historias de usuario.
* Tareas técnicas.
* Criterios de aceptación.
* Documentación asociada.
* Revisión del incremento desarrollado.

El objetivo es construir progresivamente una plataforma funcional, manteniendo una arquitectura limpia y documentada.

---

# Épicas principales del proyecto

Las funcionalidades serán agrupadas en grandes bloques de trabajo.

---

# Épica 1 — Fundamentos del proyecto

Objetivo:

Preparar la base técnica y organizativa del sistema.

Incluye:

* Configuración del repositorio.
* Arquitectura inicial.
* Entorno de desarrollo.
* Docker.
* Documentación.
* Convenciones de código.

Estado:

🟡 En desarrollo

---

# Épica 2 — Autenticación y seguridad

Objetivo:

Crear el sistema de acceso seguro a la plataforma.

Incluye:

* Usuarios.
* Roles.
* Login.
* JWT.
* Hashing de contraseñas.
* Protección de endpoints.

Estado:

Pendiente

---

# Épica 3 — Gestión de clínicas y profesionales

Objetivo:

Permitir administrar organizaciones médicas y sus profesionales.

Incluye:

* Clínicas.
* Consultorios.
* Especialidades.
* Profesionales.
* Horarios.

Estado:

Pendiente

---

# Épica 4 — Gestión de pacientes

Objetivo:

Crear el núcleo de información del paciente.

Incluye:

* Registro.
* Actualización.
* Búsqueda.
* Datos personales.
* Historial básico.

Estado:

Pendiente

---

# Épica 5 — Sistema de agenda médica

Objetivo:

Desarrollar la gestión completa de turnos.

Incluye:

* Disponibilidad.
* Reserva.
* Confirmación.
* Reprogramación.
* Cancelación.
* Agenda diaria.

Estado:

Pendiente

---

# Épica 6 — Historia clínica electrónica

Objetivo:

Crear un sistema de registro médico seguro y trazable.

Incluye:

* Historias clínicas.
* Evoluciones.
* Diagnósticos.
* Tratamientos.
* Formularios dinámicos por especialidad.

Estado:

Pendiente

---

# Épica 7 — Inventario y proveedores

Objetivo:

Gestionar insumos médicos y odontológicos.

Incluye:

* Productos.
* Stock.
* Proveedores.
* Precios.
* Integraciones externas.

Estado:

Pendiente

---

# Épica 8 — Finanzas y pagos

Objetivo:

Crear herramientas administrativas y económicas.

Incluye:

* Ingresos.
* Gastos.
* Rentabilidad.
* Pagos online.
* Reportes.

Estado:

Pendiente

---

# Épica 9 — Comunicación y automatización

Objetivo:

Mejorar la comunicación entre pacientes y profesionales.

Incluye:

* Email.
* WhatsApp Business API.
* Recordatorios.
* Confirmaciones.
* Chatbot.

Estado:

Pendiente

---

# Épica 10 — Escalabilidad y despliegue

Objetivo:

Preparar la plataforma para producción.

Incluye:

* Optimización.
* Seguridad avanzada.
* Logs.
* Monitoreo.
* CI/CD.
* Deploy.

Estado:

Pendiente

---

# Metodología SCRUM aplicada

El proyecto seguirá una adaptación de SCRUM para desarrollo individual.

Aunque el desarrollo será realizado por una sola persona, se mantendrán las prácticas profesionales utilizadas en equipos reales.

---

# Roles dentro del proyecto

## Product Owner

Responsable de definir:

* Visión del producto.
* Prioridades.
* Funcionalidades necesarias.

Rol asumido por:

El desarrollador del proyecto.

---

## Scrum Master

Responsable de:

* Organización del trabajo.
* Seguimiento de objetivos.
* Eliminación de bloqueos.

Rol asumido durante el desarrollo mediante planificación y seguimiento continuo.

---

## Developer

Responsable de:

* Diseño técnico.
* Desarrollo.
* Testing.
* Documentación.

---

# Organización de los Sprints

Cada sprint tendrá una duración aproximada de una semana.

Estructura:

```text
Sprint Planning

        ↓

Desarrollo diario

        ↓

Revisión del incremento

        ↓

Retrospectiva

        ↓

Actualización del roadmap
```

---

# Sprint actual

## Sprint 1 — Fundamentos del proyecto

Objetivo:

Preparar la base completa para comenzar el desarrollo.

Incluye:

* Creación del repositorio.
* Configuración Git.
* Arquitectura inicial.
* Documentación.
* Entorno virtual Python.
* Preparación Docker.

Estado:

🟡 En progreso

---

# Definition of Done

Una funcionalidad será considerada terminada cuando:

* El código esté implementado.
* Existan pruebas correspondientes.
* La documentación esté actualizada.
* La funcionalidad haya sido validada.
* Los cambios estén registrados mediante Git.

---