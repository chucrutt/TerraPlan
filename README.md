# TerraPlan

## ¿Qué es TerraPlan?
TerraPlan es una plataforma web interactiva diseñada para optimizar la distribución biológica y espacial de un huerto urbano. 

### Problema que resuelve
Planear un huerto es un desafío complejo, ya que requiere conocer qué plantas son compatibles entre sí (asociación de cultivos), qué distancias espaciales necesitan para crecer sin competir por nutrientes, y qué requerimientos de luz tienen. Un diseño incorrecto lleva a plagas, bajo rendimiento y frustración. TerraPlan automatiza de forma inteligente estos cálculos matemáticos y botánicos, entregando un plano visual de cultivo listo para usar.

### Usuario objetivo
Dirigido a huerteros urbanos, aficionados a la jardinería, ecologistas u organizadores de huertos comunitarios que desean maximizar el éxito y la salud de sus cosechas con ayuda de la tecnología, sin requerir conocimientos profundos previos en agronomía.

### Objetivo General
Proveer una herramienta SaaS *(Software as a Service)* centralizada donde los usuarios puedan gestionar múltiples terrenos y calcular distribuciones espaciales combinando simulación matemática con reglas biológicas reales (atracción y repulsión).

---

## Características (Features)

### Implementadas Actualmente (MVP)
- **Autenticación Multi-usuario:** Sistema de registro y login (dashboards privados por usuario).
- **Motor Lógico Espacial:** Algoritmo iterativo basado en geometría euclidiana y *Greedy Grid Search* que acomoda las plantas agregando fluctuaciones orgánicas (Jitter) e interferencias por compatibilidad (amistades botánicas).
- **Visualizador 2D Interactivo:** Representación visual proporcional del huerto en un mapa de coordenadas generado dinámicamente con HTML y CSS grid.
- **Gestión de Parcelas:** Creación, edición (retomando selecciones anteriores), eliminación y listado de múltiples configuraciones de siembra.
- **Enciclopedia Botánica (Catálogo):** Una base de datos integrada y explorable, con interfaz de búsquedas de texto dinámicas y filtrado por necesidad de sol de cada especie.

### Futuras Implementaciones (Backlog)
- Ajuste manual interactivo (*Drag & Drop*) para corregir manualmente el mapa sugerido por el algoritmo.
- Exportación del diseño en PDF/PNG para poder imprimir el mapa y llevarlo físicamente a la tierra.
- Mapeo de sombras estáticas del entorno (casas, árboles) para distribuir las semillas acorde a su necesidad de luz.
- Autocompletado inteligente (sugerir rellenar los huecos vacíos del huerto con especies beneficiosas vinculadas).
- Calendario temporal para agendamiento de tareas de riego, rotación de cultivos, y cosecha según la especie.

---

## Estructura del proyecto

A continuación se detalla la estructura principal del software y sus responsabilidades:

```text
TerraPlan/
├── manage.py              # Script principal para interactuar con el proyecto Django (correr servidor, migraciones, etc.)
├── requirements.txt       # Lista de dependencias y librerías de Python necesarias para el proyecto (Django, etc.)
├── BACKLOG.md             # Documento dinámico con la planeación ágil y priorizada de las tareas e ideas
├── terraplan/             # Directorio principal de configuración del proyecto
│   ├── settings.py        # Configuraciones globales de Django (apps, base de datos de SQLite, seguridad)
│   ├── urls.py            # Enrutador principal de URLs root del proyecto
│   └── ...
└── huerto/                # Aplicación central de lógica del negocio (El Huerto Urbano)
    ├── models.py          # Arquitectura de la BD relacional (Perfil, Planificacion, Planta, Compatibilidad)
    ├── forms.py           # ModelForms para recolectar el tamaño de la parcela y cantidades solicitadas
    ├── views.py           # Controladores de solicitudes HTTP (Dashboard, planificador, catalogo, auth)
    ├── utils.py           # Cerebro matemático: Algoritmos de geometría y colisión biológica
    ├── urls.py            # Vínculos internos entre páginas de la App
    ├── admin.py           # Registro de modelos de cara al panel de superusuario de Django
    └── templates/         # Directorio de recubrimiento de vistas (Frontend)
        └── huerto/
            ├── planificador.html # Canvas y formulario principal 2D
            ├── dashboard.html    # Bandeja de entrada multi-tenant
            ├── catalogo.html     # Navegador exploratorio del diccionario de plantas
            ├── login.html
            └── registro.html
```

---

## Cómo levantar el proyecto localmente

### 1. Requisitos
- Python 3.10 o superior *(Desarrollado sobre Python 3.14)*.
- Gestor de paquetes de Python (`pip`).

### 2. Clonar el repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd TerraPlan
```

### 3. Crear y activar Entorno Virtual
```bash
python -m venv venv

# ACTIVAR EL ENTORNO
# En Linux o macOS:
source venv/bin/activate
# En Windows (CMD/PowerShell):
venv\Scripts\activate
```

### 4. Instalar dependencias
Instala el framework web (Django) y complementos descritos en la lista:
```bash
pip install -r requirements.txt
```

### 5. Preparar la Base de Datos
Realiza las migraciones para que el ORM de Django construya el andamiaje SQLite:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Cargar Catálogo (Opcional pero Recomendado)
Si quieres manejar el panel de control como administrador y sembrar especies "quemadas" o precargadas:
```bash
python manage.py createsuperuser
```
*(Sigue las instrucciones para asignar tu email y contraseña. Luego en `127.0.0.1:8000/admin/` podrás añadir plantas manualmente).*

### 7. Levantar el puerto de Desarrollo
Pon en marcha la aplicación web local temporal:
```bash
python manage.py runserver
```

Abre cualquier navegador y entra a `http://127.0.0.1:8000/`.
---

## Stack Tecnológico
* **Backend:** Python + Arquitectura Django MVT.
* **Persistencia:** Base de datos relacional SQLite (Embebida, actualizable a PostgreSQL/MySQL).
* **Frontend:** Patrón CSR Renderizado en lado del Servidor vía Templates HTML5, CSS3 nativo y Layouts (Grid/Flexbox).

## Licencia
Este repositorio fue creado como Proyecto Formativo para CC4401 Ingeniería de Software Universidad de Chile.
