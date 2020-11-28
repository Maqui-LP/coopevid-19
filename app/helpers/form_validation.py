from app.helpers.field_validation import email, min_length, max_length, is_number, date_format_validation, time_format_validation

def validateData(data, constraint):
    """ constraint = { email: [], required: [], number: [], fecha: [] }
    """

    emailFields = constraint.get('email', [])
    requiredFields = constraint.get('required', [])
    numberFields = constraint.get('number', [])
    dateFields = constraint.get('fecha', [])
    timeFields = constraint.get('time', [])

    # validamos todos los requeridos
    for field in requiredFields:
        error = min_length(data.get(field, ''), field, 1)
        if error:
            return error
        error = max_length(data.get(field, ''), field, 255)
        if error:
            return error

    # validamos todos los emails
    for field in emailFields:
        error = email(data.get(field, ''), field)
        if error:
            return error

    # validamos todos los numeros
    for field in numberFields:
        error = is_number(data.get(field, ''), field)
        if error:
            return error

    # validamos las fechas
    for field in dateFields:
        error = date_format_validation(data.get(field, ''), field)
        if error:
            return error
    
    # validamos las horas
    for field in timeFields:
        error = time_format_validation(data.get(field, ''), field)
        if error:
            return error

def validateConfiguracion(data):
    """ Validacion de titulo, descripcion, contacto, mantenimiento, paginacion
    """

    constraints = {}
    constraints['required'] = ['titulo', 'descripcion', 'contacto']
    constraints['email'] = ['contacto']
    constraints['number'] = ['paginacion']

    return validateData(data, constraints)

def validateUser(data):
    """ Validate user
    """

    constraints = {}
    constraints['required'] = ['username', 'first_name', 'last_name', 'email', 'password']
    constraints['email'] = ['email']

    return validateData(data, constraints)

def validateUpdateUser(data):
    """ Validate user sin contraseña
    """

    constraints = {}
    constraints['required'] = ['username', 'first_name', 'last_name', 'email']
    constraints['email'] = ['email']

    return validateData(data, constraints)

def validateCentro(data):
    """ Validate centro
    """

    constraints = {}
    constraints['required'] = ['name', 'phone', 'mail', 'openHour', 'closeHour', 'type_id', 'web', 'address', 'lat', 'long']
    constraints['mail'] = ['mail']

    return validateData(data, constraints)

def validateReserve(data):
    """ Validate reserva
    """

    constraints = {}
    constraints['required'] = ['fecha', 'hora', 'mail']
    constraints['mail'] = ['mail']
    constraints['fecha'] = ['fecha']
    constraints['time'] = ['hora']

    return validateData(data, constraints)