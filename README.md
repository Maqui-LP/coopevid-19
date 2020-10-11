 # Grupo 3

- Nicolas Rodriguez Boschi 16114/4
- Lindo Poisson Macarena 16016/3
- Guillermo Calderaro 16031/2

## Iniciar ambiente

### Requisitos

- python3
- virtualenv

### Ejecución

```bash
$ virtualenv -p python3 venv
# Para iniciar el entorno virtual
$ . venv/bin/activate
# Instalar las dependencias dentro del entorno virtual
$ pip install -r requirements.txt
# En el directorio raiz
$ FLASK_ENV=development python run.py
```

Para salir del entorno virutal, ejecutar:

```bash
$ deactivate
```

## Iniciar ambiente con Docker

### Requisitos

- docker-compose

### Ejecución 

```bash
$ docker-compose up
```

### Notas

- La aplicación flask está en `localhost:5000`
- PHPMyAdmin está en `localhost:8081`
- La información de la base de datos está en el directorio `data` en la raíz del proyecto. (Borrar **SÓLO EN CASO DE SER NECESARIO**)
- Es común que al volver a levantar el proyecto, pida borrar los directorios `data` y `flask_session` con permiso de sudo