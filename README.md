# PROYECTO BIBLIOTECA DJANGO
> Práctica integradora de Django con Python: gestión de libros y préstamos.
- requirements.txt
- .gitignore
- README.md
- CONSULTAS.md
- manage.py
- config
- catalogo

## Instalación
- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py showmigrations
- python manage.py loaddata datos
- python manage.py createsuperuser
- python manage.py runserver

## Uso
- Panel de administración: http://127.0.0.1:8000/admin
- Tests: python manage.py test catalogo
- Consultas y préstamos: catalogo/servicios.py
- Resultados de las consultas: CONSULTAS.md

## Base de datos
### SQLite
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### PostgreSQL
- pip install "psycopg[binary]"
- Crear una base de datos vacía
- Cambiar DATABASES en config/settings.py
- python manage.py migrate

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

## Autor
- Samuel Carbonell
