Despliegue de la Aplicacion y la Base de Datos

1. Objetivo del documento

Este documento explica como levantar la base de datos PostgreSQL, como ejecutar la aplicacion Django y como dejar ambos servicios listos para pruebas locales o para mover el proyecto a otro equipo.

2. Requisitos previos

- Python instalado
- entorno virtual del proyecto
- dependencias instaladas
- Podman o Docker para la base de datos
- Git si se va a clonar el proyecto desde un repositorio

3. Estructura tecnica actual

- base de datos: PostgreSQL
- backend web: Django
- API: Django REST Framework
- frontend: Django Templates + Bootstrap

4. Archivo de configuracion `.env`

En la raiz del proyecto debe existir un archivo `.env` con valores similares a estos:

```env
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DB_ENGINE=postgresql
DB_NAME=tickets_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432
```

5. Crear el contenedor de PostgreSQL con Podman

5.1. Crear volumen

```bash
podman volume create tickets-postgres-data
```

5.2. Crear contenedor

```bash
podman run -d \
  --name tickets-postgres \
  -e POSTGRES_DB=tickets_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -v tickets-postgres-data:/var/lib/postgresql/data \
  postgres:16
```

5.3. Verificar contenedor

```bash
podman ps
```

```bash
podman logs tickets-postgres
```

5.4. Probar acceso a la BD

```bash
podman exec -it tickets-postgres psql -U postgres -d tickets_db
```

6. Alternativa con Docker

Si no se usa Podman, se puede hacer lo mismo con Docker:

```bash
docker volume create tickets-postgres-data
```

```bash
docker run -d \
  --name tickets-postgres \
  -e POSTGRES_DB=tickets_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -v tickets-postgres-data:/var/lib/postgresql/data \
  postgres:16
```

7. Levantar la aplicacion Django

Desde la raiz del proyecto:

```bash
python -m venv .venv
```

Activar el entorno virtual.

Linux o macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ir a la carpeta del proyecto Django:

```bash
cd src
```

Ejecutar migraciones:

```bash
python manage.py migrate
```

Cargar datos demo:

```bash
python manage.py seed_demo_data
```

Levantar el servidor:

```bash
python manage.py runserver
```

8. Usuarios de prueba

- `solicitante_demo / Demo1234*`
- `tecnico_demo / Demo1234*`

9. URL de acceso local

Una vez levantada la app:

```text
http://127.0.0.1:8000/
```

10. Pruebas recomendadas despues de levantar todo

Aplicacion web

- iniciar sesión
- crear ticket
- consultar tickets
- agregar nota
- cerrar ticket

API

- registro de usuario
- login
- listar tickets
- crear ticket
- cambiar estado
- registrar nota

11. Como mover el proyecto a otro equipo

1. Copiar o clonar el repositorio.
2. Crear el archivo `.env`.
3. Levantar PostgreSQL con Podman o Docker.
4. Crear y activar el entorno virtual.
5. Instalar dependencias.
6. Ejecutar migraciones.
7. Cargar datos demo.
8. Ejecutar la aplicacion.

12. Como subirlo para pruebas en otro lugar

Opciones simples:

- usar una maquina local o institucional con Python y PostgreSQL
- usar una VPS o servidor Linux
- usar un servicio de despliegue compatible con Django

Lo minimo necesario es:

- variable `.env`
- PostgreSQL accesible
- dependencias instaladas
- migraciones ejecutadas
- puerto de la aplicacion publicado

13. Si se quiere contenerizar tambien la app

La base de datos ya puede correr en contenedor. La app tambien podria contenerizarse despues, por ejemplo con:

- `Dockerfile`
- `podman build`
- `docker build`

En esta fase no fue necesario, porque el objetivo principal era dejar la aplicacion funcional y la base validada.

14. Comandos utiles de mantenimiento

Detener contenedor:

```bash
podman stop tickets-postgres
```

Iniciar contenedor existente:

```bash
podman start tickets-postgres
```

Eliminar contenedor:

```bash
podman rm -f tickets-postgres
```

Eliminar volumen:

```bash
podman volume rm tickets-postgres-data
```

15. Cierre

Con estos pasos se puede ejecutar la base de datos y la aplicacion en local, preparar el proyecto para demostracion y moverlo a otro equipo sin rehacer configuraciones internas del sistema.
