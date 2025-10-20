# risk-advisor-backend
Backend del proyecto de Inteligencia Artificial

### Requisitos Previos

- Python 3.13 o superior
- pip (gestor de paquetes de Python)
- virtualenv (opcional, pero recomendado)

### Pasos de Instalación

1. **Crear Entorno Virtual** Crea un entorno virtual para aislar las dependencias del proyecto.

   ```bash
   python -m venv env
   ```

2. **Activar Entorno Virtual**

   - En Windows:
     ```bash
     .\env\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source env/bin/activate
     ```

3. **Instalar Dependencias** Instala las dependencias necesarias para el proyecto.

   ```bash
   pip install poetry
   poetry install
   ```

## Ejecución del Proyecto

Para iniciar el servidor backend, utiliza el siguiente comando:

```bash
poetry shell
uvicorn app.main:app --reload
```

Esto iniciará el servidor en modo desarrollo y estará disponible en: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Estructura del Proyecto

El backend está desarrollado con FastAPI y sigue una estructura modular para mantener el código organizado y fácil de mantener.

- `app/`: Contiene el código fuente principal.
  - `main.py`: Punto de entrada de la aplicación.
  - `routes/`: Contiene los endpoints de la API.
  - `services/`: Lógica de negocio y servicios de extracción de datos.
  - `models/`: Definición de los modelos de datos utilizados por la aplicación, generalmente para interactuar con la base de datos.
  - `schemas/`: Esquemas de datos definidos mediante Pydantic para validar las solicitudes y respuestas de la API.
  - `middlewares/`: Contiene lógica que se ejecuta entre las solicitudes y las respuestas, como la gestión de errores o autenticación.
  - `utils/`: Funciones auxiliares y utilidades reutilizables en todo el proyecto.
  - `config/`: Configuraciones globales del proyecto, como variables de entorno y configuraciones de la base de datos.

## Licencia

Este proyecto está licenciado bajo los términos de la [GNU General Public License v3.0](LICENSE).