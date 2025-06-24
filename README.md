# JCFitness - Sistema de Administración de Gimnasio

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

JCFitness es una aplicación de escritorio de código abierto, desarrollada en Python con PyQt6, diseñada para ayudar a los dueños de pequeños y medianos gimnasios a gestionar su negocio de manera eficiente. Permite administrar miembros, controlar asistencias, registrar pagos, monitorear membresías y llevar un registro de las finanzas del día a día.

Este proyecto nace de la creencia en el software libre y accesible para todos.

## ✨ Características Principales

*   **Dashboard Interactivo:** Una vista rápida de las métricas más importantes: ganancias netas del día, miembros presentes, membresías activas y membresías por vencer.
*   **Gestión de Miembros (CRUD):** Registra, edita, busca y elimina miembros fácilmente.
*   **Control de Asistencia:** Registra la hora de entrada y salida de los miembros.
*   **Registro de Pagos:** Soporta pagos diarios y mensuales, con fechas personalizables.
*   **Seguimiento de Membresías:** Visualiza las membresías activas, sus fechas de vencimiento y recibe alertas visuales para las que están por expirar.
*   **Control Financiero:**
    *   Reportes de **Ganancias** mensuales y detallados por día.
    *   Registro de **Gastos** diarios (administración, aseo) y pagos a entrenadores.
    *   Cálculo de **Ganancia Neta** en tiempo real.
*   **Gestión de Entrenadores:** Registra entrenadores y los pagos que se les realizan.
*   **Interfaz Gráfica Intuitiva:** Diseñada para ser clara, amigable y fácil de usar.

## 📸 Capturas de Pantalla

| Dashboard Principal                                     | Gestión de Miembros                                 |
| ------------------------------------------------------- | --------------------------------------------------- |
| ![Dashboard](screenshots/dashboard.png)                 | ![Miembros](screenshots/miembros.png)               |
| **Control de Asistencia**                               | **Registro de Pagos**                               |
| ![Asistencias](screenshots/asistencias.png)             | ![Pagos](screenshots/pagos.png)                     |

*(Nota: Reemplaza las rutas `screenshots/*.png` con las rutas a tus imágenes)*

## 🛠️ Tecnologías Utilizadas

*   **Lenguaje:** Python 3
*   **Interfaz Gráfica:** PyQt6
*   **Base de Datos:** SQLite 3 (integrada, no requiere instalación de un servidor)

## 🚀 Instalación y Ejecución

Para ejecutar este proyecto en tu máquina local, sigue estos sencillos pasos.

### Prerrequisitos

*   Tener instalado [Python 3](https://www.python.org/downloads/).
*   Tener `pip` (el gestor de paquetes de Python) disponible en tu terminal.

### Pasos

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/JCFitness.git
    ```

2.  **Navega a la carpeta del proyecto:**
    ```bash
    cd JcFitness
    ```

3.  **Crea un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa: venv\Scripts\activate
    ```

4.  **Instala las dependencias:**
    El proyecto necesita la librería `PyQt6`. Puedes instalarla con el siguiente comando:
    ```bash
    pip install PyQt6
    ```

5.  **Ejecuta la aplicación:**
    ```bash
    python main.py
    ```
    ¡Y listo! La base de datos `jcfitness.db` se creará automáticamente en la misma carpeta si no existe.

## 🤝 ¿Cómo Contribuir?

¡Las contribuciones son el corazón del código abierto y son más que bienvenidas! Si tienes ideas para mejorar la aplicación, corregir un bug o añadir una nueva funcionalidad, sigue estos pasos:

1.  **Haz un Fork** de este repositorio.
2.  **Crea una nueva Rama** para tu funcionalidad (`git checkout -b feature/nombre-de-la-mejora`).
3.  **Realiza tus cambios** y haz commits descriptivos (`git commit -m 'Añade nueva funcionalidad X'`).
4.  **Haz un Push** a tu rama (`git push origin feature/nombre-de-la-mejora`).
5.  **Abre un Pull Request** para que podamos revisar tus cambios.

Algunas ideas para contribuir:
*   Reportar bugs y errores.
*   Sugerir nuevas características.
*   Mejorar la interfaz de usuario.
*   Optimizar las consultas a la base de datos.
*   Añadir traducciones a otros idiomas.

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**. Esto significa que eres libre de usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar y/o vender copias del software. Para más detalles, consulta el archivo `LICENSE`.

---

Creado con ❤️ por **(https://github.com/JSant-26)(https://github.com/eabarriostgc)**.
