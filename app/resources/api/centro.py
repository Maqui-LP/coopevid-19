from flask import jsonify, request
from app.models.centro import Centro

def index():
    page = int(request.args.get("page"))
    print("********************************************")
    print(page)
    print("********************************************")

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