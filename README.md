# 🏥 Medical CMS Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Sistema de gestión médica (CMS/EMR) desarrollado en **Python**, diseñado con **arquitectura limpia**, **programación defensiva** y **validación robusta de datos** para garantizar la integridad de la información clínica y la mantenibilidad a largo plazo.

---

### 🛠️ Tecnologías y Herramientas

`Python` • `FastAPI` • `Pydantic` • `SQLAlchemy` • `PostgreSQL` • `Git` • `GitHub` • `Markdown`

*Otras competencias:* Arquitectura Limpia (Clean Architecture), Programación Orientada a Objetos (POO), Validación de Datos (Data Cleaning), Persistencia de Datos, Módulos Independientes.

---

### 🎯 Objetivos Técnicos (A Mediano Plazo)

Para escalar este sistema de gestión al siguiente nivel, las próximas metas de desarrollo son:
1. **Desarrollo Web / APIs:** Exponer la lógica de dominio del sistema a través de una **REST API** asíncrona y documentada automáticamente con Swagger/OpenAPI usando **FastAPI**.
2. **Seguridad y Cumplimiento:** Implementar autenticación JWT y encriptación de datos médicos sensibles.

---

### 📂 Proyectos Destacados (Módulos de la Plataforma)

#### 📋 [Gestión de Pacientes y Clinical Data](https://github.com/tomasg1985/medical-cms-platform)
Módulo central para la administración de historias clínicas y expedientes médicos.
* **Foco técnico:** Limpieza y validación rigurosa de datos (Data Cleaning) en el ingreso de antecedentes médicos mediante Pydantic y programación defensiva.
* **Paradigma:** Aplicación estricta de arquitectura limpia y separación de responsabilidades para aislar la lógica de dominio de los componentes externos.

#### 📅 [Agenda y Control de Turnos](https://github.com/tomasg1985/medical-cms-platform)
Sistema de programación y asignación de citas médicas.
* **Foco técnico:** Lógica modular para la prevención de solapamientos horarios y persistencia de datos relacionales, garantizando un flujo sin conflictos.

#### 🔐 [Control de Acceso y Roles (RBAC)](https://github.com/tomasg1985/medical-cms-platform)
Módulo de seguridad local para la administración segura de permisos de médicos, recepcionistas y administradores.
* **Foco técnico:** Implementación de principios de POO y separación de capas para el manejo independiente de autenticación y autorización.

#### 📊 [Dashboard y Métricas Médicas](https://github.com/tomasg1985/medical-cms-platform)
Herramienta de análisis para el seguimiento de consultas e indicadores clave de la clínica.
* **Foco técnico:** Automatización de cálculos estadísticos e interfaces estructuradas por línea de comandos/API para la generación de reportes clínicos.
