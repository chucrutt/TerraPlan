# Product Backlog - TerraPlan

Este documento mantiene la lista centralizada, dinámica y priorizada de los requerimientos, funcionalidades y mejoras técnicas para el proyecto **TerraPlan**. 

---

## 1. Completado (Done - MVP y Funcionalidad Base)

* **[EPIC: Autenticación]** Sistema de registro y login de usuarios (Multi-tenant).
* **[EPIC: Modelado de Datos]** Estructura DB relacional (Django ORM) para `Planta`, `Compatibilidad`, `Planificacion` y `Perfil`.
* **[EPIC: Motor Lógico]** Algoritmo de "Greedy Grid Search" con geometría euclidiana para distribución de plantas basándose en repulsión/atracción biológica y variación natural (Jitter).
* **[EPIC: Gestión]** Dashboard para listar, crear, editar y eliminar huertos guardados por el usuario.
* **[EPIC: UI/Visualización]** Representación visual 2D del huerto mediante coordenadas HTML dinámicas y grillas CSS.
* **[EPIC: Exploración]** Enciclopedia/Catálogo botánico interactivo con búsqueda de texto y filtrado por necesidad de sol.

---

## 2. Alta Prioridad (To Do - Próximos Sprints)

* **[UX/UI] Mejoras en el Canvas Interactivo del Planificador**
  * *Historia:* Como usuario, quiero poder arrastrar y soltar (Drag & Drop) visualmente algunas plantas en el plano para corregir el algoritmo cuando prefiero un acomodo manual.
* **[Motor Lógico] Sugerencias Inteligentes (Auto-completar)**
  * *Historia:* Como usuario novato, quiero seleccionar una sola planta (ej: Tomate) y que el sistema me ofrezca "rellenar el huerto" automáticamente con plantas amigas (Albahaca, Zanahoria).
* **[Utilidad] Exportación de Resultados**
  * *Historia:* Como usuario, quiero poder descargar el plano de mi huerto como un archivo PDF o Imagen (PNG) para imprimirlo e ir al jardín real.
* **[Motor Lógico] Mapeo de Sombra y Entorno**
  * *Historia:* Como usuario, quiero definir qué partes de la cuadrícula de mi huerto reciben sol y cuáles sombra, para que el algoritmo no coloque plantas de Sol Directo en zonas oscuras.

---

## 3. Media Prioridad (Medio Plazo)

* **[Características] Calendario de Cuidados y Tareas**
  * *Historia:* Como usuario, quiero hacer clic en una planta de mi huerto y ver cuándo debo regarla, podarla o cosecharla. Integración con recordatorios.
* **[Características] Rotación de Cultivos (Dimensión Temporal)**
  * *Historia:* Como usuario, quiero que el sistema guarde el "Historial" de mi parcelas por temporada, alertándome si intento plantar la misma familia botánica en la misma tierra (prevención de plagas y agotamiento de suelo).
* **[Social] Compartir y Comunidad**
  * *Historia:* Como usuario, quiero poder hacer mi huerto "Público" para generar un enlace compartible y que otros usuarios puedan calificarlo o clonar mi diseño.

---

## 4. Baja Prioridad & "Icebox" (Ideas a futuro)
* * [Móvil] Desarrollar una PWA (Progressive Web App) o App Nativa para que los usuarios usen la app directo en la tierra con offline tracking.*
* * [IA] Integrar modelos de visión artificial para que el usuario suba una foto de una plaga y el sistema le recomiende un control biológico.*
* * [Monetización/Marketplace] Enlaces directos de compra de semillas basados en la lista de plantas del huerto planeado.*

---

## 5. Deuda Técnica y Operaciones (DevOps)

* **[Testing]** Implementar Pruebas Unitarias (Unit Tests) específicamente para las matemáticas en `utils.py` y validar escenarios de intersección extrema.
* **[DevOps]** Containerización del Entorno: Crear un archivo `Dockerfile` y `docker-compose.yml` para estandarizar el ambiente local de desarrollo.
* **[Infraestructura]** Migración de SQLite a PostgreSQL de cara a la preparación para despliegue en producción (ej. AWS, Heroku o Render).
* **[Arquitectura]** Separación de Frontend/Backend: Migrar la lógica de vistas visuales a una REST API (Django Rest Framework) y crear el Front en React/Vue si la complejidad del Canvas (arrastrar soltar) crece demasiado para Django Templates.