from flask import jsonify, request, abort
from app.models.centro import Centro

def index():
    page = int(request.args.get("page"))
    
    centros_totales = Centro.getAll()
    centros = Centro.getAllPaginado(page)
    json = []
    for centro in centros:
        dic = {
            "nombre": centro.name,
            "direccion": centro.address,
            "telefono": centro.phone,
            "hora_apertura":centro.openHour.isoformat(),
            "hora_cierre":centro.closeHour.isoformat(),
            "web":centro.web,
            "email":centro.mail
        }
        json.append(dic)
    return jsonify(centros=json, total=len(centros_totales), page=page)

def getById(id):
    centro = Centro.getCentroById(id)

    if (centro is None):
        abort(404)

    json_centro =  {
        "nombre": centro.name,
        "direccion": centro.address,
        "telefono": centro.phone,
        "hora_apertura":centro.openHour.isoformat(),
        "hora_cierre":centro.closeHour.isoformat(),
        "web":centro.web,
        "email":centro.mail
    }

    return jsonify(centro = json_centro) 