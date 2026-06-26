Uso de PostgreSQL en el Proyecto

Estado actual

El proyecto fue desarrollado con compatibilidad para `PostgreSQL` y `SQLite`.

- `SQLite` se utilizo en una fase inicial para desarrollo rapido.
- `PostgreSQL` fue validado posteriormente con una instancia real en contenedor, usando las variables de entorno del proyecto.

Validaciones realizadas sobre PostgreSQL:

- conexion real desde Django con `psycopg`
- ejecucion de `python manage.py migrate`
- ejecucion de `python manage.py seed_demo_data`
- ejecucion de `python manage.py test`
- verificacion de datos sembrados en la base principal

Variables requeridas

Crear un archivo `.env` en la raiz del proyecto con valores como los siguientes:

```env
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DB_ENGINE=postgresql
DB_NAME=tickets_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

Pasos de configuracion

1. Instalar PostgreSQL en el equipo local.
2. Crear la base de datos `tickets_db`.
3. Crear o ajustar el usuario definido en `.env`.
4. Ejecutar las migraciones.
5. Cargar datos demo.

Comandos

Desde la carpeta `src/`:

```bash
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

Validacion esperada en PostgreSQL

Se debe comprobar manualmente lo siguiente:

- acceso al login
- registro de usuario
- creacion de ticket
- consulta de tickets
- cambio de estado
- registro de nota
- cierre de ticket
- endpoints de autenticacion y tickets

Resultado de la validacion

La aplicacion quedo probada contra PostgreSQL con resultados satisfactorios.
