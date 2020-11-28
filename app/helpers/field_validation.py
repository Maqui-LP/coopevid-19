import re

def email(field, name):
    regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    if not re.search(regex, field):
        return "El campo " + str(name) + " no es un formato de email valido"

    return None

def min_length(field, name, length):
    if len(field) < length:
        message = "El campo " + str(name) + " no posee el tamaño minimo de " + str(length) + " caracteres"
        return message
    
    return None


def max_length(field, name, length):
    if len(field) > length:
        message = "El campo " + str(name) + " supera el tamaño maximo de " + str(length) + " caracteres"
        return message

        return 1
    
    return None

def is_number(field, name):
    try:
        float(field)
        return None
    except ValueError:
        message = "El campo " + str(name) + " debe ser un numero"
        return "Debe ser un valor numerico"

def date_format_validation(field, name):
    regex = "\d{4}-\d{2}-\d{2}" 
    if not re.search(regex, field):
        return "El campo " + str(name) + " no es un formato de fecha valido"
    return None

def time_format_validation(field, name):
    regex = "\d{2}\:\d{2}:\d{2}"
    if not re.search(regex,field):
        return "El campo " + str(name) + " no es un formato de hora valido"
    return None
        