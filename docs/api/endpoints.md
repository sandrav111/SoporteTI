Endpoints de la API

Autenticacion

| Metodo | Endpoint | Descripcion |
| --- | --- | --- |
| `POST` | `/api/auth/register/` | Registro de usuario |
| `POST` | `/api/auth/login/` | Inicio de sesión |
| `POST` | `/api/auth/logout/` | Cierre de sesión |

Tickets

| Metodo | Endpoint | Descripcion |
| --- | --- | --- |
| `GET` | `/api/tickets/` | Listar tickets |
| `POST` | `/api/tickets/` | Crear ticket |
| `GET` | `/api/tickets/{id}/` | Consultar detalle de ticket |
| `PUT` | `/api/tickets/{id}/` | Actualizar ticket |
| `PATCH` | `/api/tickets/{id}/status/` | Cambiar estado |
| `POST` | `/api/tickets/{id}/notes/` | Registrar nota |

Catalogos

| Metodo | Endpoint | Descripcion |
| --- | --- | --- |
| `GET` | `/api/categories/` | Listar categorias |
| `GET` | `/api/priorities/` | Listar prioridades |
| `GET` | `/api/statuses/` | Listar estados |
