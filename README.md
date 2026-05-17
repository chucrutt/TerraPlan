# TerraPlan
Una plataforma web interactiva que optimice la distribución biológica y espacial de un huerto.

## Estructura del proyecto

A continuación se detalla la estructura base del proyecto y el propósito de cada archivo y directorio:

```text
TerraPlan/
├── manage.py              # Script principal para interactuar con el proyecto Django (correr servidor, migraciones, etc.)
├── requirements.txt       # Lista de dependencias y librerías de Python necesarias para el proyecto
├── terraplan/             # Directorio principal de configuración del proyecto
│   ├── __init__.py        # Indica que este directorio debe ser tratado como un paquete de Python
│   ├── asgi.py            # Configuración para servidores web compatibles con ASGI (despliegue asíncrono)
│   ├── settings.py        # Configuraciones globales de Django (apps, base de datos, seguridad, etc.)
│   ├── urls.py            # Enrutador principal de URLs del proyecto
│   └── wsgi.py            # Configuración para servidores web compatibles con WSGI (despliegue tradicional)
└── huerto/                # Aplicación principal del Huerto Urbano
    ├── __init__.py        # Indica que el directorio de la aplicación es un paquete Python
    ├── admin.py           # Configuración de los modelos para el panel de administración de Django
    ├── apps.py            # Configuración específica de esta aplicación
    ├── forms.py           # Formularios de la aplicación (captura de dimensiones y plantas del usuario)
    ├── models.py          # Definición de la Base de Datos (Plantas, Compatibilidad, Planificaciones)
    ├── templates/         # Directorio que contiene las plantillas HTML
    │   └── huerto/        # Plantillas específicas de la app (ej. planificador.html)
    ├── tests.py           # Pruebas unitarias
    ├── urls.py            # Enrutamiento local de las vistas de la aplicación
    ├── utils.py           # Lógica matemática y biológica de distribución espacial (Greedy Grid Search)
    └── views.py           # Controladores que conectan los modelos, formularios y plantillas
```
