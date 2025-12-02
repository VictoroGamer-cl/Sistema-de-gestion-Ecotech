# 🌍 EcoTech ERP - Sistema de Gestión Corporativa

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Railway_Cloud-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-Desktop_GUI-2B2B2B?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey?style=for-the-badge)

## 📖 Descripción

**EcoTech** es una solución integral de escritorio (Desktop ERP) diseñada para la administración eficiente de recursos humanos y proyectos empresariales.

Desarrollado con una arquitectura modular en **Python**, el sistema implementa una interfaz gráfica moderna (High-DPI) utilizando `CustomTkinter` y conecta con una base de datos en la nube (**Railway**) para garantizar la disponibilidad de la información en tiempo real.

El proyecto destaca por implementar patrones de diseño profesionales como **DAO (Data Access Object)**, manejo de concurrencia con **Hilos (Threading)** y validaciones de seguridad robustas.

## 🚀 Características Principales

* **🔐 Seguridad y Accesos:** Sistema de Login con roles diferenciados (Administrador vs. Empleado) y encriptación de credenciales (SHA-256).
* **☁️ Arquitectura Cloud:** Persistencia de datos gestionada en **MySQL** alojado en la nube.
* **⚡ Rendimiento Optimizado:** Uso de **Multi-threading** para evitar bloqueos en la interfaz durante consultas pesadas.
* **📈 Integración API:** Conexión en tiempo real con APIs financieras para indicadores económicos (UF, Dólar, Euro) y generación de reportes en la nube.
* **✅ Validación de Datos:** Control estricto de entradas mediante Expresiones Regulares (Regex) para asegurar la integridad de la información (RUT, Emails, Fechas).

## 📦 Módulos del Sistema

### 👥 Gestión de Recursos Humanos
* CRUD completo de empleados.
* Automatización de creación de usuarios al registrar contratos.
* Búsqueda y filtrado de personal.

### 🏢 Estructura Organizacional (Departamentos)
* Gestión de departamentos y asignación de Gerentes.
* Validación de integridad referencial (protección contra borrado de departamentos activos).

### 📋 Gestión de Proyectos
* Asignación de empleados a proyectos con roles específicos (Relación Muchos a Muchos).
* Dashboard de control de estado de proyectos.

### ⏰ Control de Asistencia
* Registro individual de horas trabajadas y tareas.
* Visualización de historial para empleados y administradores.

### 📊 Reportabilidad
* Generación de informes en **PDF** y **Excel**.
* Historial de auditoría de reportes generados.

## 🛠️ Stack Tecnológico

### Lenguajes & Backend
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-F80000?style=for-the-badge&logo=oracle&logoColor=white)

### Librerías Clave
* **GUI:** `customtkinter`, `tkinter`, `pillow`
* **Datos:** `mysql-connector-python`
* **Red & APIs:** `requests`, `urllib`
* **Reportes:** `reportlab`, `openpyxl`

### Herramientas
![VS Code](https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![DBeaver](https://img.shields.io/badge/DBeaver-382970?style=for-the-badge&logo=dbeaver&logoColor=white)

## 🔧 Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/EcoTech-ERP.git](https://github.com/tu-usuario/EcoTech-ERP.git)
   cd EcoTech-ERP
