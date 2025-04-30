## Instalar dependencias
1. 
```bash
python -m venv .venv
```
 2. 
```bash
pip install -r req.txt
```
## Crear la base de datos

1. 
```bash
python manage.py makemigrations
```
2. 
```bash
python manage.py migrate
```

## Ejecutar

```bash
python manage.py runserver
```