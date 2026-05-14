# Práctica FastAPI

Este repositorio contiene las prácticas que he realizado con FastAPI para la asignatura de Arquitectura del Software.

Durante la práctica he creado una API REST con Python. Primero hice una versión básica con endpoints sencillos y después la amplié para trabajar con una base de datos SQLite usando SQLAlchemy.

## Tecnologías utilizadas

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- aiosqlite
- Git y GitHub

## Qué se ha realizado

Primero he creado una API básica con FastAPI para trabajar con items. En esta parte se han creado endpoints para consultar, crear, actualizar y eliminar items.

Después he conectado la API a una base de datos SQLite. Para ello he separado el proyecto en varios archivos, como `database.py`, `models.py`, `schemas.py`, `dependencies.py`, `init_db.py` y `main.py`.

También he añadido relaciones entre tablas. En concreto, he creado categorías y tags:

- Una categoría puede tener varios items.
- Un item pertenece a una categoría.
- Un item puede tener varios tags.
- Un tag puede estar asociado a varios items.

## Endpoints principales

Algunos de los endpoints implementados son:

- `GET /items/`
- `GET /items/{item_id}`
- `POST /items/`
- `PUT /items/{item_id}`
- `DELETE /items/{item_id}`
- `GET /categorias/`
- `POST /categorias/`
- `GET /tags/`
- `POST /tags/`
- `POST /items/{item_id}/tags/{tag_id}`
- `POST /categorias/{cat_id}/items/`
