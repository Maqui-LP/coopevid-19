from app.helpers.field_validation import email, min_length, max_length, is_number

def validateData(data, constraint):
    """ constraint = { email: [], required: [], number: [] }
    """

    emailFields = constraint.get('email', [])
    requiredFields = constraint.get('required', [])
    numberFields = constraint.get('number', [])

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
