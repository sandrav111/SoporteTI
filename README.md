Aplicación web - Gestion de Tickets Sistemas

Proyecto desarollado con Python, Django y PostgreSQL para gestionar tickets e incidencias de soporte TI en una institucion educativa.

- Python
- Django
- PostgreSQL
- Django REST Framework
- Bootstrap

Modulos principales

- autenticacion y usuarios
- tickets
- notas de seguimiento
- catalogos de categorias, prioridades y estados
- API de autenticacion y tickets

Puesta en marcha

1. Crear y activar entorno virtual.
2. Instalar dependencias con `pip install -r requirements.txt`.
3. Copiar `.env.example` a `.env` y ajustar variables.
4. Ejecutar migraciones con `python manage.py migrate`.
5. Crear un superusuario con `python manage.py createsuperuser`.
6. Cargar datos de demostracion con `python manage.py seed_demo_data`.
7. Iniciar el servidor con `python manage.py runserver`.

Usuarios demo sugeridos

- `solicitante_demo / Demo1234*`
- `tecnico_demo / Demo1234*`
